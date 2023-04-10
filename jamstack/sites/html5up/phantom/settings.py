import json

OUTPUT_FOLDER = 'dist/'
info = None
posts = None

with open('info.json', 'r') as f:
    info = json.load(f)

with open('posts.json', 'r') as f:
    posts = json.load(f)
