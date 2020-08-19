import React, { Component, Fragment} from 'react'
import Navbar from './Components/Navbar'
import Homeboard from './Components/Homeboard'
import Loginform from './Components/Loginform'
import RegisterForm from './Components/RegisterForm'
import InterestForm from './Components/InterestForm'
import Home from './Components/Home'
import Profile from './Components/Profile'
import Logout from './Components/Logout'
import FrontPage from './Containers/FrontPage'
import PrivateRoute from './Components/PrivateRoute'
import Account from './Components/Account'
import ProfileForm from './Components/ProfileForm'
import EditInterestsForm from './Components/EditInterestsForm'
import SendMessageForm from './Components/SendMessageForm'
import Messages from './Components/Messages'
import {check} from './Components/util/login'
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import {withRouter} from "react-router";
import './App.css'

function App() {

  let [login, setLogin] = React.useState(false);

  check().then(r => setLogin(r))

    return (
      <div>
        <Navbar />
        <Router >
          
            <Route exact path='/register' render={props =>
            <Fragment>
              <RegisterForm requestType='post'/>
            </Fragment>} />

            <PrivateRoute path='/home/' isLoggedIn={login} component={withRouter(Home)} />

            <PrivateRoute exact path='/add_interests/' isLoggedIn={login} component={withRouter(InterestForm)} />

            <Route exact path='/account/' >
              {login ? <Account /> : <FrontPage />}
            </Route>

            <Route exact path='/edit_profile/'>
              {login ? <ProfileForm requestType="put"/> : <FrontPage />}
            </Route>

            <Route exact path='/edit_interests/'>
              {login ? <EditInterestsForm /> : <FrontPage/>}
            </Route>

            <Route exact path='/profile/:user/'>
              {login ? <Profile /> : <FrontPage />}
            </Route>

            <Route exact path='/messages/'>
              {login ? <Messages />: <FrontPage/>}
            </Route>

            <Route exact path='/send_message/:user/'>
              {login ? <SendMessageForm /> : <FrontPage />}
            </Route>


            <Route exact path='/logout/' component={withRouter(Logout)}/>

            <Route exact path='/'>
              {login ? <Home /> : <FrontPage/>}
              </Route>
        
        </Router>
      </div>
    )
}


export default App

{/* <Route exact path='/home' render={login ? props => 
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
          
          
          <Route exact path='/add_interests' >
              {login ? <InterestForm requestType="post"/> : <FrontPage />}
            </Route>
          
          */}