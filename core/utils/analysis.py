from datetime import datetime
from typing import Tuple

from .dataloaders import SolarGenerationLoader

import matplotlib.pyplot as plt
import pandas as pd


class GenerationReportBuilder:
    def __init__(self, loader: SolarGenerationLoader):
        self.db = loader

    def generate_report(self, date: Tuple):
        df = pd.DataFrame(list(self.db.get('solar', {'DATE_TIME': {
            "$gte": datetime.strptime(date[0], '%Y-%m-%d'),
            "$lt": datetime.strptime(date[1], '%Y-%m-%d')
        }})))

        df_gen = df.groupby('DATE_TIME').sum().reset_index()
        df_gen['time'] = df_gen['DATE_TIME'].dt.time

        fig, ax = plt.subplots(ncols=2, nrows=1, dpi=100, figsize=(20, 5))
        # daily yield plot
        df_gen.plot(x='DATE_TIME', y='DAILY_YIELD', color='navy', ax=ax[0])
        # AC & DC power plot
        df_gen.set_index('time').drop('DATE_TIME', 1)[['AC_POWER', 'DC_POWER']].plot(style='o', ax=ax[1])

        ax[0].set_title('Daily yield', )
        ax[1].set_title('AC power & DC power during day hours')
        ax[0].set_ylabel('kW', color='navy', fontsize=17)
        plt.show()
        daily_gen = df.copy()
        daily_gen['date'] = daily_gen['DATE_TIME'].dt.date

        daily_gen = daily_gen.groupby('date').sum()

        fig, ax = plt.subplots(ncols=2, dpi=100, figsize=(20, 5))
        daily_gen['DAILY_YIELD'].plot(ax=ax[0], color='navy')
        daily_gen['TOTAL_YIELD'].plot(kind='bar', ax=ax[1], color='navy')
        fig.autofmt_xdate(rotation=45)
        ax[0].set_title('Daily Yield')
        ax[1].set_title('Total Yield')
        ax[0].set_ylabel('kW', color='navy', fontsize=17)

        plt.show()
