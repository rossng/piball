import time, sched , queue , uuid

from piball.control.output import PiballOutputHandler
from piball.game.event_processor import PiballEventProcessor
from piball.game.piball import PiballGame
from piball.control.input import PiballInputHandler
from piball.net import create_app , socketio
from flask_socketio import SocketIO ,join_room, leave_room
from flask import Flask , render_template ,session , request
from piball.control.piballevent import PiballEvent

output_pins = {
    'flipper_left': 16,
    'flipper_right': 18,
    'winding_motor': 12,  # PWM
    'plunger_pin': 22,
    'mbed_tx': 8,  # UART Tx
    'mbed_rx': 10  # UART Rx
}

input_pins = {
    'flipper_left_button': 11,
    'flipper_right_button': 13,
    'bumper_1': 29,
    'bumper_2': 31,
    'bumper_3': 33,
    'fail': 15,
    'plunger_button': 24
}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!d'
socketio = SocketIO(app ,  async_mode = "threading");

@app.route("/")
def index():
    return render_template('index.html')


@socketio.on('gameInput')
def handle_message(data):

    if( currentGame.user == session['id'] ):
        if data['control'] == 'left' :
            event_queue.put(PiballEvent.left_flipper_button_on)
        else:
            event_queue.put(PiballEvent.right_flipper_button_on)

        print('Input '+data['control'])

@socketio.on('play')
def handle_game():
    print("Play")
    if currentGame.playing == 0 :
        leave_room('ready')
        join_room('play')
        start_wait()
        currentGame.start_game(session['id'])
        notify_players()

@socketio.on('finishGame')
def handle_test():
    socketio.emit('endCurrentGame' , currentGame.tojson() , room='play');


@socketio.on('endGame')
def handle_end():
    if currentGame.playing == 1:
        currentGame.reset()
        leave_room('play')
        join_room('ready')
        stop_wait()

@socketio.on('startWait')
def handle_start():
    leave_room('ready')
    join_room('wait')
    notify_wait()


@socketio.on('stopWait')
def handle_start():
    leave_room('wait')
    join_room('ready')
    notifyReady()

@socketio.on('disconnect' )
def handle_disconect():

    if session['id'] == currentGame.user: #Player disconnected
        currentGame.reset()
        stop_wait()


@socketio.on('connect')
def handle_connection():
    if currentGame.playing == 1:
        join_room('wait')
        notify_wait()
    else:
        join_room('ready')
        notifyReady()

    session['id'] = str(uuid.uuid4())


def update_game():
    socketio.emit('gameUpdate' , currentGame.tojson() , room='play')

def start_wait():
    print("everyone start waiting")
    socketio.emit('startWaiting', room='ready')

def stop_wait():
    socketio.emit('stopWaiting' , room='wait')


def notify_wait():
    data = {'id' : 0 }
    socketio.emit('gameUpdate' , data  , room = 'wait' )

def notify_players():
    print("update game!")
    socketio.emit('currentGame' , currentGame.tojson()  , room = 'play' )

def notifyReady():
    global currentGame
    data = { 'id' : 2 }
    socketio.emit('gameUpdate' , data  , room = 'ready' )



event_queue = queue.Queue()
action_scheduler = sched.scheduler(time.time, time.sleep)
output_handler = PiballOutputHandler(output_pins)
currentGame = PiballGame(output_handler, socketio)
event_processor = PiballEventProcessor(event_queue, action_scheduler, currentGame, output_handler)
input_handler = PiballInputHandler(event_queue, input_pins)


event_processor.start()

print('socketio')

socketio.run(app, host='0.0.0.0', port=80   )

event_processor.join()







