import React, { Component } from 'react'
import Alert from './Alert'
import axios from "axios";
import {login} from './util/login'
import './Loginform.css'



export class Loginform extends Component {
    constructor(props){
        super(props)
        this.state = {
            email: '',
            password: '',
            err: ''
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
        const email = event.target.elements.email.value
        const password = event.target.elements.password.value
        if (requestType == 'post'){

            login(email, password).then(
                res => {
                    if (res === true){
                        window.location = '/home'
                        console.log(this.state.login)
                    }
                    else{
                        this.setState({err: res})
                        console.log(this.state.err)
                    }

                }
            )
            // axios.post('http://127.0.0.1:5000/api/login', {
            //     email: email,
            //     password: password,
            // })
            // .then((res) => {
            //     console.log(res.data)
            // });
       
        }
    };

    render() {
        return (
        <div className="wrapper">
            <section className="touts">

                <section className="tout">
                    <header>
                        <h3>Create a Profile</h3>
                    </header>
                    <p>Are you a Developer? Designer? or are you just getting into computer science and software engineering. Join and you might find others in the same boat as you. Put yourself out there so that others at SJU can find you!</p>
                    <a className="indexbutton" href="">Sign Up Now</a>
                </section>

                <section className="tout">
                    <header>
                        <h3>Find a Developer At SJU to Work With</h3>
                    </header>
                    <p>Looking for the right-minded developer to work with on the next big thing? or looking for a developer with your skill level to collab a project with and expand your skills. Look no further.</p>
                    <a className="indexbutton" href="">Sign Up To See Developers At SJU</a>
                </section>

                <section className="tout">
                    {this.state.err.length > 0 && (
                            <Alert
                                message={`Check your form and try again! (${this.state.err})`}
                            />
                        )}
                    <form 
                        onSubmitCapture={(event) => this.handleSubmit(
                            event, this.props.requestType
                        )} 
                        >
                        <fieldset className="form-group" style={{marginBottom: '-2px'}}>
                        <legend className="border-bottom mb-4">Log In</legend>
                        <div className="form-group">
                            <label>
                                Email:
                                <input 
                                    className="form-control form-control-lg"
                                    name="email"
                                    type="text"
                                    value={this.state.email}
                                    onChange={this.handleChange}
                                    required
                                />
                                </label>
                            </div>
                        <div className="form-group">
                            <label>
                                Password
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
                        </fieldset>    

                        <div>
                            <button className="btn btn-outline-info" type="primary" htmltype="submit">
                                Login
                            </button>
                            <br></br>
                            {this.state.login && "You're logged in!"}
                        </div>

                        <small className="text-muted ml-2">
                            <a href="#">Forgot Password?</a>
                        </small>
                    </form>

                </section>
            </section>
        </div>
        )
    }
}

export default Loginform
