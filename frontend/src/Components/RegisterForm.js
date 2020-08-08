import React, { Component } from 'react'
import axios from 'axios'
import Alert from './Alert'
import './RegisterForm.css'

export class RegisterForm extends Component {
    constructor(props){
        super(props)
        this.state = {
            firstname: '',
            lastname: '',
            username: '',
            email: '',
            password: '',
            confirmpassword: '',
            dateofbirth: '',
            err: '',
        }
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleChange = (event) => {
        const target = event.target
        const name = target.name
        this.setState({
            [name]: target.value
        });
    }

    handleSubmit = (event, requestType) => {
        event.preventDefault()
        const firstname = event.target.elements.firstname.value
        const lastname = event.target.elements.lastname.value
        const username = event.target.elements.username.value
        const email = event.target.elements.email.value
        const password = event.target.elements.password.value
        const confirmpassword = event.target.elements.confirmpassword.value
        const dateofbirth = event.target.elements.dateofbirth.value

        if (password != confirmpassword){
            this.setState({err: "Passwords don't match"})
        }
        else{
            axios.post('http://127.0.0.1:5000/api/register', {
                firstname: firstname,
                lastname: lastname,
                username: username,
                email: email,
                password: password,
                confirmpassword: confirmpassword,
                dateofbirth: dateofbirth,
            })
            .then((res) => {
                if (res.data.error) {
                    this.setState({ err: res.data.error });
                } else {
                    window.location = '/'
                }
            });
    }
}   

    render() {
        return (
            <div className="content-section">
                    <form 
                    onSubmitCapture={(event) => this.handleSubmit(
                        event, this.props.requestType
                    )} 
                    >
                    <fieldset className="form-group" style={{marginBottom: '-2px'}}>
                    {this.state.err.length > 0 && (
                        <Alert
                            message={`Check your form and try again! (${this.state.err})`}
                        />
                    )}
                    <legend className="mb-4">Join Today</legend>
                    <div className="form-group">
                        <label>
                            First Name:
                            <input 
                                className="form-control form-control-lg prop-label"
                                name="firstname"
                                type="text"
                                value={this.state.firstname}
                                onChange={this.handleChange}
                                required
                            />
                            </label>
                        </div>
                    <div className="form-group">
                        <label>
                            Last Name:
                            <input 
                            className="form-control form-control-lg"
                            name="lastname"
                            type="text"
                            value={this.state.lastname}
                            onChange={this.handleChange}
                            required
                            />
                        </label>
                    </div>
                    <div className="form-group">
                        <label>
                            Email:
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
                            Password:
                            <input 
                            className="form-control form-control-lg"
                            name="password"
                            type="text"
                            value={this.state.password}
                            onChange={this.handleChange}
                            required
                            />
                        </label>
                    </div>
                    <div className="form-group">
                        <label>
                            Confirm Password:
                            <input 
                            className="form-control form-control-lg"
                            name="confirmpassword"
                            type="text"
                            value={this.state.confirmpassword}
                            onChange={this.handleChange}
                            required
                            />
                        </label>
                    </div>
                    <div className="form-group">
                        <label>
                            Date of Birth:
                            <input 
                            className="form-control form-control-lg"
                            name="dateofbirth"
                            type="text"
                            value={this.state.dateofbirth}
                            onChange={this.handleChange}
                            required
                            />
                        </label>
                    </div>
                    </fieldset>    

                    <div>
                        <button className="btn btn-outline-info" type="primary" htmltype="submit">
                            Login
                        </button>
                    </div>

                    <small className="text-muted ml-2">
                        <a href="#">Forgot Password?</a>
                    </small>
                </form>

                

            <div className="border-top pt-3">
            <small className="text-muted">
                Already Have An Account? <a className="ml-2" href="">Sign In</a>
            </small>
            </div>

        </div>
        )
    }
}

export default RegisterForm
