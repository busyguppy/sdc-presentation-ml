import sklearn
import tensorflow as tf
from keras import Sequential, Input, Model
from keras.layers import Dense, Dropout
from keras.optimizers import Adamax
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

from mp3tagger import tools
from mp3tagger.training.models.testcallback import TestCallback
from mp3tagger.training.utils import load_data, preprocessing


def baseline():
    inputs = Input(shape=(13,))
    x = Dense(100, activation='sigmoid')(inputs)
    outputs = Dense(3, activation='softmax')(x)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    return model

'''
最佳參數：
batch_size=15, epochs=100, optimizer=Adamax, learning_rate=0.002,
init_mode = glorot_uniform, neurons: n1 = 75, n2 = 13
'''
def three_layer():
    inputs = Input(shape=(13,))
    x = Dense(26, activation='relu')(inputs)
    x = Dense(26, activation='relu')(x)
    outputs = Dense(3, activation='softmax')(x)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def three_layer_optimized():
    inputs = Input(shape=(13,))
    x = Dense(75, activation='relu', kernel_initializer='glorot_uniform')(inputs)
    x = Dense(15, activation='relu', kernel_initializer='glorot_uniform')(x)
    outputs = Dense(3, activation='softmax', kernel_initializer='glorot_uniform')(x)
    model = Model(inputs=inputs, outputs=outputs)
    optimizer = Adamax(learning_rate=0.002)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model


def six_layer():
    inputs = Input(shape=(13,))
    x = Dense(36, activation='relu')(inputs)
    x = Dense(26, activation='relu')(x)
    x = Dense(26, activation='relu')(x)
    x = Dense(26, activation='relu')(x)
    x = Dense(13, activation='relu')(x)
    outputs = Dense(3, activation='softmax')(x)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    return model

df = load_data()
df = preprocessing(df)

# x, y = shuffle(df.to_numpy()[:, :-1], df.to_numpy()[:, -1])
x = df.to_numpy()[:, :-1]
y = df.to_numpy()[:, -1]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=40)
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=20)

# 使用Feature Scaling後準確率上升快3%!
use_standardization = True
use_normalization = True

if use_standardization:
    x_train = sklearn.preprocessing.scale(x_train)
    x_test = sklearn.preprocessing.scale(x_test)
    x_val = sklearn.preprocessing.scale(x_val)
if use_normalization:
    x_train = sklearn.preprocessing.normalize(x_train)
    x_test = sklearn.preprocessing.normalize(x_test)
    x_val = sklearn.preprocessing.normalize(x_val)

# epochs大約在50就收斂了
# batch_size大一點accuracy會比較穩定
# batch_size大約在75~100間
model = four_layer()
result = model.fit(x_train, y_train, epochs=80, batch_size=100, verbose=2,
                   validation_data=(x_val, y_val),
                   callbacks=[TestCallback((x_test, y_test))])

score = model.evaluate(x_test, y_test, verbose=0)



fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

linewidth = 1

ax1.plot(result.epoch, result.history['accuracy'], color='blue',
         linewidth=linewidth, label='train acc')
ax1.plot(result.epoch, result.history['val_accuracy'], color='magenta',
         linewidth=linewidth, label='val acc')
ax1.plot(result.epoch, result.history['test_accuracy'], color='orange',
         linewidth=linewidth, label='test acc')

ax2.plot(result.epoch, result.history['loss'], color='blue',
         linewidth=linewidth, label='train loss')
ax2.plot(result.epoch, result.history['val_loss'], color='magenta',
         linewidth=linewidth, label='val loss')
ax2.plot(result.epoch, result.history['test_loss'], color='orange',
         linewidth=linewidth, label='test loss')

ax1.legend()
ax1.set_xlabel('epochs')
ax1.set_ylabel('Accuracy')
ax1.set_ylim([0.85, 0.95])
ax2.legend()
ax2.set_xlabel('epochs')
ax2.set_ylabel('Loss')
ax2.set_ylim([0.1, 0.5])
plt.show()
# loss, acc = four_layer.evaluate(x_test, y_test, verbose=1)


# preserving four_layer

# model.save(tools.data_file('mlp_4Layer.h5'))
# new_model = keras.models.load_model('path_to_my_model.h5')
print('')

