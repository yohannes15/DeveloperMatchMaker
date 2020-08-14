import React, { Component } from 'react'
import Axios from 'axios'
import {check} from './util/login'
import './Home.css'
import {withRouter} from 'react-router-dom'

const alignCenter = {
    textAlign: 'center'
}

const marginBottom = {
    marginBottom: '10px'
}

export class Home extends Component {
    constructor(props){
        super(props)
        this.state = {
            allInterests: [],
            usersStack: [],
            interests: [],
        }
        
    }

    componentDidMount() {
        // check if current user has registered
            const token = localStorage.getItem("token")

            Axios.all([
                Axios.get("http://localhost:5000/api/hasinterests", {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': token
                    }
                }),
                Axios.get("http://localhost:5000/api/get_users", {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': token
                    }  
            })])
            .then(Axios.spread((hasInterestsRes, getUsersRes) => {
                if (hasInterestsRes.data.error) {
                    console.log(hasInterestsRes.data.error)
                    this.props.history.push('/add_interests')
                }
                else if (hasInterestsRes.data.success && !getUsersRes.data.error){
                    this.setState({
                        allInterests: getUsersRes.data.all_interests,
                        usersStack: getUsersRes.data.users_stack,
                        interests: getUsersRes.data.interests,
                    })
                    console.log(getUsersRes.data.all_interests[0][2])
                    console.log(getUsersRes.data.users_stack[1])
                    console.log(getUsersRes.data.interests)
                }
            }))
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
                        {this.state.usersStack.map((user, index)=> {
                            return (
                                <div style = {marginBottom} className="flip-container" key={index}>
                                    <div className="flipper">
                                        <div className="front">
                                            <img className="profile-picture" src="#" width="250px" height="250px" />
                                            <div className="profile-devider"></div>
                                            <h3 className="profile-name">{user.firstname} {user.lastname}</h3>
                                            {this.state.interests.map((interest, index) => {
                                                if (user.id == interest.user_id){
                                                    return (
                                                        <ul className="tags" key={index}>
                                                            {this.state.allInterests[0][1].map((proglang, index) => {
                                                                if (proglang[`${this.state.allInterests[0][2]}id`] === interest.fav_programming_lang_id){
                                                                    return (
                                                                        <div className="programming-lang" key={index}>
                                                                            <li><a href='#'>{proglang[`${this.state.allInterests[0][2]}name`]}</a></li>
                                                                         </div>
                                                                    )
                                                                }

                                                            })}

                                                            {this.state.allInterests[1][1].map((proglang, index) => {
                                                                if (proglang[`${this.state.allInterests[1][2]}id`] === interest.second_fav_lang_id){
                                                                    return (
                                                                        <li key={index}><a href='#'>{proglang[`${this.state.allInterests[1][2]}name`]}</a></li>
                                                                    )
                                                                }

                                                            })}

                                                            {this.state.allInterests[4][1].map((proglang, index) => {
                                                                if (proglang[`${this.state.allInterests[4][2]}id`] === interest.experience_id){
                                                                    return (
                                                                        <div key={index}className="experience-level">
                                                                            <li><a href='#'>{proglang[`${this.state.allInterests[4][2]}name`]}</a></li>
                                                                         </div>
                                                                    )
                                                                }

                                                            })}
                                                        </ul>

                                                    )
                                                }
                                            })}
                                        </div>

                                        <div className="back">
                                            <div className="flip-padding">
                                                <div>
                                                {this.state.interests.map((interest, index) => {
                                                if (user.id == interest.user_id){
                                                    return (
                                                        <div key ={index}>
                                                            {this.state.allInterests[0][1].map((proglang, index) => {
                                                                if (proglang[`${this.state.allInterests[0][2]}id`] === interest.fav_programming_lang_id){
                                                                    return (
                                                                        <div key={index}>
                                                                            <h5>Primary Language</h5>
                                                                            <p>{proglang[`${this.state.allInterests[0][2]}name`]}</p>
                                                                         </div>
                                                                    )
                                                                }

                                                            })}

                                                            {this.state.allInterests[1][1].map((proglang, index) => {
                                                                if (proglang[`${this.state.allInterests[1][2]}id`] === interest.second_fav_lang_id){
                                                                    return (
                                                                        <div key={index}>
                                                                            <h5>Secondary Language</h5>
                                                                            <p>{proglang[`${this.state.allInterests[1][2]}name`]}</p>
                                                                        </div>
                                                                    )
                                                                }

                                                            })}

                                                            {this.state.allInterests[4][1].map((proglang, index) => {
                                                                if (proglang[`${this.state.allInterests[4][2]}id`] === interest.experience_id ){
                                                                    return (
                                                                        <div key={index}>
                                                                            <h5>Years of Experience</h5>
                                                                            <p>{proglang[`${this.state.allInterests[4][2]}name`]}</p>
                                                                        </div>
                                                                    )
                                                                }

                                                            })}


                                                            {this.state.allInterests[2][1].map((proglang, index) => {
                                                                if (proglang[`${this.state.allInterests[2][2]}id`] === interest.fav_database_system_id){
                                                                    return (
                                                                        <div key={index}>
                                                                            <h5>Database System</h5>
                                                                            <p>{proglang[`${this.state.allInterests[2][2]}name`]}</p>
                                                                        </div>
                                                                
                                                                    )
                                                                }

                                                            })}
                                                             <a href={'/profile/' + user.username }><button className="follow-button">Visit Profile</button></a>
                                                        </div>
                                                    )
                                                }
                                            })}
                                            </div>
                                            <div></div>
                                        </div>
                                    </div>
                                    </div>
                                </div>

                            )
                        })}

                    </div>
                </div>
            </div>


        )
    }
}

export default withRouter(Home)


