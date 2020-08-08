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
                            {/* <a className="nav-item nav-link" href="{{ url_for('account') }}">Account</a>
                            <a className="nav-item nav-link" href="{{ url_for('messages') }}">Messages
                                {% set new_messages = current_user.new_messages() %}
                                <span id="message_count" className="badge"
                                    style="visibility: {% if new_messages %}visible
                                                        {% else %}hidden {% endif %};">
                                    {{ new_messages }}
                                </span>
                            </a>
                            <a className="nav-item nav-link" href="{{ url_for('logout') }}">Logout</a> */}


                            {/* {% else %} */}
                            <a className="nav-item nav-link" href="/login">Login</a>
                            <a className="nav-item nav-link" href="/register">Register</a>
                            {/* {% endif %} */}
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
