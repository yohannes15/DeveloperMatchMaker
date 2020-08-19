import React, { Component } from 'react'
import Alert from './Alert'
import axios from 'axios'
import './SendMessageForm.css'
import {withRouter} from 'react-router-dom'

const heightAndFontSize = {
    height: 'fit-content',
    fontSize: '14px'
}

export class SendMessageForm extends Component {
    constructor(props){
        super(props)
        this.state = {
            err: '',
            message: ''
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

    handleSubmit(event){
        event.preventDefault()
        const {user} = this.props.match.params
        const token = localStorage.getItem('token')
        const message = event.target.elements.message.value

        axios.post(`http://127.0.0.1:5000/api/send_message/${user}`, {
            message: message,
        },
        {
            headers: {
                'Authorization': token
            }
        })
        .then((res) => {
            if (res.data.error){
                console.log(res.data.error)
            }
            else{
                this.props.history.push(`/profile/${user}`)
                console.log(res.data.success)
            }
        });

    }

    render() {
        return (
            <div className="container">
                <section className="contact">
                    <h1 className="section-header">Send A Message to Yohannes Berhane</h1>
                        <div className="contact-wrapper">
                            <div className="column">
                            {this.state.err.length > 0 && (
                            <Alert
                                message={`Check your form and try again! (${this.state.err})`}
                            />
                            )}
                            <form 
                             onSubmitCapture={(event) => this.handleSubmit(
                                event
                            )} 
                            className="form-horizontal" 
                            encType="multipart/form-data">
                                <div style={heightAndFontSize} className="form-controls">
                                <div style={{width: '600px'}}>
                                <label>
                                    Message
                                    <textarea
                                        className="textArea"
                                        name="message"
                                        type="text"
                                        value={this.state.message}
                                        onChange={this.handleChange}
                                        required
                                    />
                                </label>
                                    

                                <div style={{textAlign: 'center'}}>
                                    <input id="submit" name="submit" type="submit" value="Submit"/>
                                </div>
                                </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </section>
            </div>
        )
    }
}

export default withRouter(SendMessageForm)
