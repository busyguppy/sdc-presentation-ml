import time
import tensorflow as tf
import sklearn
from keras import Input, layers, Model
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score, KFold

from mp3tagger.training.utils import load_data, preprocessing

# 86.68% (1.18%)

def baseline_model():
    inputs = Input(shape=(14,), name='features')
    x = layers.Dense(100, activation='sigmoid', name='dense_1')(inputs)
    outputs = layers.Dense(3, activation='softmax', name='predictions')(x)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

df = load_data()
df = preprocessing(df)

tf.keras.backend.clear_session()

# sklearn調用Keras模型
estimator = KerasClassifier(build_fn=baseline_model)
x_train = df.to_numpy()[:9999, :14]
y_train = df.to_numpy()[:9999, 13]
x_test = df.to_numpy()[2000:2199, :14]
y_test = df.to_numpy()[2000:2199, 13]

estimator.fit(x_train, y_train)
# s = estimator.score(x_test, y_test)
t = 1