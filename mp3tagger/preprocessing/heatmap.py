import pandas as pd
import seaborn as sns
#get correlations of each features in dataset
from mp3tagger.training.utils import load_data, preprocessing
import matplotlib.pyplot as plt


# top_corr_features = x.index
plt.figure(figsize=(20, 20))
#plot heat map
df = load_data()
df = preprocessing(df)
x = df.iloc[:, :-1]
corr = x.corr()
ax = sns.heatmap(df.corr(), annot=True, cmap=sns.diverging_palette(20, 220, n=200))
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.show()