"""CIFAR-10 using CNN with dropout and batch normalization.

Based on the Keras CIFAR-10 example.

Source: https://github.com/keras-team/keras/blob/d2803c0fb7d0ba9361dcba8eb9bcebbf2f774958/examples/cifar10_cnn.py

Note: to make it work I had to re-introduce `steps_per_epoch` that was removed
in https://github.com/keras-team/keras/commit/bc285462ad8ec9b8bc00bd6e09f9bcd9ae3d84a2#diff-96f332e007bcdf35ed78e7cba091d6f8.

Discussions in that PR say it's not needed in this case, but it didn't work for
me without it.

Original header from from Keras code:

Train a simple deep CNN on the CIFAR10 small images dataset.

It gets to 75% validation accuracy in 25 epochs, and 79% after 50 epochs.
(it's still underfitting at that point, though).
"""

import keras
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.layers import BatchNormalization, Dropout
from keras.layers import Conv2D, MaxPooling2D
from keras import backend
import numpy as np
import json
import time

batch_size = 32
num_classes = 10
epochs = 2  # NOTE: remember to increase this value
data_augmentation = True

# The data, split between train and test sets:
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Convert class vectors to binary class matrices.
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same',
                 input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
# Batch normalization added after activation because of the results reported
# in https://github.com/ducha-aiki/caffenet-benchmark/blob/master/batchnorm.md
# shows that it has higher accuracy.
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
# TODO: test with 2x units
model.add(Dense(512))
model.add(Activation('relu'))
# TODO: test if we should add batch normalization here as well
# model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))

# initiate RMSprop optimizer
# TODO: check if increasing the rate improve is
opt = keras.optimizers.rmsprop(lr=0.0005, decay=1e-6)

# Let's train the model using RMSprop
model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

start = time.process_time()

if not data_augmentation:
    print('Not using data augmentation.')
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_test, y_test),
              shuffle=True)
else:
    print('Using real-time data augmentation.')
    # This will do preprocessing and realtime data augmentation:
    datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        zca_epsilon=1e-06,  # epsilon for ZCA whitening
        # randomly rotate images in the range (degrees, 0 to 180)
        rotation_range=0,
        # randomly shift images horizontally (fraction of total width)
        width_shift_range=0.1,
        # randomly shift images vertically (fraction of total height)
        height_shift_range=0.1,
        shear_range=0.,  # set range for random shear
        zoom_range=0.,  # set range for random zoom
        channel_shift_range=0.,  # set range for random channel shifts
        # set mode for filling points outside the input boundaries
        fill_mode='nearest',
        cval=0.,  # value used for fill_mode = "constant"
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False,  # randomly flip images
        # set rescaling factor (applied before any other transformation)
        rescale=None,
        # set function that will be applied on each input
        preprocessing_function=None,
        # image data format, either "channels_first" or "channels_last"
        data_format=None,
        # fraction of images reserved for validation (strictly between 0 and 1)
        validation_split=0.0)

    # Compute quantities required for feature-wise normalization
    # (std, mean, and principal components if ZCA whitening is applied).
    datagen.fit(x_train)

    # Fit the model on the batches generated by datagen.flow().
    model.fit_generator(
        datagen.flow(x_train, y_train, batch_size=batch_size),
        steps_per_epoch=int(np.ceil(x_train.shape[0] / float(batch_size))),
        epochs=epochs, validation_data=(x_test, y_test), workers=4)

training_time = time.process_time() - start

# Save model
base_name = "cifar_10_cnn_batchnorm_dropout"
model.save(base_name + "_model.h5")

# Save training history
with open(base_name + "_history.json", 'w') as f:
    json.dump(model.history.history, f)

# Save a summary of the results
with open(base_name + "_summary.txt", 'w') as f:
    f.write("Training time: {}\n".format(training_time))
    f.write("Total parameters: {}\n".format(model.count_params()))
    f.write("Optimizer: {}\n".format(type(model.optimizer).__name__))
    f.write("Learning rate: {:0.6f}".format(backend.eval(model.optimizer.lr)))