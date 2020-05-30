from flask import Flask

app = Flask(__name__)

import Route.TheaterRoute
import  Route.UserRoute

if __name__ == "__main__":
    app.run(debug=True)
