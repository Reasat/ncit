#!/bin/sh
IMAGE=${IMAGE:-odkfull}
docker run -v "$PWD/:/work" -w /work \
  -e ROBOT_JAVA_ARGS="-Xmx24G" -e JAVA_OPTS="-Xmx24G" \
  --rm -ti obolibrary/$IMAGE "$@"
