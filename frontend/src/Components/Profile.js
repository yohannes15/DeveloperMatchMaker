import React, { Component } from 'react'
import Axios from 'axios'
import './Profile.css'
import {withRouter} from 'react-router-dom'


export class Profile extends Component {
    constructor(props){
        super(props)
        this.state = {
            selectedUser : [],
            selectedInterests: []
        }
    }

    componentDidMount(){
        const {user} = this.props.match.params
        const token = localStorage.getItem("token")

        Axios.get(`http://localhost:5000/api/get_selected_user/${user}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            }
        }).then(res => {
            if (res.data.error){
                console.log(res.data.error)
            }
            else{
                this.setState({
                    selectedUser: res.data.selected_user,
                    selectedInterests: res.data.selected_interests,
                })
                console.log(res.data.selected_user)
                console.log(res.data.selected_interests)
            }
        })

    }
    render() {
        return (
            <div className="pfl-wrapper">
                <article>
                    <div className="profile-photo">
                        <img src="#" width="200" height="130"/>
                    </div>
                    <div className="profile-info">
                        <h1>selected_user.firstname,selected_user.lastname</h1>
                        <h5>current_user.email</h5>
                    </div>
                    <div className="col-xs-12">
                        <div className="col-md-2 people"></div>
                            <div className="col-md-8 posts">
                                <div className="col-xs-12 col-lg-12 col-xl-6 tile">
                                    <div className="inner">
                                        <h4>Primary Programming Languages</h4>
                                        <h5>selected_interests[0] and elected_interests[1]</h5>
                                    </div>
                                </div>
                                <div className="col-xs-12 col-lg-12 col-xl-6 tile">
                                    <div className="inner">
                                        <h4>Database Knowledge</h4>
                                        <h5>selected_interests[2]</h5>
                                    </div>
                                </div>
                                <div className="col-xs-12 col-lg-12 col-xl-6 tile">
                                    <div className="inner">
                                        <h4>Primary Database Management System</h4>
                                        <h5>selected_interests[3]</h5>
                                    </div>
                                </div>
                                <div className="col-xs-12 col-lg-12 col-xl-6 tile">
                                    <div className="inner">
                                        <h4>Current Field of Interest</h4>
                                        <h5>selected_interests[4]</h5>
                                    </div>
                                </div>
                                <div className="col-xs-12 col-lg-12 col-xl-6 tile">
                                    <div className="inner">
                                        <h4>Experience Level</h4>
                                        <h5>selected_interests[6]</h5>
                                    </div>
                                </div>
                                <div className="col-xs-12 col-lg-12 col-xl-6 tile">
                                    <div className="inner">
                                        <h4>Type of Programmer</h4>
                                        <h5>selected_interests[5]</h5>
                                    </div>
                                </div>
                            </div>
                        </div>
                </article>

                <div style={{textAlign: 'center'}}>
                    <form action="#" method="POST">
                        <button className="buttonz" name="send_message" type="submit" style={{textAlign: 'center'}}>
                        Send A Quick Message
                        </button>
                    </form>
                </div>
                
            </div>
        )
    }
}

export default withRouter(Profile)
