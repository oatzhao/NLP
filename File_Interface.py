__author__ = 'yan.zhao'

import csv, pickle

def read_csv(path):
    file = open(path, 'r')
    reader = csv.reader(file)
    data = [row for row in reader]
    return data

def load_pickle(path):
    file = open(path, 'rb')
    data = pickle.load(file)
    file.close()
    return data

def save_picle(data, path):
    file = open(path, 'wb')
    pickle.dump(data, file)
    file.close()