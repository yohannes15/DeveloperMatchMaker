import React, { Component } from 'react'
import './Homeboard.css'

export class Homeboard extends Component {
    render() {
        return (
            <div>
                <p className="tagline">Find Developers <ins>at</ins> St John's&nbsp;University.</p>
                <section className="banner">
                    <div className="wrapper">
                        <div className="blurb">
                            <h2>Find Developers At SJU</h2>
                            <p>Have a great idea for a project or a product and require help? Or are you trying to grow your skills through team collaboration? SJU Dev Connect is the best place for developers to find each other.</p>
                            <a className="indexbutton" href="">Create a Profile</a>
                        </div>
                    </div>
                </section>
            </div>
        )
    }
}

export default Homeboard
