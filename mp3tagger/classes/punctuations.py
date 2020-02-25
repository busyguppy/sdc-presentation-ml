
stopwords = ['mv', 'music video', '歌詞', '高清', 'hd', 'lyric video', 'lyrics', '版']
# Ps, Pe, Pi, Pf, Po
quotes = ['()', '[]', '《》', '【】', '（）', "“”", "''", '""']
dash = ['-', '_', '─', '－']  # 第三個是So, 其他都在word_segmentation被換成Pd: -
connectors = [',', '&', 'x']
dq = dash + quotes


if __name__ == '__main__':
    print(any('-' in s for s in dq))