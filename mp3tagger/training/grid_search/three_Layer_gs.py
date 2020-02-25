import time
from typing import Tuple

import numpy
import sklearn
from keras import Input, Model
from keras.layers import Dense, Dropout
from keras.optimizers import Adamax
from keras.wrappers.scikit_learn import KerasClassifier
from numpy.core.multiarray import ndarray
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.utils import shuffle
from mp3tagger.training.utils import load_data, preprocessing


import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

seed = 7
numpy.random.seed(seed)

def prepare_data() -> Tuple[ndarray, ndarray]:
    df = load_data()
    df = preprocessing(df)

    x, y = shuffle(df.to_numpy()[:, :-1], df.to_numpy()[:, -1])

    x = sklearn.preprocessing.scale(x)
    x = sklearn.preprocessing.scale(x)
    return (x, y)

def step1(x: ndarray, y:ndarray):
    """ Grid Search Batch_size, epochs, optimizer
    Time spent: 1 hour1, 24 minutes and 6 seconds without GPU acceleration.
    Best Parameter:
    0.9203319748242696 參數： {'batch_size': 15, 'epochs': 100, 'optimizer': 'Adamax'}
    """
    ts = time.time()
    def create_model(optimizer='adam'):
        inputs = Input(shape=(13,))
        x = Dense(26, activation='relu')(inputs)
        x = Dense(26, activation='relu')(x)
        outputs = Dense(3, activation='softmax')(x)
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        return model

    model = KerasClassifier(build_fn=create_model, verbose=2)

    batch_size = [15, 25, 50, 75, 100]
    epochs = [80, 100, 120]
    optimizer = ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']

    param_grid = dict(batch_size=batch_size, epochs=epochs, optimizer=optimizer)
    grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=4, cv=4)
    grid_result = grid.fit(x, y)

    print(f'最佳: {grid_result.best_score_} 參數： {grid_result.best_params_}')
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print(f'平均：{mean} 標準差：{stdev} 參數：{param}')

    print(f'GS時間：{time.time()-ts}')


def step2(x: ndarray, y: ndarray):
    """ optimizer parameters: Adamax learing Rate
    Time spent: 19 minutes and 39 seconds without GPU acceleration.
    Best Parameter:
    最佳: 0.9192667603492737 參數： {'learn_rate': 0.002}
    """

    ts = time.time()

    def create_model(learn_rate=0.002):
        inputs = Input(shape=(13,))
        x = Dense(26, activation='relu')(inputs)
        x = Dense(26, activation='relu')(x)
        outputs = Dense(3, activation='softmax')(x)
        model = Model(inputs=inputs, outputs=outputs)
        optimizer = Adamax(learning_rate=learn_rate)
        model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        return model

    model = KerasClassifier(build_fn=create_model, batch_size=15, epochs=100,
                            verbose=2)

    learn_rate = [0.001, 0.002, 0.01, 0.02, 0.1, 0.2, 0.3]

    param_grid = dict(learn_rate=learn_rate)
    grid = GridSearchCV(estimator=model, param_grid=param_grid,
                        n_jobs=4, cv=4)
    grid_result = grid.fit(x, y)

    print(f'最佳: {grid_result.best_score_} 參數： {grid_result.best_params_}')
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print(f'平均：{mean} 標準差：{stdev} 參數：{param}')

    print(f'GS時間：{time.time() - ts}')

def step3(x: ndarray, y: ndarray):
    """ Network Weight Initialization
    Time spent: 16 minutes and 17 seconds without GPU acceleration.
    Best Parameter:
    最佳: 0.9203764796257019 參數： {'init_mode': 'glorot_uniform'}
    """

    ts = time.time()
    def create_model(init_mode='uniform'):
        inputs = Input(shape=(13,))
        x = Dense(26, activation='relu', kernel_initializer=init_mode)(inputs)
        x = Dense(26, activation='relu', kernel_initializer=init_mode)(x)
        outputs = Dense(3, activation='softmax', kernel_initializer=init_mode)(x)
        model = Model(inputs=inputs, outputs=outputs)
        optimizer = Adamax(learning_rate=0.002)
        model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        return model

    model = KerasClassifier(build_fn=create_model, batch_size=15, epochs=100,
                            verbose=2)

    init_mode = ['uniform', 'lecun_uniform', 'normal', 'zero', 'glorot_normal',
                 'glorot_uniform', 'he_normal', 'he_uniform']

    param_grid = dict(init_mode=init_mode)
    grid = GridSearchCV(estimator=model, param_grid=param_grid,
                        n_jobs=4, cv=4)
    grid_result = grid.fit(x, y)

    print(f'最佳: {grid_result.best_score_} 參數： {grid_result.best_params_}')
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print(f'平均：{mean} 標準差：{stdev} 參數：{param}')

    print(f'GS時間：{time.time() - ts}')

def step4(x: ndarray, y: ndarray):
    """ Neurons
    Time spent: 1 hour, 13 minutes and 18 seconds without GPU acceleration.
    Best Parameter:
    最佳: 0.9210865050554276 參數： {'n1': 75, 'n2': 13}
    """

    ts = time.time()

    def create_model(n1= 26, n2=26):
        inputs = Input(shape=(13,))
        x = Dense(n1, activation='relu', kernel_initializer='glorot_uniform')(inputs)
        x = Dense(n2, activation='relu', kernel_initializer='glorot_uniform')(x)
        outputs = Dense(3, activation='softmax', kernel_initializer='glorot_uniform')(x)
        model = Model(inputs=inputs, outputs=outputs)
        optimizer = Adamax(learning_rate=0.002)
        model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        return model

    model = KerasClassifier(build_fn=create_model, batch_size=15, epochs=100,
                            verbose=2)

    n1 = [13, 26, 50, 75]
    n2 = n1
    param_grid = dict(n1=n1, n2=n2)
    grid = GridSearchCV(estimator=model, param_grid=param_grid,
                        n_jobs=4, cv=4)
    grid_result = grid.fit(x, y)

    print(f'最佳: {grid_result.best_score_} 參數： {grid_result.best_params_}')
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print(f'平均：{mean} 標準差：{stdev} 參數：{param}')

    print(f'GS時間：{time.time() - ts}')



if __name__ == '__main__':
    x, y = prepare_data()
    # step1(x, y)
    # step2(x, y)
    # step3(x, y)
    step4(x, y)