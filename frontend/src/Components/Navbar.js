import React, { Component } from 'react'
import './Navbar.css'

export class Navbar extends Component {
    render() {
        return (
            <div>
                <header>
                    <nav className="navbar navbar-expand-md navbar-dark bg-steel">
                    <div className="container">
                        <a className="navbar-brand mr-4" href="/">Developers Connect</a>
                        <div className="collapse navbar-collapse" id="navbarToggle">
                        <div className="navbar-nav mr-auto">
                            <a className="nav-item nav-link" href="/">Home</a>
                        </div>
                        {/* <!-- Navbar Right Side --> */}
                        <div className="navbar-nav">
                            {this.props.isLoggedIn ?
                                <>
                                <a className="nav-item nav-link" href="/account">Account</a>
                                <a className="nav-item nav-link" href="/messages">Messages</a>
                                <a class="nav-item nav-link" href="/logout">Logout</a>
                                </>
                             :
                             <>
                             <a className="nav-item nav-link" href="/">Login</a>
                             <a className="nav-item nav-link" href="/register">Register</a>
                             </>
                            }
                        </div>
                        </div>
                    </div>
                    </nav>
                </header>
            </div>
        )
    }
}

export default Navbar
