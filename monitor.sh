#!/bin/bash

DIRECTORY_TO_WATCH="/home/ubuntu/doc"
BUILD_SCRIPT="./build.sh"
CHECK_INTERVAL=2 # seconds

generate_checksum() {
    find "$DIRECTORY_TO_WATCH" -type f \( ! -path "$DIRECTORY_TO_WATCH/_build/*" \) -exec md5sum {} \; | sort -k 2 | md5sum
}

previous_checksum=$(generate_checksum)

while true; do
    sleep "$CHECK_INTERVAL"
    current_checksum=$(generate_checksum)

    if [ "$previous_checksum" != "$current_checksum" ]; then
        echo "Changes detected. Running build script..."
        $BUILD_SCRIPT
        previous_checksum=$current_checksum
    fi
done


