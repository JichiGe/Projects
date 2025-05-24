import React from 'react'
import { Link } from 'react-router-dom'
import '../style/navbar.css'
import Logo from "../img/logo.png"
import { useAuth0 } from "@auth0/auth0-react";

const Navbar = () => {
  const { loginWithRedirect, logout, isAuthenticated } = useAuth0();

  const login = () => {
    loginWithRedirect({ screen_hint: "signin" });
  };

  const logoutWithRedirect = () =>
    logout({
      logoutParams:{returnTo:  window.location.origin,}
    });
  return (
    <div className='navbar'>
      <div className="container">
        <div className='logo'>
          <Link to="/">
            <img src={Logo} alt="logo" />
          </Link>
        </div>
        <div className='links'>
          <Link className='link' to="/?cat=art">
            <h6>ART</h6>
          </Link>
          <Link className='link' to="/?cat=science">
            <h6>SCIENCE</h6>
          </Link>
          <Link className='link' to="/?cat=technology">
            <h6>TECHNOLOGY</h6>
          </Link>
          <Link className='link' to="/?cat=cinema">
            <h6>CINEMA</h6>
          </Link>
          <Link className='link' to="/?cat=design">
            <h6>DESIGN</h6>
          </Link>
          <Link className='link' to="/?cat=food">
            <h6>FOOD</h6>
          </Link>
          {!isAuthenticated ? (
            <span className="link" onClick={login}>
              Login
            </span>
          ) : (
            <span className="link" onClick={logoutWithRedirect}>
              Logout
            </span>
          )}

          <Link className="authLink" to="/profile"><span>Profile</span></Link>


          <Link className="authLink" to="/debug"><span>Debug</span></Link>


          <Link className="authLink" to="/post"><span>Write</span></Link>



        </div>
      </div>
    </div>
  )
}

export default Navbar