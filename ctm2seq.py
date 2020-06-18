__author__ = 'ryan.nguyen'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


sys.path.append(os.getcwd())

import os
from subprocess import *
import data_read_write

def ctm2seq_file_withalpha(file):
    data = data_read_write.read_data(file)

    seq = ""
    for line in data:
        if str(line).__contains__("<ALT_BEGIN>") or str(line).__contains__("<ALT>") or str(line).__contains__("<ALT_END>"):
            continue

        arr = str(line).split(" ")
        ch = arr[4]
        seq += ch

    return str(seq).strip()

def ctm2seq_file(file):
    data = data_read_write.read_data(file)

    seq = ""
    for line in data:
        if str(line).__contains__("<ALT_BEGIN>") or str(line).__contains__("<ALT>") or str(line).__contains__("<ALT_END>"):
            continue

        arr = str(line).split(" ")
        ch = arr[4]
        if ch != "@":
            seq += ch

    return str(seq).strip()

if __name__ == "__main__":
    ctm_path = "/Users/minhtien/PyCharmProjects/rossa/data/csj_voting/csj_new_augmentation/out_3/"
    ctm_files = data_read_write.list_files(ctm_path)
    print(len(ctm_files))

    original_path = "/Users/minhtien/PyCharmProjects/rossa/data/csj_voting/csj_new_augmentation/hybrid_end2end_google.txt"
    data = data_read_write.read_data_json(original_path)["data"]
    print(len(data))

    voting_3_path = "/Users/minhtien/PyCharmProjects/rossa/data/csj_voting/csj_new_augmentation/voting_3_hybrid_end2end_google.txt"
    data_voting_3 = data_read_write.read_data_json(voting_3_path)["data"]

    data_json = []

    for item in data:
        voting = ""
        audio_path = item["audio_path"]
        print(audio_path)
        for ctm_f in ctm_files:
            wav_file = str(ctm_f).replace("ctm", "wav")

            if str(audio_path).__contains__(str(wav_file)):

                for item_voting in data_voting_3:
                    path = item_voting["audio_path"]
                    arr = str(path).split("/")
                    file_name = arr[len(arr)-1]

                    if str(audio_path).__contains__(file_name):

                        in_ctm_file = ctm_path + ctm_f
                        voting = ctm2seq_file(in_ctm_file)
                        print("running here...", voting)
                        print(wav_file)
                        break

        #break

        end2end_predict = item["end2end"]
        google_predict = item["google"]
        hybrid_predict = item["hybrid"]
        ground_truth = item["ground_truth"]

        if voting == "":
            continue

        entry = {
            "audio_path": audio_path,
            "ground_truth": ground_truth,
            "hybrid_predict": hybrid_predict,
            "end2end_predict": end2end_predict,
            "google_predict": google_predict,
            "voting": voting
        }

        data_json.append(entry)
        #break
        json = {
            "data": data_json
        }

    out_file = "/Users/minhtien/PyCharmProjects/rossa/data/csj_voting/csj_new_augmentation/voting_3.txt"
    data_read_write.write_data_json(out_file, json)