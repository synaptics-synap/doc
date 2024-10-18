#!/bin/bash

LATEST_BRANCH=${LATEST_BRANCH:="refs/heads/main"}

set -e

cd doc

mkdir -p _build

if [[ -f _build/doxygen/xml/index.xml ]] ; then
    echo "Skipping build of doxygen because _build/doxygen/xml/index.xml already exists"
else
    echo Building doxygen...

    doxygen Doxyfile
fi

echo Building sphinx...

sphinx-build . _build/html

if [[ "${GITHUB_REF}" == "${LATEST_BRANCH}" ]]; then
  /tools/create-site.py
else
  cp -r _build/html _build/site
fi

echo Updating permission of files...

chown -R $(stat -c '%u:%g' . ) _build

echo Done
