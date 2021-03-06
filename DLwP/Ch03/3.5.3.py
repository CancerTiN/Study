import copy
import logging
import time

import numpy as np
from keras import layers
from keras import models
from keras.datasets import reuters
from keras.utils.np_utils import to_categorical

logging.basicConfig(format='%(asctime)s\t%(name)s\t%(levelname)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

(train_data, train_labels), (test_data, test_labels) = reuters.load_data(num_words=10000)

logging.debug(len(train_data))
logging.debug(len(test_data))
logging.debug(train_data[10])

word_index = reuters.get_word_index()
reverse_word_index = dict((value, key) for key, value in word_index.items())
decoded_newswire = ' '.join(reverse_word_index.get(i - 3, '?') for i in train_data[0])

logging.debug(decoded_newswire)
logging.debug(train_labels[10])


def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.0
    return results


x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

one_hot_train_labels = to_categorical(train_labels)
one_hot_test_labels = to_categorical(test_labels)

model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(46, activation='softmax'))
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

x_val = x_train[:1000]
partial_x_train = x_train[1000:]
y_val = one_hot_train_labels[:1000]
partial_y_train = one_hot_train_labels[1000:]

history = model.fit(partial_x_train, partial_y_train, batch_size=512, epochs=9, validation_data=(x_val, y_val))
results = model.evaluate(x_test, one_hot_test_labels)

time.sleep(1)
logging.debug(['categorical_crossentropy', 'accuracy'])
logging.debug(results)

test_labels_copy = copy.copy(test_labels)
np.random.shuffle(test_labels_copy)
hits_array = np.array(test_labels) == np.array(test_labels_copy)
logging.debug(np.sum(hits_array) / len(test_labels))

predictions = model.predict(x_test)
logging.debug(predictions[0].shape)
logging.debug(np.sum(predictions[0]))
logging.debug(np.argmax(predictions[0]))
