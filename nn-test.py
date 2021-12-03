# Утилита для обучения нейронной сети на имеющихся статистических данных

import json
import pandas as pd
import numpy as np
import os
import time
import re

from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense, Dropout, SpatialDropout1D, BatchNormalization, Embedding, Flatten, Activation
from tensorflow.keras.layers import SimpleRNN, GRU, LSTM, Bidirectional, Conv1D, MaxPooling1D, GlobalMaxPooling1D
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator

dir_name = 'dump'
data_file_name = "db.json"


# loading data from file
def load_db(file_path):
    with open(file_path, "r") as read_file:
        database = pd.read_json(read_file)
    return database[1]


# convert three numbers to sequence with 10 numbers 1 and 0
# each 1 show number equal position have or not
def to_binar(data):
    out_data = []
    for d in data:
        element = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        element[d // 100] = 1
        dd = d % 100
        element[dd // 10] = 1
        dd = dd % 10
        element[dd] = 1
        out_data.append(element)
    out_data = np.array(out_data)
    return out_data


# Функция визуализации результата предсказания сети и верных ответов

def show_predict(y_pred, y_true,  # прогноз данных и исходный ряд
                 start,  # точка ряда, с которой начинается отрисовка графика
                 length,  # количество точек для отрисовки графика
                 title=''):
    for i in range(10):
        print(f'Real: {y_true[i]} \n'
              f'Pred: {y_pred[i]} \n'
              f'Diff: {abs(y_true[i] - y_pred[i])}')


# Функция визуализации результата работы сети
def eval_net(model,  # модель
             x_test, y_test,  # тестовая выборка
             start=0, length=100,  # параметры отображения графиков
             title=''):
    # Получение денормализованного предсказания и данных базового ряда
    y_pred = model.predict(x_test)

    # приводим данные предикта к округленным значенияс 1 и 0
    # три максимальных числа приводим к 1 остальные обращаем в 0
    for i in range(y_pred.shape[0]):
        for j in range(7):
            y_pred[i, np.argmin(y_pred[i])] = 2
        for j in range(10):
            if y_pred[i, j] == 2:
                y_pred[i, j] = 0
            else:
                y_pred[i, j] = 1

    # Отрисовка графика сопоставления базового и прогнозного рядов
    show_predict(y_pred, y_test, start, length,
                 title=f'{title}: Сопоставление базового и прогнозного рядов на {i + 1} шагов вперед')


db = []
data = load_db(f'{dir_name}/{data_file_name}')
for i in range(len(data)):
    for j in range(len(data[i])):
        db.append(data[i][j][0])

db = np.array(db)
print(db.shape)

x_data = db[:-1]
y_data = db[1:]
print(x_data.shape)

x_data = to_binar(x_data)
y_data = to_binar(y_data)
print(x_data.shape)

SEQ_LEN = 300
TEST_LEN = 10000
BATCH_SIZE = 40
TRAIN_LEN = x_data.shape[0] - (2 * SEQ_LEN) - TEST_LEN
print(TRAIN_LEN)

train_datagen = TimeseriesGenerator(x_data,
                                    y_data,
                                    length=SEQ_LEN,
                                    stride=1,
                                    sampling_rate=1,
                                    batch_size=BATCH_SIZE,
                                    end_index=TRAIN_LEN)
# validation
val_datagen = TimeseriesGenerator(x_data,
                                  y_data,
                                  length=SEQ_LEN,
                                  stride=1,
                                  sampling_rate=1,
                                  batch_size=BATCH_SIZE,
                                  start_index=(2 * SEQ_LEN) + TRAIN_LEN)

# Проверка формы выдаваемого генератором результата
print(f'Train batch x: {train_datagen[0][0].shape}, y: {train_datagen[0][1].shape}')

# Генератор тестовой выборки, генерирует один батч на всю выборку
test_datagen = TimeseriesGenerator(x_data,
                                   y_data,
                                   length=SEQ_LEN,
                                   stride=1,
                                   sampling_rate=1,
                                   batch_size=TEST_LEN,
                                   start_index=(2 * SEQ_LEN) + TRAIN_LEN)

# Формирование тестовой выборки из генератора
x_test, y_test = test_datagen[0]

# Проверка формы тестовой выборки
print(f'Test x: {x_test.shape}, y: {y_test.shape}')

model = Sequential()

model.add(Conv1D(512, 10, input_shape=x_test.shape[1:], activation='relu'))
model.add(Flatten())
model.add(Dropout(0.3))
model.add(BatchNormalization())
model.add(Dense(256, activation='tanh'))
model.add(BatchNormalization())
model.add(Dense(128, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(y_test.shape[1], activation='softmax'))

model.summary()

checkpoint_filepath = dir_name + '/checkpoint.h5'

if os.path.exists(checkpoint_filepath):
    model.load_weights(checkpoint_filepath)

eval_net(model, x_test, y_test)