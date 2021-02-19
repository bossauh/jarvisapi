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
import datetime

class Resources:
    days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ]

    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december"
    ]

    day_indicators = {
        "later": 0,
        "today": 0,
        "tomorrow": 1,
        "next day": 2
    }

class Helpers:
    def get_time_or_date(self, text):
        text = text.lower()

        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        
        time_strings = []
        time_string = ""
        p = ""

        for txt, tag in tagged:
            if tag == "CD":
                if ":" in txt:
                    time_strings.append(txt)

            if txt in ['a.m.', 'a.m', 'p.m.', 'p.m']:
                p = txt
        
        if time_strings:
            if len(time_strings) > 1:
                if time_strings[0].endswith("0"):
                    first_part = time_strings[1].split(":")[0]
                    new = time_strings[0][:-1] + first_part

                    time_strings.clear()
                    time_strings.append(new)
            
            time_string = f"{time_strings[0]} {p}"
        
        dt = datetime.datetime.today()
        date_data = {"m": dt.month, "y": dt.year}
        # Check for days
        for day in Resources.days:
            if day in text.split():
                date_data['wd'] = Resources.days.index(day)
                break
        
        # Check for months
        for month in Resources.months:
            splitted = text.split()

            if month in splitted:
                index = splitted.index(month)
                day = None

                try:
                    day = splitted[index + 1]
                except IndexError:
                    pass
                
                if day:
                    day = day.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").strip()

                    try:
                        day = int(day)
                        date_data['d'] = day
                    except ValueError:
                        pass
                
                if not "d" in date_data:
                    date_data['d'] = dt.day
                
                date_data['m'] = Resources.months.index(month) + 1
                break
        
        # Check for indicators

        for indicator, value in Resources.day_indicators.items():
            if indicator in text:
                day = dt.weekday() + value
                if day > 6:
                    diff = abs(day - 6)
                    day = (0 + diff) - 1

                date_data['wd'] = day

        return time_string, date_data

def parse_args(args, _type="module"):
    if _type == "module":
        host, port = args[3], args[4]
        content = args[1]
        parameters = ""
        starts_with = ""

        if len(args) > 7:
            parameters = args[7]
            starts_with = args[8]

        return host, port, content, parameters, starts_with
    elif _type == "background_task":
        api_host, api_port = args[1], args[2]
        ws_host, ws_port = args[3], args[4]
        return api_host, api_port, ws_host, ws_port

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
