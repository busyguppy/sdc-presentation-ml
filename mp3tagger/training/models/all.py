
import time
import tensorflow as tf
import sklearn
from keras import Input, layers, Model
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

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

clfs = [
     # ("Logistic Regression", LogisticRegression(solver='newton-cg', max_iter=1000, C=1, multi_class='ovr')),
    ("Nearest Neighbors", KNeighborsClassifier(3)),
    # ("Linear SVM", SVC(kernel="linear", C=0.025)),
    ("RBF SVM", SVC(gamma=2, C=1)),
    ("Decision Tree", DecisionTreeClassifier(max_depth=5)),
    ("Random Forest", RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)),
    ("Neural Net", MLPClassifier(alpha=0.01, max_iter=1000)),
    ("AdaBoost", AdaBoostClassifier()),
    ("Naive Bayes", GaussianNB()),
    # ("Gaussian Process", GaussianProcessClassifier(1.0 * RBF(1.0))),
    ("QDA", QuadraticDiscriminantAnalysis())
]

cross_validate = False

if cross_validate: print('Using cross validation')
for name, clf in clfs:
    # print('\n=== {} ==='.format(name))
    if cross_validate:
        results = cross_val_score(clf, df.to_numpy()[:, 0:14], df.to_numpy()[:, 13], cv=kfold)
        print("{}: Accuracy:{:.2f}% Std:({:.2f}%)".format(name, results.mean() * 100, results.std() * 100))
        print('訓練時間：{}'.format(time.time() - start))
    else:
        # not working: inconsistent number of samples
        # x_train, x_test, y_train, y_test = train_test_split(
        #     df.to_numpy()[:, :13], df.to_numpy()[:, 13], test_size=0.2, random_state=13)
        n = -4000
        x_test = df.to_numpy()[n:, :13]
        y_test = df.to_numpy()[n:, 13]
        x_train = df.to_numpy()[:n, :13]
        y_train = df.to_numpy()[:n, 13]

        clf.fit(x_train, y_train)
        score = clf.score(x_test, y_test)
        print("----\n{} (score={:.5f}):".format(name, score))



