from jamstack.api.template import load_json

OUTPUT_FOLDER = 'dist/'

info = load_json('info.json')
posts = load_json('posts.json')
