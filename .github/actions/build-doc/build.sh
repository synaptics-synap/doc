#!/bin/bash

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


echo Updating permission of files...

chown -R $(stat -c '%u:%g' . ) _build
