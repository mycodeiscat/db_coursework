import io
import pickle

import joblib
import pandas as pd
from matplotlib import pyplot as plt

from .base import Model
from pandas.tseries.offsets import DateOffset
from pmdarima.arima import auto_arima
from statsmodels.tsa.stattools import adfuller


class ArimaModel(Model):
    def __init__(self, train_df, test, checkpoint=False):
        if checkpoint:
            self.model = joblib.load(checkpoint)
        else:
            self.model = None
        self.train_df = train_df
        self.test = test

    def train(self):
        self.model = auto_arima(self.train_df,
                                start_p=0, d=1, start_q=0,
                                max_p=4, max_d=4, max_q=4,
                                start_P=0, D=1, start_Q=0,
                                max_P=1, max_D=1, max_Q=1, m=96,
                                seasonal=True,
                                error_action='warn', trace=True,
                                supress_warning=True, stepwise=True,
                                random_state=20, n_fits=1)
        with open('model.pkl', 'wb') as pkl:
            pickle.dump(self.model, pkl)

    def predict(self):
        future_dates = [self.test.index[-1] + DateOffset(minutes=x) for x in range(0, 2910, 15)]
        prediction = pd.DataFrame(self.model.predict(n_periods=96), index=self.test.index)
        prediction.columns = ['predicted_yield']

        fig, ax = plt.subplots(ncols=2, nrows=1, dpi=100, figsize=(17, 5))
        ax[0].plot(self.train_df, label='Train', color='navy')
        ax[0].plot(self.test, label='Test', color='darkorange')
        ax[0].plot(prediction, label='Prediction', color='green')
        ax[0].legend()
        ax[0].set_title('Forecast on test set', size=17)
        ax[0].set_ylabel('kW', color='navy', fontsize=17)

        f_prediction = pd.DataFrame(self.model.predict(n_periods=194), index=future_dates)
        f_prediction.columns = ['predicted_yield']
        ax[1].plot(self.test, label='Original data', color='navy')
        ax[1].plot(f_prediction, label='18th & 19th June', color='green')
        ax[1].legend()
        ax[1].set_title('Next days forecast', size=17)
        plt.show()

    def compute_metrics(self):
        pass

    def get_params(self):
        self.model.summary()
