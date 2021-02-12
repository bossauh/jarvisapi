from flask import jsonify
from difflib import SequenceMatcher
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

import os
import json
import string
import time
import threading
import nltk
import random

def setOtherVolumes(value):

    def smooth(volume):
        current = volume.GetMasterVolume()

        while True:
            if value < current:
                current -= 0.05
                if current > value:
                    volume.SetMasterVolume(current, None)
                    time.sleep(0.003)
                else:
                    break
            else:
                current += 0.05
                if current < value:
                    volume.SetMasterVolume(current, None)
                    time.sleep(0.003)
                else:
                    break

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and not session.Process.name() == "python.exe":
            threading.Thread(target=smooth, args=(volume,), daemon=True).start()

def get_tags(text, tags):
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)

    meet_tags = [word for word, tag in tagged if tag in tags]
    return meet_tags

def remove_tags(text, tags):
    to_remove = get_tags(text, tags)
    removed = ' '.join([x for x in text.split(" ") if not x in to_remove])
    return removed

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def current_path(path):
    paths = path.split("/")
    return os.path.join(os.getcwd(), *paths)

def readJson(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def readFile(path, split=False):
    with open(path, "r") as f:
        if split:
            return f.read().splitlines()
        return f.read()

def writeJson(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def config():
    with open(current_path("data/config.json")) as f:
        return json.load(f)

def id_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def make_response(data, code=200, message_status=""):
    data = {
        "status": code,
        "timestamp": int(time.time()),
        "message_status": message_status,
        "data": data
    }

    return jsonify(data), code
