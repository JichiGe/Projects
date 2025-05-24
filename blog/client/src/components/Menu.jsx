

import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import '../style/menu.css'
const Menu = ({ cat }) => {
    const [posts, setPosts] = useState([]);

    useEffect(() => {

        const fetchPosts = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_API_URL}/blogs?cat=${cat}`);
                if (!response.ok) {
                    console.log(`HTTP error! status: ${response.status}`);
                }
                let data = await response.json();
                data = Array.from(data);
                setPosts(data);


            }
            catch (error) {
                console.log('Error fetching posts:', error);
            }
        }
        fetchPosts();
    }, [cat]);
    return (
        <div className='menu'>
            <h1>Other posts you may like</h1>
            {posts.map((posts) => (
                <div className='post' key={posts.id}>
                    <img src={posts?.img} alt="post" />
                    <div className='content'>
                        <h2>{posts?.title}</h2>
                        <Link className="link" to={`/details/${posts?.id}`}>
                            <h6>Read More</h6>
                        </Link>
                    </div>
                </div>
            ))}

        </div>
    )
}

export default Menu