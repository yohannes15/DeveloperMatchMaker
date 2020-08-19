import React, { Component } from 'react'
import axios from 'axios'
import './Messages.css'

export class Messages extends Component {
    constructor(props){
        super(props)
        this.state = {
            err: '',
            messages: '',
            nextUrl: '',
            prevUrl: ''
        }
    }
    componentDidMount(){
        const token = localStorage.getItem("token")
        axios.get('http://localhost:5000/api/messages', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            }
        }).then(res => {
            if (res.data.error){
                console.log(res.data.error)
            }
            else {
                this.setState({
                    messages: res.data.messages,
                    nextUrl: res.data.next_url,
                    prevUrl: res.data.prev_url
                })
                console.log(res.data.messages[0])
            }
        });

    }
    render() {
        return (
            <div className="container">
            <h1 style={{marginBottom: '10px', textAlign: 'center'}}>All Messages</h1>
            <div className="container">
                <table className="table table-hover">
                    <tbody>
                    <tr>
                        <td width="145px" height="145px">
                            <a href="#" >
                                
                                <h6 >AlexBayBay</h6>
                            </a>
                            
                        </td>
                        <td>
                            
                                <span className="user_popup">
                                    <a href="{{ url_for('profile', user=post.sender.username) }}">
                                        AlexBayBay
                                    </a>
                                </span>
                            

                            <span id="post{{ post.id }}">This is the message</span>
                            <br></br>
                            {/* <span id="translation{{ post.id }}">
                                <a href="javascript:translate(
                                            '#post{{ post.id }}',
                                            '#translation{{ post.id }}',
                                            '{{ post.language }}',
                                            '{{ g.locale }}');"></a>
                            </span> */}
                            <form action="/send_message/{{post.sender.username}}" method="POST">
                                <button className="btn btn-default match-button" name="match_profile" type="submit" value="{{post.sender.username}}">
                                Reply
                                </button>
                            </form>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
                
                {/* ------------------------ */}
            
                <div className="row">
                    <div className="col-sm-3">
                        <div className="button-area">
                            <a href="{{ prev_url or '#' }}">
                
                                <i className="fa fa-arrow-left"></i>
                                <span>Older Messages</span>
                            </a>    
                        </div>
                    </div>
                    <div className="col-sm-6"></div>
                    <div className="col-sm-3">
                        <div className="button-area">
                            <a href="{{ next_url or '#' }}">
                                <span>Newer Messages</span>
                                <i className="fa fa-arrow-right"></i>
                            </a>    
                        </div>
                    </div>
                   
                </div>
        </div>  
        )
    }
}

export default Messages
