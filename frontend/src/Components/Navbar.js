import React, { Component } from 'react'
import axios from 'axios'
import './Navbar.css'

export class Navbar extends Component {
    constructor(props){
        super(props)
        this.state = {
            currentUser: [],
            notifications: [],
            newMessages: 0,
            Messagetext: '',
            visibility: 'hidden',
            currentCount: 10000

        }
        this.setMessageCount = this.setMessageCount.bind(this)
        this.timer = this.timer.bind(this)
    }

    setMessageCount(n){
        if (n==0){
            this.setState({
                Messagetext: n,
                visibility: 'hidden'
            })
        }
        else{
            this.setState({
                Messagetext: n,
                visibility: 'visible'
            })
        }
    }

    timer() {
        var since  = 0;
        const token = localStorage.getItem("token")
        const res = axios.get(`http://localhost:5000/api/notifications?since=${since}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            }
        }).then(res => {
            for (var i=0; i< res.data.notifications.length; i++){
                if (res.data.notifications[i].name == 'unread_message_count'){
                    this.setMessageCount(res.data.notifications[i].payload_json);
                since = res.data.notifications[i].timestamp;
                }
            }
            this.setState({
              currentCount: this.state.currentCount - 1
            })
    
            if(this.state.currentCount < 1) { 
              clearInterval(this.intervalId);
            }
          })
        }
        



    componentDidMount(){
        const token = localStorage.getItem("token")
        const fetchData = async () => {
        const res = await axios.get('http://localhost:5000/api/notifications', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            }
        });

        if (res.data.currentUser){
            this.setState({
                currentUser: res.data.current_user,
                notifications: res.data.notifications,
                newMessages: res.data.new_messages
            })
        }

        this.intervalId = setInterval(this.timer, 1000);
       };
       
       fetchData();
        
    }

    componentWillUnmount(){
        clearInterval(this.intervalId);
      }

    render() {


        return (
            <div>
                <header>
                    <nav className="navbar navbar-expand-md navbar-dark bg-steel">
                    <div className="container">
                        <a className="navbar-brand mr-4" href="/">Developers Connect</a>
                        <div className="collapse navbar-collapse" id="navbarToggle">
                        <div className="navbar-nav mr-auto">
                            <a className="nav-item nav-link" href="/">Home</a>
                        </div>
                        {/* <!-- Navbar Right Side --> */}
                        <div className="navbar-nav">
                            {this.props.isLoggedIn ?
                                <>
                                <a className="nav-item nav-link" href="/account">Account</a>
                                <a className="nav-item nav-link" href="/messages">Messages
                                    <span className="badge"
                                    style={{visibility: this.state.visibility}}>
                                    {this.state.Messagetext}
                                    </span>
                                         
                                </a>
                                <a className="nav-item nav-link" href="/logout">Logout</a>
                                </>
                             :
                             <>
                             <a className="nav-item nav-link" href="/">Login</a>
                             <a className="nav-item nav-link" href="/register">Register</a>
                             </>
                            }
                        </div>
                        </div>
                    </div>
                    </nav>
                </header>
            </div>
        )
    }
}

export default Navbar
