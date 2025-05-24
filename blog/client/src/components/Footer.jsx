import React from 'react'
import Logo from "../img/logo.png"
import '../style/footer.css'
const Footer = () => {
  return (
    <div className="footerDiv">
      <footer>
        <img src={Logo} alt="logo"/>
        <span>
          Made for <b>CS5610</b>.
        </span>
      </footer>

    </div>
    
  )
}

export default Footer