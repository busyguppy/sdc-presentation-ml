from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import ShuffleSplit

from mp3tagger.training.utils import preprocessing, load_data, plot_learning_curve
import keras
from keras import layers
import matplotlib.pyplot as plt

def baseline_model():
    inputs = keras.Input(shape=(14,), name='features')
    x = layers.Dense(100, activation='sigmoid', name='dense_1')(inputs)
    outputs = layers.Dense(3, activation='softmax', name='predictions')(x)
    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

df = load_data()
df = preprocessing(df)

fig, axes = plt.subplots(3, 2, figsize=(10, 15))

X = df.to_numpy()[:, :13]
y = df.to_numpy()[:, 13]

title = "Learning Curves (Baseline)"
# Cross validation with 100 iterations to get smoother mean test and train
# score curves, each time with 20% data randomly selected as a validation set.
cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

estimator = KerasClassifier(build_fn=baseline_model, epochs=10, batch_size=1000, verbose=0)
plot_learning_curve(estimator, title, X, y, axes=axes[:, 0], ylim=(0.7, 1.01),
                    cv=cv, n_jobs=4)

# title = r"Learning Curves (SVM, RBF kernel, $\gamma=0.001$)"
# # SVC is more expensive so we do a lower number of CV iterations:
# cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=0)
# estimator = SVC(gamma=0.001)
# plot_learning_curve(estimator, title, X, y, axes=axes[:, 1], ylim=(0.7, 1.01),
#                     cv=cv, n_jobs=4)

plt.show()