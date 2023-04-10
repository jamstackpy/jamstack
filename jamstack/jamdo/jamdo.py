import json
import os
from urllib.request import urlretrieve

import requests
from tqdm import tqdm

TEMPLATES_URL = ("https://api.github.com/repos/jamstackpy/"
                 "jamstack-templates/git/trees/main?recursive=1")


def get_raw_url(file_path, url):
    tmp_url = url.replace(
        'https://api.github.com/repos/',
        'https://raw.githubusercontent.com/')
    tmp_url = tmp_url.split('/git/blobs/')[0]
    tmp_url = tmp_url + '/master/' + file_path
    return tmp_url


def get_download_links(template):
    api = requests.get(TEMPLATES_URL).text
    files = json.loads(api)
    output = []
    location = dict()
    for (k, i) in enumerate(files['tree']):
        if template in i['path']:
            if i['type'] == 'blob':
                tmp = [i['path']]
                tmp += [get_raw_url(tmp[0], i['url'])]
                output.append(tmp)
            else:
                location[i['path']] = k
    return output, location


def mkdirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def download(template, target_folder='*', recursive=True):
    files, location = get_download_links(template)

    if target_folder == '*':
        start = 0
    else:
        # tmp_target = target_folder.replace('./', '').replace('../', '')
        # tmp_target = tmp_target.rstrip('/')
        start = location[target_folder]

    with tqdm(total=len(files), desc="Downloading assets...") as pbar:
        for i in files[start:]:
            ndir = i[0].replace('templates/' + template, 'dist/assets/')
            if recursive or ndir.split(target_folder)[1].count('/') <= 1:
                mkdirs('.' + '/' + os.path.dirname(ndir))
                urlretrieve(i[1], '.' + '/' + ndir)
            pbar.update(1)
