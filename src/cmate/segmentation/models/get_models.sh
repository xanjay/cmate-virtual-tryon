#!/bin/bash

echo "Downloading model files..."

# deeplab model
DEEPLAB_URL="https://www.dropbox.com/s/1a2hyzuiol6g1w1/frozen_inference_graph-110871.pb?dl=1"
DEEPLAB_FOLDER="deeplab"
DEEPLAB_MODEL="frozen_inference_graph-110871.pb"

# opepose body_25 model
BODY_25_URL="https://www.dropbox.com/sh/pfrrd0znex1nerz/AABVEnY0ptgrc9iGmjQjBjRDa/pose_iter_584000.caffemodel?dl=1"
BODY_25_FOLDER="mpii_openpose_body25"
BODY_25_MODEL="pose_iter_584000.caffemodel"

mkdir -p deeplab
wget -c ${DEEPLAB_URL} -O ${DEEPLAB_FOLDER}/${DEEPLAB_MODEL}
wget -c ${BODY_25_URL} -O ${BODY_25_FOLDER}/${BODY_25_MODEL}

echo "Model files donwloaded."