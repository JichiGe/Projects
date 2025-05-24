import React, { useEffect, useState } from 'react';
import '../style/profilePage.css';
import { useAuthToken } from '../AuthTokenContext';

const ProfilePage = () => {
  const { accessToken } = useAuthToken();
  const [userData, setUserData] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [bio, setBio] = useState('');

  useEffect(() => {
    if (accessToken) {
      (async () => {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/profile`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`
          }
        });
        if (response.ok) {
          const user = await response.json();
          setUserData(user);
          setBio(user.bio);
        }
      })();
    }
  }, [accessToken]);

  const handleBioChange = (event) => {
    setBio(event.target.value);
  };

  const saveBio = async () => {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/users/${userData.id}`, {
      method: 'PATCH',
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`
      },
      body: JSON.stringify({ bio })
    });

    if (response.ok) {
      const updatedUser = await response.json();
      setUserData(updatedUser);
      setEditMode(false);
    }
  };

  if (!userData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="profile-page">
      <h1>Profile Page</h1>
      <div>
        <img src={userData.userImg || 'defaultURL'} alt="Profile" />
        <p><strong>Email:</strong> {userData.email}</p>
        <p><strong>name:</strong> {userData.name}</p>
        <p><strong>UserId:</strong> {userData.id}</p>

        {editMode ? (
          <div>
            <textarea value={bio} onChange={handleBioChange} />
            <button onClick={saveBio}>Save Bio</button>
          </div>
        ) : (
          <div>
            <p><strong>Bio:</strong> {userData.bio}</p>
            <button onClick={() => setEditMode(true)}>Edit Bio</button>
          </div>
        )}
      </div>
    </div>
  );
}

export default ProfilePage;
