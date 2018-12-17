import datetime as dt
import os
import zipfile
from threading import Thread

from step_motor_manager import StepMotorManager

from flask import Flask, request, send_file
from flask import jsonify
from flask_cors import CORS

from scipy.io.wavfile import read

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "/uploads"
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), "uploads")

SOUNDS_FOLDER = os.path.join(os.path.dirname(__file__), "static", "sounds")
LOGS_FILE_DIR = os.path.join(os.path.dirname(__file__), "logs/parrot-screaming-data.csv")

file_names = []
manager = StepMotorManager()

for root, dirs, files in os.walk(SOUNDS_FOLDER):
    for file in files:
        file_names.append(file)

@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/sounds/<sound_name>", methods=["GET"])
def get_sound(sound_name):
    return send_file("static/sounds/" + sound_name)


@app.route("/upload_file", methods=['POST'])
def upload_file():
    file = request.files['audio_data']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], "audio.wav"))

    sample_rate, audio = read(app.config['UPLOAD_FOLDER'] + "/audio.wav")
    if audio.ndim == 2: # we need to convert the stereo audio to mono
        audio = audio[:, 0]

    result = is_parrot_screaming(audio, sample_rate)
    if result:
       return  manager.onParrotScream()
    
    #print("Is parrot screaming: ", result)
    return jsonify(is_parrot_screaming=result)


@app.route("/soundNames", methods=["GET"])
def get_all_sounds():
    return jsonify(file_names)



def is_parrot_screaming(audio, sample_rate):
    min_number_of_screams = 3
    if audio.shape[0] == 0:
        return
    min_peak_val = 12000
    focus_size = int(0.23 * sample_rate)

    # find all sound chunk ranges
    ranges = {}
    ranges[0] = focus_size
    last_end_range = focus_size
    while True:
        range_start = last_end_range
        range_end = last_end_range + focus_size
        last_end_range = range_end
        
        ranges[range_start] = range_end
        if range_end >= audio.shape[0]: # out of bounds of the array
            range_end = audio.shape[0]
            ranges[range_start] = range_end
            break
    
    # split into n arrays
    audio_chunks = []
    for start, end in ranges.items():
        audio_chunks.append(audio[start: end])
    
    screaming_sequence = []
    for np_arr in audio_chunks:
        if np_arr.max() >= min_peak_val:
            screaming_sequence.append(True)
        else:
            screaming_sequence.append(False)
    
    seq_scream_counter = 0
    for is_screaming in screaming_sequence:
        if is_screaming:
            seq_scream_counter+=1
            if seq_scream_counter >= min_number_of_screams:
                return True
        else:
            seq_scream_counter = 0
    
    return seq_scream_counter >= min_number_of_screams



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5005)

