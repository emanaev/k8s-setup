#!/bin/bash
DOCKER="sudo docker"
IMAGE=k8setup
$DOCKER build -t $IMAGE .
ID_RSA=`paste -sd ";" ~/.ssh/id_rsa`
$DOCKER run -it --rm -e ID_RSA="$ID_RSA" -e HCLOUD_TOKEN=$HCLOUD_TOKEN $IMAGE
