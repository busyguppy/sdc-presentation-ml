import time
import tensorflow as tf
import sklearn
from keras import Input, layers, Model
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score, KFold

from mp3tagger.training.utils import load_data, preprocessing

# 86.68% (1.18%)

def baseline_model():
    inputs = Input(shape=(13,), name='features')
    x = layers.Dense(10, activation='sigmoid', name='dense_1')(inputs)
    outputs = layers.Dense(3, activation='softmax', name='predictions')(x)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

df = load_data()
df = preprocessing(df)

tf.keras.backend.clear_session()

# sklearn調用Keras模型
estimator = KerasClassifier(build_fn=baseline_model, epochs=50, batch_size=100, verbose=0)
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
x = df.to_numpy()[:, 0:13]
y = df.to_numpy()[:, 13]
# standardization, normalization只能對data作! 不能對label作!
if use_standardization:
    x = sklearn.preprocessing.scale(df.to_numpy()[:, 0:13])
if use_normalization:
    # 用了normalization準確度反而變差了@@，91.40% -> 74.59%
    x = sklearn.preprocessing.normalize(df.to_numpy()[:, 0:13])

results = cross_val_score(estimator, x, y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))
print('訓練時間：{}'.format(time.time() - start))