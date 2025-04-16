const express = require('express');
const auth = require('../middleware/auth');
const User = require('../models/User');
const router = express.Router();

// Get user profile
router.get('/profile', auth, async (req, res) => {
  try {
    res.json({
      id: req.user._id,
      name: req.user.name,
      email: req.user.email,
      type: req.user.type,
      preferences: req.user.preferences,
      location: req.user.location,
      avatar: req.user.avatar
    });
  } catch (error) {
    res.status(500).json({ message: 'Error fetching profile', error: error.message });
  }
});

// Update user preferences
router.patch('/preferences', auth, async (req, res) => {
  try {
    const { preferences, location, additionalInfo } = req.body;
    
    const updatedUser = await User.findByIdAndUpdate(
      req.user._id,
      { preferences, location, additionalInfo },
      { new: true }
    );

    res.json({
      id: updatedUser._id,
      name: updatedUser.name,
      email: updatedUser.email,
      type: updatedUser.type,
      preferences: updatedUser.preferences,
      location: updatedUser.location,
      avatar: updatedUser.avatar
    });
  } catch (error) {
    res.status(500).json({ message: 'Error updating preferences', error: error.message });
  }
});

module.exports = router;