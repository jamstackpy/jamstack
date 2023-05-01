import os
import urllib.request

import requests
from tqdm import tqdm

TEMPLATES_URL = "https://api.github.com/repos/jamstackpy/jamstack-templates/git/trees/main?recursive=1"


def mkdirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def get_raw_url(file_path, url):
    raw_url = url.replace(
        'https://api.github.com/repos/',
        'https://raw.githubusercontent.com/')
    raw_url = raw_url.split('/git/blobs/')[0]
    raw_url = raw_url + '/master/' + file_path
    return raw_url


def get_download_links(template):
    api = requests.get(TEMPLATES_URL).json()
    files = api['tree']
    output = []
    location = {}
    for i, file in enumerate(files):
        if template in file['path']:
            if file['type'] == 'blob':
                output.append([file['path'], get_raw_url(file['path'], file['url'])])
            else:
                location[file['path']] = i
    return output, location


def download(template, target_folder='*', recursive=True):
    data = get_download_links(template)
    files = data[0]
    location = data[1]

    if target_folder == '*':
        start = 0
    else:
        start = location[target_folder]

    with tqdm(total=len(files), desc="Downloading assets...") as pbar:
        for i in files[start:]:
            ndir = i[0].replace('templates/' + template, 'dist/assets/')
            if recursive or ndir.split(target_folder)[1].count('/') <= 1:
                mkdirs('.' + '/' + os.path.dirname(ndir))
                urllib.request.urlretrieve(i[1], '.' + '/' + ndir)
            pbar.update(1)
