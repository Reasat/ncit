#!/bin/sh
IMAGE=${IMAGE:-odkfull}
docker run -v "$PWD/:/work" -w /work \
  -e ROBOT_JAVA_ARGS="-Xmx4G" -e JAVA_OPTS="-Xmx4G" \
  --rm -ti obolibrary/$IMAGE "$@"
