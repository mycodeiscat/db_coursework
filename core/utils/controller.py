from matplotlib import pyplot as plt

from core.db import db, connect
from .dataloaders import SolarGenerationLoader
from .preprocessors import preprocessing, forecast_preprocessing
from .analysis import GenerationReportBuilder
from datetime import datetime
from core.models.arima import ArimaModel
import pandas as pd


def query(start, end, loader):
    q = loader.get('solar', {'DATE_TIME': {
        "$gte": datetime.strptime(start, '%Y-%m-%d'),
        "$lt": datetime.strptime(end, '%Y-%m-%d')
    }})
    df = pd.DataFrame(list(q))
    return df


def prediction(start, end, loader, out):

    df = query(start, end, loader)
    pred_gen = forecast_preprocessing(df)
    train = pred_gen[:192]
    test = pred_gen[-96:]
    if out:
        helper(train, test)
        return
    model = ArimaModel(train, test, 'D:\Py_projects\db_coursework\core\models\\arima.pkl')
    # model.train()
    model.predict()
    model.get_params()


def get_stats(start, end, loader):
    print("Calculating max daily generation values...")
    df = query(start, end, loader)
    stat = df.copy()
    stat['day'] = stat['DATE_TIME'].dt.date
    stat = stat.groupby('day').sum()
    stat.sort_values(by=['DAILY_YIELD'], ascending=False, inplace=True)
    print(stat)
    pass


def analysis():
    pass


def user_interface():
    inp = None
    loader = SolarGenerationLoader('D:\Py_projects\db_coursework\data\\raw\Plant_1_Generation_Data.csv',
                                   [preprocessing])
    while True:
        inp = input()
        if "graphs" in str(inp):
            print("Start date:\n")
            start = input()
            print("End date:\n")
            end = input()

            print("Generating report....")
            reporter = GenerationReportBuilder(loader)
            reporter.generate_report((start, end))
        if "forecast" in str(inp):
            print("Start date:\n")
            start = input()
            print("End date:\n")
            end = input()
            prediction(start, end, loader, out=True)
        if "stats" in str(inp):
            print("Start date:\n")
            start = input()
            print("End date:\n")
            end = input()
            get_stats(start, end, loader)


def helper(train, test):
    prediction = pd.read_csv('D:\Py_projects\db_coursework\\assets\out.csv')
    prediction.columns = ['predicted_yield']


    fig, ax = plt.subplots(ncols=2, nrows=1, dpi=100, figsize=(17, 5))
    ax[0].plot(train, label='Train', color='navy')
    ax[0].plot(test, label='Test', color='darkorange')
    ax[0].plot(prediction, label='Prediction', color='green')
    ax[0].legend()
    ax[0].set_title('Forecast on test set', size=17)
    ax[0].set_ylabel('kW', color='navy', fontsize=17)
    print(prediction)
    plt.show()