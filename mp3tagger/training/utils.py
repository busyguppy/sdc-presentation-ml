import pickle
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from mp3tagger import tools


class NullValueException(Exception):
    pass


def has_null(df: DataFrame):
    return df.isnull().to_numpy().any()


def load_data():
    path_dataset = tools.data_file('dataset.pkl')
    fvs = [y for x in pickle.load(open(path_dataset, 'rb')) for y in x]
    df = pd.DataFrame(fvs)
    return df


le_label = None
le_quote_type = None
le_str = None
le_tag = None

def preprocessing(df: DataFrame):
    # 詳細資料清理、轉換過程參考Data Preprocessing.ipynb

    le_label = OrdinalEncoder()
    df[['tag', 'str', 'quote_type']] = le_label.fit_transform(
        df[['tag', 'str', 'quote_type']].to_numpy())

    if df['label'].isnull().to_numpy().any():
        raise NullValueException
    else:
        le_label = LabelEncoder()
        df['label'] = le_label.fit_transform(df.label.to_numpy())

    if df['in_quote'].isnull().to_numpy().any():
        raise NullValueException
    else:
        df['in_quote'] = df['in_quote'].astype(int)

    if df['i_slot_between_dash'].isnull().to_numpy().any():
        raise NullValueException

    if df['right_lo_seg_cnt'].isnull().to_numpy().any():
        raise NullValueException

    if df['right_seg_length'].isnull().to_numpy().any():
        raise NullValueException

    if df['title_len'].isnull().to_numpy().any():
        raise NullValueException

    if df['left_lo_seg_cnt'].isnull().to_numpy().any():
        raise NullValueException

    if df['seg_len'].isnull().to_numpy().any():
        raise NullValueException

    if df['str_len_left'].isnull().to_numpy().any():
        raise NullValueException

    if df['i_seg'].isnull().to_numpy().any():
        raise NullValueException

    return df

# def preprocessing(df: DataFrame):
#     # 詳細資料清理、轉換過程參考Data Preprocessing.ipynb
#
#     # Label encode留到最後再做
#     if df['label'].isnull().to_numpy().any():
#         raise NullValueException
#     else:
#
#         le_label = LabelEncoderExt()
#         le_label.fit(df.label.to_numpy())
#         df['label'] = le_label.transform(df.label.to_numpy())
#
#     if df['quote_type'].isnull().to_numpy().any():
#         raise NullValueException
#     else:
#         le_quote_type = LabelEncoder()
#         le_quote_type.fit(df.quote_type.to_numpy())
#         df['quote_type'] = le_quote_type.transform(df.quote_type.to_numpy())
#
#     if df['in_quote'].isnull().to_numpy().any():
#         raise  NullValueException
#     else:
#         df['in_quote'] = df['in_quote'].astype(int)
#
#     if df['i_slot_between_dash'].isnull().to_numpy().any():
#         raise NullValueException
#
#     if df['right_lo_seg_cnt'].isnull().to_numpy().any():
#         raise NullValueException
#
#     if df['right_seg_length'].isnull().to_numpy().any():
#         raise NullValueException
#
#     if df['title_len'].isnull().to_numpy().any():
#         raise NullValueException
#
#     if df['left_lo_seg_cnt'].isnull().to_numpy().any():
#         raise NullValueException
#
#     if df['seg_len'].isnull().to_numpy().any():
#         raise NullValueException
#
#     if df['str_len_left'].isnull().to_numpy().any():
#         raise NullValueException
#
#     if df['i_seg'].isnull().to_numpy().any():
#         raise NullValueException
#
#     if df['str'].isnull().to_numpy().any():
#         raise NullValueException
#     else:
#         le_str = CategoricalEncoder()
#         df['str'] = le_str.fit_transform(df.str.to_numpy())
# #         print('Segment字串總共有{}種！'.format(len(e1.classes_)))
#
#     if df['tag'].isnull().to_numpy().any():
#         raise NullValueException
#     else:
#         le_tag = LabelEncoder()
#         df['tag'] = le_tag.fit_transform(df.tag.to_numpy())
#     return df

if __name__ == '__main__':
    # train_baseline()

    # train_two_layer_mcp()
    t = 1