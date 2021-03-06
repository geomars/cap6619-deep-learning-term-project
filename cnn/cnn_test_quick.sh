#!/bin/bash

# Run on pass in each test, with the default values
# Use for quick evaluation before longer tests

python3 CAP6619_term_project_cifar_10_cnn_standard.py \
   --learning_rate=0.0001 --units_dense_layer=512 --epochs=50

python3 CAP6619_term_project_cifar_10_cnn_dropout_all.py \
   --learning_rate=0.001 --units_dense_layer=1024 --epochs=50

python3 CAP6619_term_project_cifar_10_cnn_dropout_dense.py \
   --learning_rate=0.001 --units_dense_layer=1024 --epochs=50

python3 CAP6619_term_project_cifar_10_cnn_batch_normalization.py \
   --learning_rate=0.0005 --units_dense_layer=512 --epochs=50

python3 CAP6619_term_project_cifar_10_cnn_batchnorm_dropout.py \
   --learning_rate=0.0005 --units_dense_layer=512 --epochs=50
