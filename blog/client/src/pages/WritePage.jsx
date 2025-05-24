
import '../style/writePage.css'
import React, { useState } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import { useLocation, useNavigate } from "react-router-dom";
import { useAuthToken } from "../AuthTokenContext";

const WritePage = () => {
  const state = useLocation().state;
  const [value, setValue] = useState(state?.desc || '');
  const [title, setTitle] = useState(state?.title || '');
  const navigate = useNavigate()
  const [category, setCategory] = useState(state?.category || '');
  const { accessToken } = useAuthToken();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {


      if (!title.trim() || !value.trim() || !category.trim()) {
        alert('Please fill in all fields.');
        return;
      }
      // Prepare data to send
      const postData = {
        title,
        desc: value,
        category,


      };



      // Determine HTTP method and URL based on whether it's an update or creation
      const url = state ? `${process.env.REACT_APP_API_URL}/blogs/${state.id}` : `${process.env.REACT_APP_API_URL}/blogs`;
      const method = state ? 'PUT' : 'POST';
      console.log('url:', url)
      // Send the request using fetch
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(postData)
      });

      // Check if request was successful
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Redirect to home page
      navigate("/");
    } catch (err) {
      console.log(err);
    }
  };


 

  return (
    <div className='add'>
      <div className="content">
        <input type='text' placeholder='Title' value={title} onChange={e => setTitle(e.target.value)} />
        <div className="editorContainer">
          <ReactQuill className="editor" theme="snow" value={value} onChange={setValue} />
        </div>
      </div>
      <div className="menu">
        <div className="item">
          <h1>
            Publish
          </h1>

          <div className='btn'>

            <button onClick={handleSubmit}>publish</button>
          </div>
        </div>
        <div className="item">
          <h1>Category</h1>
          <div className="category">
            <input type='radio' checked={category === "art"} name='category' value="art" id='art' onChange={e => setCategory(e.target.value)} />
            <label htmlFor="art">Art</label>
          </div>
          <div className="category">
            <input type='radio' checked={category === "science"} name='category' value="science" id='science' onChange={e => setCategory(e.target.value)} />
            <label htmlFor="science">Science</label>
          </div>
          <div className="category">
            <input type='radio' checked={category === "technology"} name='category' value="technology" id='technology' onChange={e => setCategory(e.target.value)} />
            <label htmlFor="technology">Technology</label>
          </div>
          <div className="category">
            <input type='radio' checked={category === "cinema"} name='category' value="cinema" id='cinema' onChange={e => setCategory(e.target.value)} />
            <label htmlFor="cinema">Cinema</label>
          </div>
          <div className="category">
            <input type='radio' checked={category === "design"} name='category' value="design" id='design' onChange={e => setCategory(e.target.value)} />
            <label htmlFor="design">Design</label>
          </div>
          <div className="category">
            <input type='radio' checked={category === "food"} name='category' value="food" id='food' onChange={e => setCategory(e.target.value)} />
            <label htmlFor="food">Food</label>
          </div>
        </div>
      </div>
    </div>
  )
}

export default WritePage