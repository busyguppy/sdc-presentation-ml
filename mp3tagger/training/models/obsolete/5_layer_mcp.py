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
    x = layers.Dense(50, activation='sigmoid', name='dense_2')(x)
    # x = layers.Dense(25, activation='sigmoid', name='dense_3')(x)
    outputs = layers.Dense(3, activation='softmax', name='predictions')(x)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

df = load_data()
df = preprocessing(df)

tf.keras.backend.clear_session()

# sklearn調用Keras模型
estimator = KerasClassifier(build_fn=baseline_model, epochs=10, batch_size=1000, verbose=0)
kfold = KFold(n_splits=10, shuffle=True)

start = time.time()

use_standardization = True
use_normalization = False
'''
(std, normal):
(T,T) = 87.28% (1.28%)
(T,F) = 86.89% (1.35%)
(F,T) = 86.36% (1.79%)
(F,F) = 87.12% (1.22%)
'''

results = None
x = df.to_numpy()[:, 0:14]
# standardization, normalization只能對data作! 不能對label作!
if use_standardization:
    x = sklearn.preprocessing.scale(df.to_numpy()[:, 0:14])
if use_normalization:
    # Normalize後準確率反而下降了@@
    x = sklearn.preprocessing.normalize(df.to_numpy()[:, 0:14])

results = cross_val_score(estimator, df.to_numpy()[:, 0:14], df.to_numpy()[:, 13], cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))
print('訓練時間：{}'.format(time.time() - start))