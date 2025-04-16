from flask import Flask, jsonify, request
from flask_cors import CORS
from user import User
from cause import Cause
from database import db, db_client
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
import os
from dotenv import load_dotenv
import jwt

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure MongoDB
app.config['MONGODB_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/aidai_db')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'your-super-secret-key')

# Initialize JWT
jwt = JWTManager(app)

# Initialize MongoDB
db.init_app(app)

def verify_token():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].replace('Bearer ', '')
    
    if not token:
        return None
        
    try:
        # Check if token exists in database
        token_doc = db_client.tokens.find_one({'token': token})
        if not token_doc:
            return None
            
        # Verify JWT
        decoded = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
        user = User.objects(id=decoded['userId']).first()
        return user
    except Exception:
        return None

def jwt_required(fn):
    def wrapper(*args, **kwargs):
        user = verify_token()
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def recommend_causes(donor_tags, location, causes):
    recommendations = []
    for cause in causes:
        # Calculate tag match score
        match_score = len(set(donor_tags) & set(cause.tags))
        
        # Add location boost if locations match
        if location and cause.location.lower() == location.lower():
            match_score += 2
            
        if match_score > 0:
            recommendations.append((match_score, cause))
    
    # Sort by best matches
    recommendations.sort(key=lambda x: x[0], reverse=True)
    return [cause for score, cause in recommendations]

@app.route('/api/recommendations', methods=['GET'])
@jwt_required
def get_recommendations():
    try:
        user = verify_token()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Get all causes
        causes = Cause.objects.all()
        
        # Get recommendations based on user preferences and location
        recommended_causes = recommend_causes(
            user.preferences or [], 
            user.location,
            causes
        )
        
        # Convert to JSON-serializable format
        response = [{
            'id': str(cause.id),
            'name': cause.name,
            'organization': cause.organization,
            'description': cause.description,
            'image': cause.image,
            'goal': cause.goal,
            'raised': cause.raised,
            'tags': cause.tags,
            'location': cause.location,
            'impact': cause.impact,
            'donorCount': cause.donorCount,
            'verified': cause.verified
        } for cause in recommended_causes]
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)