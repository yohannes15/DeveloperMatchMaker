import React from "react";
import {logout} from "./util/login"

class Logout extends React.Component {
    componentDidMount() {
        logout()
    }

    render() {
        return (
            <div className="container">
                <h2>Please wait, logging you out...</h2>
            </div>
        )
    }
}

export default Logout;