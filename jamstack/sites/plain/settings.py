import json

OUTPUT_FOLDER = 'dist/'
info = None

with open('info.json', 'r') as f:
    info = json.load(f)
