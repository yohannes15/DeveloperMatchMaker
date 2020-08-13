import React, { Component, Fragment} from 'react'
import Navbar from './Components/Navbar'
import Homeboard from './Components/Homeboard'
import Loginform from './Components/Loginform'
import RegisterForm from './Components/RegisterForm'
import InterestForm from './Components/InterestForm'
import Home from './Components/Home'
import Logout from './Components/Logout'
import FrontPage from './Containers/FrontPage'
import PrivateRoute from './Components/PrivateRoute'

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

            {/* <PrivateRoute exact path='/:user/' isLoggedIn={login} component={withRouter(""} /> */}


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