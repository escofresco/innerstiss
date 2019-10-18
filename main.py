from app import app, socketio
from views import *

if __name__ == "__main__":
    #app.run()
    socketio.run(app)
