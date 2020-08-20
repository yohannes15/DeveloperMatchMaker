import React, { Component } from 'react'
import axios from 'axios'
import Pagination from './Pagination'
import './Messages.css'

export class Messages extends Component {
    constructor(props){
        super(props)
        this.state = {
            err: '',
            messages: [],
            loading: false,
            currentPage: 1,
            messagesPerPage: 5,
            usersStack: []
        }
        this.paginate = this.paginate.bind(this)
    }
    componentDidMount(){
        const token = localStorage.getItem("token")
        const fetchPosts = async () => {
            this.setState({
                loading: true
            })
            const res = await axios.get('http://localhost:5000/api/messages', {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token
                }
            });
            if (res.data.messages){
                this.setState({
                    messages: res.data.messages,
                    loading: false,
                    usersStack: res.data.users_stack
                })
                console.log(res.data.users_stack)
            }
        }

        fetchPosts()


    }

    paginate(pageNumber){
        console.log("paginate", pageNumber)
        this.setState({
            currentPage: pageNumber
        })
    }

    render() {

        const indexOfLastMessage = this.state.currentPage * this.state.messagesPerPage;
        const indexOfFirstMessage = indexOfLastMessage - this.state.messagesPerPage;
        const currentMessages = this.state.messages.slice(indexOfFirstMessage, indexOfLastMessage);

   

        if (this.state.loading){
            return <h2>Loading...</h2>
        }

        return (
            <div className="container">
            <h1 style={{marginBottom: '10px', textAlign: 'center'}}>All Messages</h1>
            {this.state.messages.map(message => {
                return (
                    <div className="container" key={message.id}>
                    <table className="table table-hover">
                        <tbody>
                        <tr>
                            <td width="145px" height="145px">
                                <a href="" >
                                    {/* <img src="#"/> */}
                                    {this.state.usersStack.map((user, index) => {
                                        if (user.id === message.sender_id){
                                            return (
                                                <div key={user.id}>
                                                <img src={`${process.env.PUBLIC_URL}/assets/images/${user.image_file}`} width="90px" height="91px"/>
                                                <h6>{user.username}</h6>
                                                </div>
                                            )
                                        }

                                    })}

                                        
                                </a>
                                
                            </td>
                            <td>
                                <span id="post{{ post.id }}">{message.body}</span>
                                <br></br>

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
                )
            })}

                
                {/* ------------------------ */}
            
                <Pagination
                    postsPerPage={this.state.messagesPerPage}
                    totalPosts={this.state.messages.length}
                    paginate={this.paginate}
                 />
        </div>  
        )
    }
}

export default Messages
        // axios.get('http://localhost:5000/api/messages', {
        //     headers: {
        //         'Content-Type': 'application/json',
        //         'Authorization': token
        //     }
        // }).then(res => {
        //     if (res.data.error){
        //         console.log(res.data.error)
        //     }
        //     else {
        //         this.setState({
        //             messages: res.data.messages
        //         })
        //         console.log(res.data.messages)
        //     }
        // });
