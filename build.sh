#!/bin/bash

set -e

ROOT_DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

echo Building docker...

IMAGE_ID=$(docker build -q ${ROOT_DIR}/.github/actions/build-doc)

docker run -it --rm -v /:/host/ -u $(id -u):$(id -g) -w /host/${ROOT_DIR}/.. ${IMAGE_ID}
