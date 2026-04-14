import React, { useState, useEffect } from 'react';
import type { UserProfile } from '../types';
import { profileService } from '../services/profileServices';
import '../styles/ProfilePage.css';
import SEO from '../components/SEO';



const ProfilePage: React.FC = () => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [formData, setFormData] = useState({
    first_name: '',
    gender: 'Other' as 'M' | 'F' | 'Other',
    age: '',
    height_cm: '',
    weight_kg: '',
    target_weight_kg: '',
    bio: ''
  });

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const data = await profileService.getProfile();
      setProfile(data);
      setFormData({
        first_name: data.first_name || '',
        gender: data.gender || 'Other',
        age: data.age ? String(data.age) : '',
        height_cm: data.height_cm ? String(data.height_cm) : '',
        weight_kg: data.weight_kg ? String(data.weight_kg) : '',
        target_weight_kg: data.target_weight_kg ? String(data.target_weight_kg) : '',
        bio: data.bio || ''
      });
    } catch (err) {
      setError('Failed to load profile');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setError('');
      setSuccess('');
      
      const dataToSend = {
        ...formData,
        age: formData.age ? parseInt(formData.age) : null,
        height_cm: formData.height_cm ? parseInt(formData.height_cm) : null,
        weight_kg: formData.weight_kg ? parseFloat(formData.weight_kg) : null,
        target_weight_kg: formData.target_weight_kg ? parseFloat(formData.target_weight_kg) : null
      };

      const updated = await profileService.updateProfile(dataToSend);
      setProfile(updated);
      setIsEditing(false);
      setSuccess('Profile updated successfully!');
    } catch (err) {
      setError('Failed to update profile');
      console.error(err);
    }
  };

  if (loading) return <div className="profile-container"><p>Loading...</p></div>;

    return (
        <>
            <SEO
              title="Профиль"
              description="Личный кабинет пользователя"
              canonical="/profile"
              noIndex={true} // ← не индексировать
            />  
    <div className="profile-container">
      <div className="profile-card">
        <h1>👤 My Profile</h1>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        {!isEditing ? (
          <div className="profile-view">
            <div className="profile-grid">
              <div className="profile-item">
                <span className="label">Username</span>
                <span className="value">{profile?.username}</span>
              </div>
              <div className="profile-item">
                <span className="label">Email</span>
                <span className="value">{profile?.email}</span>
              </div>
              <div className="profile-item">
                <span className="label">Full Name</span>
                <span className="value">{profile?.first_name || 'Not set'}</span>
              </div>
              <div className="profile-item">
                <span className="label">Gender</span>
                <span className="value">
                  {profile?.gender === 'M' ? '👨 Male' : profile?.gender === 'F' ? '👩 Female' : 'Other'}
                </span>
              </div>
              <div className="profile-item">
                <span className="label">Age</span>
                <span className="value">{profile?.age || 'Not set'} years</span>
              </div>
              <div className="profile-item">
                <span className="label">Height</span>
                <span className="value">{profile?.height_cm || 'Not set'} cm</span>
              </div>
              <div className="profile-item">
                <span className="label">Current Weight</span>
                <span className="value">{profile?.weight_kg || 'Not set'} kg</span>
              </div>
              <div className="profile-item">
                <span className="label">Target Weight</span>
                <span className="value">{profile?.target_weight_kg || 'Not set'} kg</span>
              </div>
              <div className="profile-item">
                <span className="label">BMI (Body Mass Index)</span>
                <span className="value">
                  {profile?.bmi ? `${profile.bmi}` : 'Not calculated'}
                  {profile?.bmi && ` (${getBmiCategory(profile.bmi)})`}
                </span>
              </div>
              <div className="profile-item full-width">
                <span className="label">Bio</span>
                <span className="value">{profile?.bio || 'Not set'}</span>
              </div>
            </div>
            <button className="btn btn-primary" onClick={() => setIsEditing(true)}>
              ✏️ Edit Profile
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="profile-form">
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                placeholder="Enter your full name"
              />
            </div>

            <div className="form-group">
              <label>Gender</label>
              <select name="gender" value={formData.gender} onChange={handleChange}>
                <option value="M">👨 Male</option>
                <option value="F">👩 Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div className="form-group">
              <label>Age</label>
              <input
                type="number"
                name="age"
                value={formData.age}
                onChange={handleChange}
                placeholder="Enter your age"
                min="1"
                max="150"
              />
            </div>

            <div className="form-group">
              <label>Height (cm)</label>
              <input
                type="number"
                name="height_cm"
                value={formData.height_cm}
                onChange={handleChange}
                placeholder="Enter your height in cm"
                min="50"
                max="250"
              />
            </div>

            <div className="form-group">
              <label>Current Weight (kg)</label>
              <input
                type="number"
                name="weight_kg"
                value={formData.weight_kg}
                onChange={handleChange}
                placeholder="Enter your weight in kg"
                step="0.1"
                min="20"
                max="500"
              />
            </div>

            <div className="form-group">
              <label>Target Weight (kg)</label>
              <input
                type="number"
                name="target_weight_kg"
                value={formData.target_weight_kg}
                onChange={handleChange}
                placeholder="Enter your target weight in kg"
                step="0.1"
                min="20"
                max="500"
              />
            </div>

            <div className="form-group">
              <label>Bio</label>
              <textarea
                name="bio"
                value={formData.bio}
                onChange={handleChange}
                placeholder="Tell us about yourself"
                rows={4}
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                💾 Save Changes
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => setIsEditing(false)}
              >
                ❌ Cancel
              </button>
            </div>
          </form>
        )}
      </div>
            </div>
      </>
  );
};

function getBmiCategory(bmi: number): string {
  if (bmi < 18.5) return 'Underweight';
  if (bmi < 25) return 'Normal weight';
  if (bmi < 30) return 'Overweight';
  return 'Obese';
}

export default ProfilePage;
