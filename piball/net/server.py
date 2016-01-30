from flask import Flask , render_template ,session
import uuid
import flask.ext.login as flask_login
from flask_socketio import SocketIO ,join_room, leave_room
import json
import pickle
import time
from flask import request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!d'

socketio = SocketIO(app ,  async_mode = "threading");



class Game:

    def  tojson(self):
        json = {}
        json["score"] = self.score
        json["playing"] =  self.playing
        json["user"] = self.user
        return json

    def startGame(self , user):
        self.score = 0
        self.playing = 1
        self.user = user

    def endGame(self):
        self.playing = 0
        self.user = -1

    def finishGame(self):
        self.playing = 0

    def addScore(self, score):
        self.score += score

    def setScore(self, score):
        self.score = score


    def subtrackScore(self , score):
        self.score -= score

    def __init__(self ):
        self.score = 0
        self.playing = 0
        self.user = -1



@app.route("/")
def index():
    return render_template('index.html')


@socketio.on('gameInput')
def handle_message(data):
    global currentGame
    if( currentGame.user == session['id'] ):
        print("Trigger pressed " +  str(data['control']) + str(session['id']))


def notifyWait():
    global currentGame
    data = {'id' : 0 }
    socketio.emit('gameUpdate' , data  , room = 'wait' )

def notifyPlayers():
    global currentGame
    print("New game!")
    socketio.emit('currentGame' , currentGame.tojson()  , room = 'play' )

def notifyReady():
    global currentGame
    data = { 'id' : 2 }
    socketio.emit('gameUpdate' , data  , room = 'ready' )



@socketio.on('play')
def handle_game():
    print("Play")
    global currentGame
    if currentGame.playing == 0 :
        leave_room('ready')
        join_room('play')
        startWait()
        currentGame.startGame(session['id'])
        notifyPlayers()

@socketio.on('finishGame')
def handle_test():
    socketio.emit('endCurrentGame' , currentGame.tojson() , room='play');


@socketio.on('endGame')
def handle_end():
    global currentGame
    if currentGame.playing == 1:
        currentGame.endGame()
        leave_room('play')
        join_room('ready')
        stopWait()

def update_game():
    global currentGame
    socketio.emit('gameUpdate' , currentGame.tojson() , room='play')

def startWait():
    print("everyone start waiting")
    socketio.emit('startWaiting', room='ready')

def stopWait():
    socketio.emit('stopWaiting' , room='wait')

@socketio.on('startWait')
def handle_start():
    leave_room('ready')
    join_room('wait')
    notifyWait()


@socketio.on('stopWait')
def handle_start():
    leave_room('wait')
    join_room('ready')
    notifyReady()

@socketio.on('disconnect' )
def handle_disconect():

    if session['id'] == currentGame.user: #Player disconnected
        currentGame.endGame()
        stopWait()



@socketio.on('connect')
def handle_connection():
    print('Connect')
    print('  ')
    print('  ')
    print('  ')

    if currentGame.playing == 1:
        join_room('wait')
        notifyWait()
    else:
        join_room('ready')
        notifyReady()

    session['id'] = str(uuid.uuid4())




currentGame = Game()





if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=80  )