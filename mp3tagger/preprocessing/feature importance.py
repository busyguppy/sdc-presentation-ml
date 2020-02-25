import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt

from mp3tagger.training.utils import load_data, preprocessing

model = ExtraTreesClassifier()
df = load_data()
df = preprocessing(df)
x, y = df.iloc[:, :-1], df.iloc[:, -1]
model.fit(x, y)
print(model.feature_importances_)
feat_importances = pd.Series(model.feature_importances_, index=x.columns)
feat_importances.nlargest(13).iloc[::-1].plot(kind='barh')
plt.show()