#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
# from imp import reload
#
# reload(sys)
# sys.setdefaultencoding("utf-8")

sys.path.append(os.getcwd())

import json, codecs
import random
import xml.etree.ElementTree as ET
from os import listdir
from xml.dom import minidom


def read_data_json(filename):
    with open(filename) as f:
        data = json.load(f)

    return data

def getting_training_sents(data):
    lst_data = []
    for item in data:
        count = 0
        for word, label in item:
            if label == "E":
                count += 1
        if count >= 2:
            lst_data.append(item)

    return lst_data

def read_data_nikko_predict(filename):
    lst_data = []
    f_in = filename
    f = open(f_in, "r")
    data = f.readlines()

    for line in data:
        # print(len(line))
        if len(line) == 1:
            continue
        if str(line).__contains__("CER"):
            break
        lst_data.append(line)
    return lst_data


def read_data_nikko_gold(filename):
    lst_data = []
    f_in = filename
    f = open(f_in, "r")
    data = f.readlines()

    for line in data:
        if len(line) == 1:
            continue
        lst_data.append(line)
    return lst_data


def list_files(path):
    return listdir(path)


def write_data_json(filename, data):
    with open(filename, mode="w", encoding="utf8") as f:
        json.dump(data, ensure_ascii=False, fp=f, sort_keys=True, indent=4)

def write_code(filename, data):
    with codecs.open(filename, 'w', 'utf8') as f:
        f.write(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))


def read_data(filename):
    f_in = filename
    f = open(f_in, "r")
    data = f.readlines()
    return data

def write_data_beam(filename):
    data = read_data(filename)
    print(len(data))

    lst_data = []
    count = 0
    tmp = []

    for idx, item in enumerate(data):
        arr = str(item).split(":")
        #name = arr[0]
        predict = arr[1]
        #gold = str(arr[2]).strip()

        #if idx == 0:
        #    tmp.append(predict)
        #    continue

        if count == 8:
            name = str(data[idx-1]).split(":")[0]
            gold = str(data[idx - 1]).split(":")[2].strip()
            entry = {
                "audio_name": name,
                "ground_truth": gold,
                "predict": tmp
            }
            lst_data.append(entry)
            tmp = []
            count = 0
        if count < 8:
            tmp.append(predict)
            count += 1

    json = {
        "data": lst_data
    }

    return json

def removing_short_sentences(filename):
    data = read_data_json(filename)["data"]
    print(len(data))

    lst_data = []
    for item in data:
        gold = item["ground_truth"]
        if len(gold) > 4:
            lst_data.append(item)

    print(len(lst_data))
    json = {
        "data": lst_data
    }

    return json

def removing_duplicate_candidates(filename):
    data = read_data_json(filename)["data"]
    print(len(data))

    lst_data = []
    for item in data:
        audio_name = item["audio_name"]
        ground_truth = item["ground_truth"]
        predicts = item["predict"]

        lst_tmp = []
        for pred in predicts:
            if not lst_tmp.__contains__(pred):
                lst_tmp.append(pred)

        entry = {
            "audio_name": audio_name,
            "ground_truth": ground_truth,
            "predict": lst_tmp
        }
        lst_data.append(entry)

    js = {
        "data": lst_data
    }

    return js

def read_xml_file_ET(path):
    # with open(path) as xml:
    # data = read_data(path)
    root = ET.parse(path).getroot()
    return root


def read_xml_file(path):
    with open(path) as xml:
        xmldoc = minidom.parse(xml)
    return xmldoc

def read_ja_dict(path):
    data = read_data_json(path)["data"]
    lst_dict = []
    for item in data:
        kanji = item["kanji"]
        lst_dict.append(kanji)

    return lst_dict

def write_data(filename, data):
    f_out_path = filename
    f_out = open(f_out_path, "w")
    for line in data:
        f_out.write(str(line) + "\n")
        f_out.flush()

    f_out.close()


def write_data_append(filename, data):
    f_out_path = filename
    f_out = open(f_out_path, "a")
    for line in data:
        f_out.write(str(line) + "\n")
        f_out.flush()

    f_out.close()

def get_50k_data(filename):
    data = read_data_json(filename)["data"]
    print(len(data))
    lst_data = []

    for count in range(len(data)):
        if len(lst_data) == 50000:
            break
        idx = random.randint(0, len(data)-1)
        lst_data.append(data[idx])

    print(len(lst_data))
    json = {
        "data": lst_data
    }
    return json

def get_ground_truth(filename):
    data = read_data_json(filename)["data"]
    lst_data = []
    for item in data:
        audio_name = item["audio_name"]
        ground_truth = item["ground_truth"]

        entry = {
            "audio_name": audio_name,
            "ground_truth": ground_truth
        }
        lst_data.append(entry)

    lst_test = []
    for count in range(len(lst_data)):
        if len(lst_test) == 5000:
            break
        idx = random.randint(0, len(lst_data) - 1)
        lst_test.append(lst_data[idx])

    lst_train = []
    for item in lst_data:
        if not lst_test.__contains__(item):
            lst_train.append(item)

    json_train = {
        "data": lst_train
    }
    json_test = {
        "data": lst_test
    }
    return json_train, json_test

def remove_duplicate_words(file1, file2):
    lst70k = read_data(file1)
    lst240k = read_data(file2)
    lst_result = []
    for w in lst240k:
        if not lst70k.__contains__(w):
            lst_result.append(w)

    return lst_result

if __name__ == "__main__":
    infile1 = "data/csj_550/550lectures_ryan.json"

    data = read_data_json(infile1)["data"]
    print(len(data))