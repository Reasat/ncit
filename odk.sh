#!/bin/sh
IMAGE=${IMAGE:-odkfull}
docker run -v "$PWD/:/work" -w /work \
  -e ROBOT_JAVA_ARGS="-Xmx12G" -e JAVA_OPTS="-Xmx12G" \
  --rm -ti obolibrary/$IMAGE "$@"
