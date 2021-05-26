from typing import AnyStr, List

# class MissingImputation:
#     def __init__(self, strategy: AnyStr, columns: List):
#         self.strategy = strategy
#         self.columns = columns
#
#     def __call__(self, df):
#         for column in self.columns:
import pandas as pd


def preprocessing(df):
    df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], format='%d-%m-%Y %H:%M')
    df.dropna(axis=1)
    return df


def forecast_preprocessing(df):
    pred_gen = df.copy()
    pred_gen = pred_gen.groupby('DATE_TIME').sum()
    pred_gen = pred_gen['DAILY_YIELD'][-288:].reset_index()
    pred_gen.set_index('DATE_TIME', inplace=True)
    return pred_gen
