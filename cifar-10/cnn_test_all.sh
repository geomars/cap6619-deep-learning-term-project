#!/bin/bash

# Run all CNN tests

python3 CAP6619_term_project_cifar_10_cnn_plain.py \
   --learning_rate=0.0001 --units_dense_layer=512

python3 CAP6619_term_project_cifar_10_cnn_dropout.py \
   --learning_rate=0.001 --units_dense_layer=1024

python3 CAP6619_term_project_cifar_10_cnn_batch_normalization.py \
   --learning_rate=0.0005 --units_dense_layer=512

python3 CAP6619_term_project_cifar_10_cnn_batchnorm_dropout.py \
   --learning_rate=0.0005 --units_dense_layer=512