import json
import os
import urllib.request

import requests
from tqdm import tqdm

templates_url = ("https://api.github.com/repos/jamstackpy/"
                 "jamstack-templates/git/trees/main?recursive=1")


def get_raw_url(file_path, url):
    tmp_url = url.replace(
        'https://api.github.com/repos/',
        'https://raw.githubusercontent.com/')
    tmp_url = tmp_url.split('/git/blobs/')[0]
    tmp_url = tmp_url + '/master/' + file_path
    return tmp_url


def get_download_links(template):
    api = requests.get(templates_url).text
    print(templates_url)
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
    files = output
    location = location

    return (files, location)


def mkdirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def download(template, target_folder='*', recursive=True):
    data = get_download_links(template)
    files = data[0]
    location = data[1]

    # mkdirs(".")

    if target_folder == '*':
        start = 0
    else:
        tmp_target = target_folder.replace('./', '')
        tmp_target = tmp_target.replace('../', '')

        # Remove "/"
        tmp_target = (tmp_target if tmp_target[-1] != '/'
                      else tmp_target[:-1])
        start = location[target_folder]

    # Start download
    with tqdm(total=len(files), desc="Downloading assets...") as pbar:
        for i in files[start:]:
            ndir = i[0].replace('templates/' + template, 'dist/assets/')
            if recursive or ndir.split(target_folder)[1].count('/') \
                    <= 1:
                mkdirs('.' + '/' + os.path.dirname(ndir))
                urllib.request.urlretrieve(i[1], '.' + '/' + ndir)
            pbar.update(1)
