#!/usr/bin/env python3

import os
import shutil
import http.client
import json
import zipfile
import urllib.request as rq


BANNER_ANCHOR = '<div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">'
VERSION_ANCHOR = '<script>'
CANONICAL_ANCHOR = '<title>'

DOWNLOAD_FOLDER = "v"
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snippets")

# Function to inject content into an HTML file after matching a specific line
def inject_content_into_html(file_path, anchor, content_to_inject):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    injected = False

    # Process each line
    for line in lines:
        # If pattern is found, insert the content
        if anchor in line and not injected:
            new_lines.append(content_to_inject + '\n')
            injected = True

        new_lines.append(line)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(new_lines)


def load_version_bar():
    with open('v/git-main/index.html', 'r') as fp:
        lines = fp.readlines()

    version_lines = []

    found = False
    for line in lines:
        if "<!-- START_VERSIONS -->" in line:
            found = True

        if found:
            version_lines.append(line.strip())

        if "<!-- END VERSIONS -->" in line:
            break

    return " ".join(version_lines)

def download_releases(cache_directory):

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

    os.makedirs(cache_directory, exist_ok=True)

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
                        zip_ref.extractall(cache_directory)
                    print(f"Downloaded and decompressed: {asset_name}")
                else:
                    print(f"Downloaded: {asset_name} (not a ZIP file)")
                os.unlink(asset_path)
    else:
        print(f"Failed to fetch releases: {response.status}, {response.reason} {data}")

    conn.close()

def get_sorted_versions(base_dir):
    versions = [x for x in os.listdir(base_dir) if x != 'latest' and x != 'git-main']
    return  sorted(versions, key=lambda s: [int(x) for x in s.split('.')])


def create_latest_version_link(base_dir):
    latest_version = get_sorted_versions(base_dir)[-1]

    link_name = os.path.join(base_dir, 'latest')

    if os.path.islink(link_name):
        print("Updating latest version")
        os.unlink(link_name)
    else:
        print("Creating link to latest version")

    os.symlink(latest_version, link_name)

    return latest_version


def create_site():

    versions_cache_dir = "v"
    download_releases(versions_cache_dir)

    site_dir = '_build/site'

    if os.path.exists(site_dir):
        shutil.rmtree(site_dir)

    os.makedirs(site_dir)

    # create the main index
    with open(os.path.join(site_dir, 'index.html'), 'w') as fp:
        fp.write(load_template('index.html'))

    # copy released versions
    versions_dir = os.path.join(site_dir, 'v')
    shutil.copytree(versions_cache_dir, versions_dir)

    # copy latest dev version
    dev_version_dir = os.path.join(versions_dir, 'git-main')
    shutil.copytree('_build/html', dev_version_dir)

    # setup a link to the latest released version
    latest_version = create_latest_version_link(versions_dir)

    old_version_banner = load_template("old-release-header.html")
    dev_version_banner = load_template("dev-header.html")

    canonical_header = load_template("canonical.html")

    latest_version_dir = os.path.join(versions_dir, latest_version)

    # update all the files
    for root, dirs, files in os.walk(versions_dir, topdown=True, followlinks=False):

        for file_name in files:

            if not file_name.endswith('.html'):
                continue

            file_path = os.path.join(root, file_name)            

            if root.startswith(dev_version_dir):
                # inject the development version warning in the latest version
                inject_content_into_html(file_path, BANNER_ANCHOR, dev_version_banner)

            elif not root.startswith(latest_version_dir):
                # inject the old version warning banner in the non-latest versions
                inject_content_into_html(file_path, BANNER_ANCHOR, old_version_banner)

            # inject the version bar in the doc we downloaded from the release
            inject_content_into_html(file_path, VERSION_ANCHOR, get_version_bar(versions_dir, file_path))

            # inject the canonical header
            path_parts = os.path.relpath(file_path, versions_dir).split('/')

            if path_parts[-1] == 'index.html':
                canonical_path = "/".join(path_parts[1:-1]) + ('/' if len(path_parts) > 2 else '')
            else:
                canonical_path = "/".join(path_parts[1:])

            page_canonical_header = canonical_header.replace('%PAGE_PATH%', canonical_path)
            inject_content_into_html(file_path, CANONICAL_ANCHOR, page_canonical_header)

            print(f"Processed {file_path}")

def load_template(template_name, **kwargs):
    with open(os.path.join(TEMPLATE_DIR, template_name), 'r') as fp:
        data = fp.read()

    for key, value in kwargs.items():
        data = data.replace(f'%%{key.upper()}%%', value)

    return data

def get_version_bar(versions_dir, file_name):

    latest_version = os.path.basename(os.readlink(os.path.join(versions_dir, 'latest')))

    versions = []

    for v in ['git-main'] + get_sorted_versions(versions_dir)[::-1]:
        version_label = v
        version_url = "/doc/v/" + v + "/"

        if v == latest_version:
            version_label += " (latest)"

        versions.append(f'<dd><a href="{version_url}">{ version_label }</a>')

    current_version = os.path.relpath(file_name, versions_dir).split('/')[0]

    if current_version == latest_version:
        current_version += ' (latest)'

    return load_template('versions.html', versions="\n".join(versions), current_version=current_version)


if __name__ == "__main__":
    create_site()
