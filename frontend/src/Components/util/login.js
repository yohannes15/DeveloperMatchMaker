// src/login.js
import Axios from "axios";

async function login(email, password) {
    const res = await Axios.post("http://localhost:5000/api/login", {email, password});
    const {data} = await res;
    if (data.error) {
        return data.error
    } else {
        localStorage.setItem("token", data.token);
        localStorage.setItem("refreshToken", data.refreshToken);
        return true
    }
}

async function check() {
    const token = localStorage.getItem("token")
    try {
        const res = await Axios.post("http://localhost:5000/api/checkiftokenexpire", {}, {
            headers: {
                Authorization: token
            }
        })
        const {data} = await res;
        return data.success
    } catch {
        console.log("p")
        const refresh_token = localStorage.getItem("refreshToken")
        if (!refresh_token) {
            localStorage.removeItem("token")
            return false;
        }
        Axios.post("http://localhost:5000/api/refreshtoken", {}, {
            headers: {
                Authorization: `${refresh_token}`
            }
        }).then(res => {
            localStorage.setItem("token", res.data.token)
        })
        return true;
    }
}

function logout() {
    if (localStorage.getItem("token")) {
        const token = localStorage.getItem("token")
        Axios.post("http://localhost:5000/api/logout/access", {}, {
            headers: {
                Authorization: `${token}`
            }
        }).then(res => {
            if (res.data.error) {
                console.error(res.data.error)
            } else {
                localStorage.removeItem("token")
            }
        })
    }
    if (localStorage.getItem("refreshToken")) {
        const refreshToken = localStorage.getItem("refreshToken")
        Axios.post("http://localhost:5000/api/logout/refresh", {}, {
            headers: {
                Authorization: `${refreshToken}`
            }
        }).then(res => {
            if (res.data.error) {
                console.error(res.data.error)
            } else {
                localStorage.removeItem("refreshToken")
            }
        })
    }
    localStorage.clear();
    setTimeout(() => window.location = "/", 500)
}

export {login, check, logout};
