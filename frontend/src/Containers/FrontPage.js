import React, { Component } from 'react'
import HomeBoard from '../Components/Homeboard'
import Loginform from '../Components/Loginform'
import {check} from '../Components/util/login'

export class FrontPage extends Component {
    render() {
        return (
            <div className="container">
                <HomeBoard />
                <Loginform requestType="post" />
            </div>
        )
    }
}

export default FrontPage
