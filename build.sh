set -x
set -e

tag=2.82
docker build -t brainlife/blender container
docker tag brainlife/blender brainlife/blender:$tag
docker push brainlife/blender:$tag
