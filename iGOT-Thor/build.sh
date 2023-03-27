#!/bin/bash
# Build script
set -eo pipefail

build_tag=$1
name='profanity-image-moderation'
node=$2
org=$3
cd $docker_file_path

docker build -f ${dockerfile} --label commitHash=$(git rev-parse --short HEAD) -t ${org}/${name}:${build_tag} .
echo {\"image_name\" : \"${name}\", \"image_tag\" : \"${build_tag}\", \"node_name\" : \"$node\"} > metadata.json
