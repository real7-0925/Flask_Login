#login main

from flask import Flask, Blueprint
import os
from dotenv import load_dotenv

from app import create_app

app = create_app('testing')

if __name__ == "__main__":
    app.run(debug=True)