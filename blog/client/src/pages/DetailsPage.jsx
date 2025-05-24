import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { useAuth0 } from "@auth0/auth0-react";
import { useAuthToken } from "../AuthTokenContext";
import moment from 'moment';
import parse from 'html-react-parser';
import '../style/detailsPage.css';
import Edit from "../img/edit.png";
import Delete from "../img/delete.png";
import Menu from "../components/Menu";

const DetailsPage = () => {
  const [post, setPost] = useState({});
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  
  const location = useLocation();
  const postId = location.pathname.split('/')[2];
  const { user } = useAuth0();
  const { accessToken } = useAuthToken();

  useEffect(() => {
    async function fetchPosts() {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/blogs/${postId}`);
      const data = await res.json();
      if (data && Object.keys(data).length) {
        setPost(data);
        setComments(data.Comments || []);

      } else {
        console.log('Error fetching posts:', data);
      }
    };

    fetchPosts();
  }, [postId]);

  const handleDelete = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/blogs/${postId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      window.location.href = '/';
    } catch (error) {
      console.error('Error deleting post:', error);
    }
  };

  const handleCommentSubmit = async () => {
    if (!newComment.trim()) return;

    const response = await fetch(`${process.env.REACT_APP_API_URL}/blogs/${postId}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: newComment }),
    });

    if (response.ok) {
      const comment = await response.json();
      setComments([...comments, comment]);
      setNewComment('');
    } else {
      console.error('Failed to post comment');
    }
  };

  return (
    <div className="detail">
      <div className="content">
        <img src={post?.img} alt="" />
        <div className="user">
          <img src={post.User?.userImg} alt='' />
          <div className="info">
            <span>{post.User?.name}</span>
            <p>Posted {moment(post.createdAt).fromNow()}</p>
          </div>
          {user?.sub === post.User?.auth0Id && (
            <div className='edit'>
              <Link to='/post?edit=2' state={post}>
                <img src={Edit} alt="edit" />
              </Link>
              <img onClick={handleDelete} src={Delete} alt="delete" />
            </div>
          )}
        </div>
        <div className='title'>
          <h1>{post.title}</h1>
        </div>
        {typeof post.desc === 'string' && parse(post.desc)}
        <div>
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Add a comment..."
          />
          <button onClick={handleCommentSubmit}>Post Comment</button>
        </div>
        <div className="comments">
          {comments.map((comment) => (
            <div key={comment.id} className="comment">
              <p>{comment.text}</p>
            </div>
          ))}
        </div>
      </div>
      {post.category && <Menu cat={post.category} />}
    </div>
  );
};

export default DetailsPage;
