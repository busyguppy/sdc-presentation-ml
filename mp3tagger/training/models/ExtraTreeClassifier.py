from sklearn.tree import DecisionTreeClassifier

from mp3tagger.training.utils import load_data, preprocessing

# 竟然是1

df = load_data()
df = preprocessing(df)

x_valid = df.to_numpy()[-4000:, :14]
y_valid = df.to_numpy()[-4000:, 13]
x_train = df.to_numpy()[:-4000, :14]
y_train = df.to_numpy()[:-4000, 13]

clf = DecisionTreeClassifier()
clf.fit(x_train, y_train)
score = clf.score(x_valid, y_valid)
print(score)


