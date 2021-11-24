#!/usr/bin/env python3
# Утилита для обучения нейронной сети на имеющихся статистических данных

import json
import pandas as pd
import numpy as np

dir_name = 'dump'
data_file_name = "db.json"


# loading data from file
def load_db(file_path):
    with open(file_path, "r") as read_file:
        db = pd.read_json(read_file)
    db = np.array(db[1])
    return db


data_base = load_db(f'{dir_name}/{data_file_name}')
