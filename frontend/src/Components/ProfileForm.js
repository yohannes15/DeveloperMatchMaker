import React, { Component } from 'react'
import Axios from 'axios'
import Alert from './Alert'
import {withRouter} from 'react-router-dom'


import './ProfileForm.css'

export class ProfileForm extends Component {
    constructor(props){
        super(props)
        this.state = {
            username: '',
            email: '',
            selectedFile: '',
            err: ''
        }
        this.fileSelectedHandler = this.fileSelectedHandler.bind(this)
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleChange(event){
        const target = event.target
        const name = target.name
        this.setState({
            [name]: target.value
        });
    }

    handleSubmit(event, requestType){
        event.preventDefault()
        const username = event.target.elements.username.value
        const email = event.target.elements.email.value
        const profilepic = this.state.selectedFile
        const token = localStorage.getItem("token")

        const fd = new FormData()
        fd.append("username", username)
        fd.append("email", email)
        if (this.state.selectedFile !== ''){
            fd.append("profilepic", profilepic, profilepic.name)
        }

        if (requestType==='put'){
            Axios.put("http://localhost:5000/api/edit_profile", fd,
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': token
                    }
                }).then(res =>{
                    if (res.data.error){
                        this.setState({ err: res.data.error })
                        console.log(res.data.error)
                    }
                    else {
                        console.log(res.data)
                        this.props.history.push('/account/')
                    }
                    
                })
        }

    }

    fileSelectedHandler(event){
        this.setState({
            selectedFile: event.target.files[0] 
        })
        console.log(event.target.files[0])
    }




    render() {
        console.log(this.state.selectedFile)
        return (
            <div className="container">
                <div className="sc-edprofile">
                    <h1>Edit Profile</h1>
                    <div className="sc-container">
                    {this.state.err.length > 0 && (
                            <Alert
                                message={`Check your form and try again! (${this.state.err})`}
                            />
                        )}
                    <form 
                    onSubmitCapture={(event) => 
                        this.handleSubmit(
                            event, this.props.requestType
                        )}  
                        encType="multipart/form-data"
                    >
                        <div>
                            <div className="form-group">
                                <label>
                                    Username:
                                    <input 
                                        className="form-control form-control-lg"
                                        name="username"
                                        type="text"
                                        value={this.state.username}
                                        onChange={this.handleChange}
                                        required
                                    />
                                    </label>
                            </div>
                            <div className="form-group">
                                <label>
                                    Email
                                    <input 
                                    className="form-control form-control-lg"
                                    name="email"
                                    type="email"
                                    value={this.state.email}
                                    onChange={this.handleChange}
                                    required
                                    />
                                </label>
                            </div>
                            <div className="form-group">
                                <label>
                                    Add Profile Picture
                                    <input 
                                    className="form-control-file"
                                    type="file"
                                    onChange={this.fileSelectedHandler}
                                    />
                                </label>
                            </div>
                        </div>

                        <p><input id="submit" name="submit" type="submit" value="Submit"/></p>
                    </form>
                    </div>
            
                </div>
        </div>
    )
    }
    
}

export default withRouter(ProfileForm)
