#!/bin/bash

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

sudo apt-get update

sudo apt-get install edgetpu-compiler

TPU_NUM=1

TFLITE_FILENAME_A=model_A.tflite

TFLITE_FILENAME_B=model_B.tflite

edgetpu_compiler --num_segments=$TPU_NUM $TFLITE_FILENAME_A $TFLITE_FILENAME_B