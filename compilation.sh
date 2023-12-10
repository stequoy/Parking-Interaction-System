#!/bin/bash

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

sudo apt-get update

sudo apt-get install edgetpu-compiler

TPU_NUM=1

TFLITE_FILENAME=model.tflite

edgetpu_compiler $TFLITE_FILENAME --search_delegate --num_segments=$TPU_NUM