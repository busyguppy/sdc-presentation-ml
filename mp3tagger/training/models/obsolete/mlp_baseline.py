import sklearn
import tensorflow as tf
from keras import Sequential, Input, Model
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

from mp3tagger.training.utils import load_data, preprocessing

def model_baseline():
    inputs = Input(shape=(13,))
    x = Dense(100, activation='sigmoid', kernel_initializer='he_normal')(inputs)
    outputs = Dense(3, activation='softmax', kernel_initializer='he_normal')(x)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

df = load_data()
df = preprocessing(df)

x, y = shuffle(df.to_numpy()[:,:-1], df.to_numpy()[:,-1])
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=40)

# 使用Feature Scaling後準確率上升快2%!
use_standardization = True
use_normalization = True

if use_standardization:
    x_train = sklearn.preprocessing.scale(x_train)
    x_val = sklearn.preprocessing.scale(x_val)
if use_normalization:
    x_train = sklearn.preprocessing.scale(x_train)
    x_val = sklearn.preprocessing.scale(x_val)

# epochs大約在50就收斂了
# batch_size大一點accuracy會比較穩定
# batch_size大約在75~100間
model = model_baseline()
result = model.fit(x_train, y_train, epochs=50, batch_size=100, verbose=2,
                   validation_data=(x_val, y_val))


fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

ax1.plot(result.epoch, result.history['accuracy'], color='blue',
         linewidth=3, label='train acc')
ax1.plot(result.epoch, result.history['val_accuracy'], color='magenta',
         linewidth=3, label='val acc')

ax2.plot(result.epoch, result.history['loss'], color='blue',
         linewidth=3, label='train loss')
ax2.plot(result.epoch, result.history['val_loss'], color='magenta',
         linewidth=3, label='val loss')
ax1.legend()
ax1.set_xlabel('epochs')
ax1.set_ylabel('Accuracy')
ax1.set_ylim([0.825, 1])
ax2.legend()
ax2.set_xlabel('epochs')
ax2.set_ylabel('Loss')
ax2.set_ylim([0.1, 0.5])
plt.show()
# loss, acc = four_layer.evaluate(x_test, y_test, verbose=1)





print('')

