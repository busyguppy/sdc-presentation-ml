
import sklearn
import tensorflow as tf
from keras import Sequential, Input, Model
from keras.layers import Dense, Dropout, Activation
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

from mp3tagger.training.utils import load_data, preprocessing

from hyperopt import Trials, STATUS_OK, tpe
from hyperas import optim
from hyperas.distributions import choice, uniform

def data():
    df = load_data()
    df = preprocessing(df)

    x, y = shuffle(df.to_numpy()[:,:-1], df.to_numpy()[:,-1])
    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=40)

    use_standardization = True
    use_normalization = True

    if use_standardization:
        x_train = sklearn.preprocessing.scale(x_train)
        x_val = sklearn.preprocessing.scale(x_val)
    if use_normalization:
        x_train = sklearn.preprocessing.scale(x_train)
        x_val = sklearn.preprocessing.scale(x_val)

    return x_train, y_train, x_val, y_val

def model(x_train, y_train, x_val, y_val):
    model = Sequential()
    # four_layer.add(Dense({{choice([13, 26, 36, 52])}}, input_shape=(13,)))
    model.add(Dense(26, input_shape=(13,)))
    # four_layer.add(Activation({{choice(['relu', 'sigmoid'])}}))
    model.add(Activation('sigmoid'))

    # four_layer.add(Dense({{choice([13, 26, 36, 52])}}))
    # four_layer.add(Activation({{choice(['relu', 'sigmoid'])}}))
    # four_layer.add(Dense({{choice([6, 13, 26, 36, 52])}}))
    # four_layer.add(Activation({{choice(['relu', 'sigmoid'])}}))
    model.add(Dense(3))
    model.add(Activation('softmax'))

    adam = tf.keras.optimizers.Adam(lr={{choice([10 ** -3, 10 ** -2, 10 ** -1])}})

    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
    model.fit(x_train, y_train, batch_size={{choice([25, 50, 75, 100])}},
              nb_epoch={{choice([40, 60, 80])}}, verbose=2,
              validation_data=(x_val, x_train))

    score, acc = model.evaluate(x_val, y_val, verbose=0)
    print('Test accuracy:', acc)
    return {'loss': -acc, 'status': STATUS_OK, 'four_layer': model}


x_train, y_train, x_val, y_val = data()
best_run, best_model = optim.minimize(model=model, data=data, algo=tpe.suggest,
                                      max_evals=5, trials=Trials())
