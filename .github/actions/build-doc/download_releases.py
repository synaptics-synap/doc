#!/usr/bin/env python3

import http.client
import json
import os
import zipfile
import urllib.request as rq

DOWNLOAD_FOLDER = "v"

conn = http.client.HTTPSConnection("api.github.com")

headers = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'synaptics-synap-doc-ci'
}

url = '/repos/synaptics-synap/doc/releases'

conn.request("GET", url, headers=headers)

response = conn.getresponse()
data = response.read().decode()

os.makedirs('v', exist_ok=True)

if response.status == 200:
    releases = json.loads(data)
    for release in releases:
        print(f"Release: {release['name']}, Tag: {release['tag_name']}, URL: {release['html_url']}")
        if os.path.exists("v/" + release['name'][1:]):
            print("Documentation already downloaded, skipping.")
            continue
        if release['assets']:
            first_asset = release['assets'][0]
            asset_url = first_asset['browser_download_url']
            asset_name = first_asset['name']
            asset_path = 'v/' + asset_name

            rq.urlretrieve(asset_url, asset_path)

            if zipfile.is_zipfile(asset_path):
                with zipfile.ZipFile(asset_path, 'r') as zip_ref:
                    zip_ref.extractall(DOWNLOAD_FOLDER)
                print(f"Downloaded and decompressed: {asset_name}")
            else:
                print(f"Downloaded: {asset_name} (not a ZIP file)")
            os.unlink(asset_path)
else:
    print(f"Failed to fetch releases: {response.status}, {response.reason} {data}")

conn.close()
