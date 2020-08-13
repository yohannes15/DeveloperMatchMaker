from flask import Flask, request, jsonify
from matcher import app

if __name__ == "__main__":
    app.run(debug=True)