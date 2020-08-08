import React from "react";

function Alert(props) {
    return (
        <div
            className="fade alert alert-danger show"
            >
            {props.message}
        </div>
    );
}

export default Alert;