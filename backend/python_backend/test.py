# Sample donor preferences
donor = {
    "name": "Aarav",
    "interests": ["education", "mental health"]
}

# Sample causes
causes = [
    {"id": 1, "name": "Teach for Change", "tags": ["education", "children"]},
    {"id": 2, "name": "MindCare", "tags": ["mental health", "youth"]},
    {"id": 3, "name": "EcoSave", "tags": ["environment", "climate"]}
]
def recommend_causes(donor_tags, causes):
    recommendations = []
    for cause in causes:
        match_score = len(set(donor_tags) & set(cause['tags']))
        if match_score > 0:
            recommendations.append((match_score, cause))
    # Sort by best matches
    recommendations.sort(key=lambda x: x[0], reverse=True)
    return [cause for score, cause in recommendations]
# Run recommender
recommended = recommend_causes(donor["interests"], causes)

# Display results
for cause in recommended:
    print(f"Recommended: {cause['name']} (Tags: {', '.join(cause['tags'])})")
