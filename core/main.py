import pandas as pd

from db import db, connect
from utils.dataloaders import SolarGenerationLoader
from utils.preprocessors import preprocessing, forecast_preprocessing
from utils.analysis import GenerationReportBuilder
from datetime import datetime
from models.arima import ArimaModel
from utils.controller import user_interface

if __name__ == '__main__':
    connect()
    # loader = SolarGenerationLoader('D:\Py_projects\db_coursework\data\\raw\Plant_1_Generation_Data.csv', [preprocessing])
    user_interface()
    # loader.load('solar', preprocessing=True)
    # query = loader.get('solar', {'DATE_TIME': {
    #     "$gte": datetime.strptime("2020-05-15", '%Y-%m-%d'),
    #     "$lt": datetime.strptime("2020-06-15", '%Y-%m-%d')
    # }})
    # print("Generating report....")
    # reporter = GenerationReportBuilder(loader)
    # reporter.generate_report(('2020-05-17', '2020-06-01'))
    # df = pd.DataFrame(list(query))
    # pred_gen = forecast_preprocessing(df)
    # train = pred_gen[:192]
    # test = pred_gen[-96:]
    # model = ArimaModel(train, test, 'D:\Py_projects\db_coursework\core\models\\arima.pkl')
    # model.train()
    # model.predict()
    # model.get_params()
    # for q in query:
    #     print(q)
    # loader.load()
