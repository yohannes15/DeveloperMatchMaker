import React, { Component } from 'react'
import Axios from 'axios'
import './Account.css'
import {withRouter} from 'react-router-dom'


export class Account extends Component {
    constructor(props){
        super(props)
        this.state = {
            selectedInterests : [],
            currentUser : []
        }
    }

    componentDidMount(){
        const token = localStorage.getItem("token")

        Axios.get("http://localhost:5000/api/get_account_details", {
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
                    selectedInterests: res.data.selected_interests,
                    currentUser: res.data.current_user
                })
                console.log(res.data.selectedInterests)
                console.log(res.data.current_user)
            }
        })

    }
    render() {
        return (
            <div className="pfl-wrapper">
                <article>
                    <div className="profile-photo">
                        <img src={`${process.env.PUBLIC_URL}/assets/images/${this.state.currentUser.image_file}`} width="130" height="130"/>
                    </div>
                    <div className="profile-info">
                        <h1>{this.state.currentUser.firstname} {this.state.currentUser.lastname}</h1>
                        <p>Username : {this.state.currentUser.username}</p>
                        <p style={{lineHeight: '0em'}} >Email: {this.state.currentUser.email}</p>

                    </div>
                    <div className="col-xs-12">
                        <div className="col-md-2 people"></div>
                            <div className="col-md-8 posts">
                                <div className="col-xs-12 col-lg-12 col-xl-6 tile">
                                    <div className="inner">
                                        <h4>Primary Programming Languages</h4>
                                            <h5>{this.state.selectedInterests[0]} and {this.state.selectedInterests[1]}</h5>
                                    </div>
                                </div>
                                <div className="col-xs-12 col-lg-12 col-xl-6 tile">
                                    <div className="inner">
                                        <h4>Database Knowledge</h4>
                                        <h5>{this.state.selectedInterests[2]}</h5>
                                    </div>
                                </div>
                                <div className="col-xs-12 col-lg-12 col-xl-6 tile">
                                    <div className="inner">
                                        <h4>Primary Database Management System</h4>
                                        <h5>{this.state.selectedInterests[3]}</h5>
                                    </div>
                                </div>
                                <div className="col-xs-12 col-lg-12 col-xl-6 tile">
                                    <div className="inner">
                                        <h4>Current Field of Interest</h4>
                                        <h5>{this.state.selectedInterests[4]}</h5>
                                    </div>
                                </div>
                                <div className="col-xs-12 col-lg-12 col-xl-6 tile">
                                    <div className="inner">
                                        <h4>Experience Level</h4>
                                        <h5>{this.state.selectedInterests[6]}</h5>
                                    </div>
                                </div>
                                <div className="col-xs-12 col-lg-12 col-xl-6 tile">
                                    <div className="inner">
                                        <h4>Type of Programmer</h4>
                                        <h5>{this.state.selectedInterests[5]}</h5>
                                    </div>
                                </div>
                            </div>
                        </div>
                </article>

                <div className="border-top pt-8">
                    <div className="text-muted">
                    <a className="ml-2" href="/edit_profile/">Edit Account</a>
                    <a className="ml-2" href="/edit_interests/">Edit Profile</a>
                    </div>
                </div>
            </div>
        )
    }
}

export default withRouter(Account)
