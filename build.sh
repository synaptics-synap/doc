#!/bin/bash

set -e

ROOT_DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

if [[ ! -d "${ROOT_DIR}/framework" ]] ; then
   echo "WARNING: Framework git not found in ${ROOT_DIR}/framework, doxygen generation will not work"
fi


echo Building docker...

IMAGE_ID=$(docker build -q ${ROOT_DIR}/.github/actions/build-doc)

docker run --rm -e GITHUB_REF -v /:/host/ -w /host/${ROOT_DIR}/.. ${IMAGE_ID}
