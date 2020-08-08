// src/login.js
import Axios from "axios";

async function login(email, password) {
    const res = await Axios.post("http://localhost:5000/api/login", 
    {email: email, password: password});
    const {data} = await res;
    console.log(data)
    if (data.error) {
        return data.error
    } else {
        localStorage.setItem("token", data.token);
        return true
    }
}

function check() {
    if (localStorage.getItem("token")) {
        return true;
    } else {
        return false;
    }
}

export {check, login};