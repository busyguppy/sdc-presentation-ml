from sklearn.feature_selection import SelectKBest, chi2
import pandas as pd
from mp3tagger.training.utils import load_data, preprocessing

df = load_data()
# df = df[df['label'].isin(['a', 't'])]
df = preprocessing(df)



x, y = df.iloc[:, :-1], df.iloc[:, -1]
best_features = SelectKBest(score_func=chi2, k=10)
result = best_features.fit(x, y)
scores = pd.DataFrame(result.scores_)
columns = pd.DataFrame(x.columns)
feature_scores = pd.concat([columns, scores], axis=1)
feature_scores.columns = ['Feature', 'Score']
ndf = feature_scores.nlargest(13, 'Score')
ndf['Score'] = ndf['Score'].map('{:,.0f}'.format)
print(ndf)