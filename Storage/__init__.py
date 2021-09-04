from flask import Flask
from . import Login
from . import MiniFace

app = Flask(__name__)

app.register_blueprint(Login.Login_Blueprint)
app.register_blueprint(MiniFace.MiniFace_Blueprint)