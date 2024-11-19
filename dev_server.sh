#!/bin/bash

set -e

ROOT_DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

if [[ ! -d "${ROOT_DIR}/framework" ]] ; then
   echo "WARNING: Framework git not found in ${ROOT_DIR}/framework, doxygen generation will not work"
fi

echo "Building docker..."

IMAGE_ID=$(docker build -q ${ROOT_DIR}/.github/actions/build-doc)

docker run --rm -e GITHUB_REF -v /:/host/ -w /host/${ROOT_DIR}/.. ${IMAGE_ID}

# Function to rebuild documentation
rebuild_docs() {
    #  rm -fr _build/
    echo "Changes detected. Rebuilding documentation..."
    docker run --rm -e GITHUB_REF -v /:/host/ -w /host/${ROOT_DIR}/.. ${IMAGE_ID}
}

# Start Python web server to serve the _build/html directory
if [[ -d "${ROOT_DIR}/_build/html" ]]; then
    echo "Starting Python web server to serve _build/html..."
    (cd "${ROOT_DIR}/_build/html" && python3 -m http.server 8002) &
else
    echo "ERROR: Directory _build/html not found!"
    exit 1
fi

# Monitor the 'manual' directory for changes using `find`
echo "Monitoring 'manual' directory for changes..."
LAST_CHECKSUM=$(find "${ROOT_DIR}/manual" -type f -exec md5sum {} + | md5sum)

while true; do
    sleep 5  # Polling interval (adjust as needed)
    CURRENT_CHECKSUM=$(find "${ROOT_DIR}/manual" -type f -exec md5sum {} + | md5sum)
    if [[ "$LAST_CHECKSUM" != "$CURRENT_CHECKSUM" ]]; then
        LAST_CHECKSUM=$CURRENT_CHECKSUM
        rebuild_docs
    fi
done
