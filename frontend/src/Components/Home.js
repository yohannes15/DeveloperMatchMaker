import React, { Component } from 'react'
import Axios from 'axios'
import {check} from './util/login'
import './Home.css'

const alignCenter = {
    textAlign: 'center'
}

const marginBottom = {
    marginBottom: '10px'
}

export class Home extends Component {

    componentDidMount() {
        // check if current user has registered
        if (check()){
            Axios.get("http://localhost:5000/api/hasinterests").then(res => {
                if (res.data.error) {
                    window.location = '/add_interests'
                }
            })
        }

    }

    render() {
        return (
            <div>
                <div className="container">
                    <div className="section" style={alignCenter}>
                        <h2>Developers At SJU</h2>
                    </div>
                </div>

                <div className="container">
                    <div className="grid">
                        <div style = {marginBottom} className="flip-container">
                            <div className="flipper">
                                <div className="front">
                                    <img className="profile-picture" src="https://image.shutterstock.com/image-photo/white-transparent-leaf-on-mirror-260nw-1029171697.jpg" width="250px" height="250px" />
                                    <div className="profile-devider"></div>
                                    <h3 className="profile-name">Yohannes Berhane</h3>
                                        <ul className="tags">
                                            <div className="programming-lang">
                                                <li><a href='#'>Python</a></li>
                                            </div>

                                            <li><a href='#'>Java</a></li>

                                            <div className="field-interest" >
                                                <li><a href="#">Software Engineering</a></li>
                                            </div>
                                        </ul>
                                </div>

                                <div className="back">
                                    <div className="flip-padding">
                                        <div>
                                            <h5>Primary Langugae</h5>
                                            <p>Python</p>

                                            <h5>Secondary Language</h5>
                                            <p>Java</p>

                                            <h5>Years of Experience</h5>
                                            <p>4</p>

                                            <h5>Database System</h5>
                                            <p>PostgreSQL</p>

                                            <a href="#"><button className="follow-button">Visit Profile</button></a>
                                        </div>
                                    </div>

                                </div>

                            </div>
                        </div>

                    </div>
                </div>
            </div>


        )
    }
}

export default Home


