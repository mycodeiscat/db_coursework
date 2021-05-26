import os
from typing import Dict, AnyStr, Any
from typing import List

from bson import ObjectId

from core.db import db
import numpy as np
import fastai
import pandas as pd


class SolarGenerationLoader():
    def __init__(self, path: AnyStr, preprocessors: List):
        self.path = path
        self.preprocessors = preprocessors

    def get(self, table, params):
        document = db[table].find(params)
        return document

    def load(self, table, preprocessing: bool = False):
        generation_df = pd.read_csv(self.path)
        if preprocessing:
            for pp in self.preprocessors:
                pp(generation_df)
        generation_dict = generation_df.to_dict("records")
        db[table].insert_many(generation_dict)
        pass


