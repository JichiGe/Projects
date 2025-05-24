import React, { useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import '../style/homePage.css'
import Weather from '../components/Weather';
import parse from 'html-react-parser';
const HomePage = () => {

  const [posts, setPosts] = React.useState([]);
  const cat = useLocation().search
  useEffect(() => {
    const fetchPosts = async () => {
      try {

        const response = await fetch(`${process.env.REACT_APP_API_URL}/blogs${cat}`);
        const data = await response.json();
        setPosts(data);
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    };
    fetchPosts();

  }, [cat]);



  return (
    <div className="home">
      <Weather />
      <div className="posts">
        {Array.isArray(posts) ? posts.map((post) => (
          <div key={post.id} className="postItem">
            <div className='postItem_img'>
              <img src={post.img} alt="" />
            </div>
            <div className='postItem_content'>
              <Link to={`/details/${post.id}`} className='link'>
                <h1>{post.title}</h1>
                {typeof post.desc === 'string' && parse(post.desc)}
                <div><button>
                  Read More
                </button></div>

              </Link>
            </div>
          </div>
        )) : (
          <p>No posts found</p>
        )}
      </div>
    </div>
  );
}

export default HomePage