from sklearn.model_selection import KFold, cross_val_score
from sklearn.svm import SVC

from mp3tagger.training import load_data, preprocessing

# 0.903

df = load_data()
df = preprocessing(df)

x_valid = df.to_numpy()[-4000:, :14]
y_valid = df.to_numpy()[-4000:, 13]
x_train = df.to_numpy()[:-4000, :14]
y_train = df.to_numpy()[:-4000, 13]

clf = SVC(gamma=0.001, C=100.)
# clf.fit(x_train, y_train)
# score = clf.score(x_valid, y_valid)
kfold = KFold(n_splits=10, shuffle=True)
results = cross_val_score(clf, df.to_numpy()[:, 0:14], df.to_numpy()[:, 13], cv=kfold)
print("SVC: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))
# print(score)
# print(re)

