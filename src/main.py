from flask import Flask
from resources import api
def create_app():
    app=Flask(__name__)
    api.init_app(app)


if __name__=='__main__':
    app.run(debug=True)




