import React, { Component, Fragment} from 'react'
import Navbar from './Components/Navbar'
import Homeboard from './Components/Homeboard'
import Loginform from './Components/Loginform'
import RegisterForm from './Components/RegisterForm'
import Home from './Components/Home'
import {check} from './Components/util/login'
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import './App.css'

export class App extends Component {
  constructor(props){
    super(props)
    this.state = {
      loggedin: check()
    }
  }
  render() {
    return (
      <div>
        <Navbar />
        <Router >
            <Route exact path='/register' render={props =>
            <Fragment>
              <RegisterForm requestType='post'/>
            </Fragment>} />

            <Route exact path='/home' render={check() ? props => 
            <Fragment>
              <Home />
            </Fragment> 
            : props =>
            <Fragment>
            <div className="container">
              <Homeboard />
              <Loginform requestType='post'/>
              </div>
            </Fragment>
            
            } />



            <Route exact path='/' render={check() 
            ? props => 
            <Fragment>
              <Home />
            </Fragment> 
            : props =>
            <Fragment>
            <div className="container">

              <Homeboard />
              <Loginform requestType='post'/>
            </div>
            </Fragment>} />

          {/* <Homeboard exact path='/'/>
          <Loginform requestType='post'/> */}
        
        </Router>
      </div>
    )
  }
}

export default App

