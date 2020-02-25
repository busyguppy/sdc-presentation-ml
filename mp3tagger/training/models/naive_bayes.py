from sklearn.naive_bayes import BernoulliNB
from mp3tagger.training import load_data, preprocessing

# 0.859

df = load_data()
df = preprocessing(df)

x_valid = df.to_numpy()[-4000:, :14]
y_valid = df.to_numpy()[-4000:, 13]
x_train = df.to_numpy()[:-4000, :14]
y_train = df.to_numpy()[:-4000, 13]

clf = BernoulliNB()
clf.fit(x_train, y_train)
score = clf.score(x_valid, y_valid)
print(score)


