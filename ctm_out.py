#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
# from imp import reload
#
# reload(sys)
# sys.setdefaultencoding("utf-8")

sys.path.append(os.getcwd())
import data_read_write

def ctm_making(audio_name, seq):
    lst_char = list(seq)
    #print(lst_char)
    lst = []
    for idx, ch in enumerate(lst_char):
        start_time = idx
        dur = 0.1
        entry = str(audio_name) + " A " + str(start_time) + " " + str(dur) + " " + str(ch)
        lst.append(entry)

    return lst

if __name__ == "__main__":
    in_file = "/Users/minhtien/PyCharmProjects/rossa/data/csj_voting/csj_new_augmentation/hybrid_end2end_google.txt"
    data = data_read_write.read_data_json(in_file)["data"]

    for item in data:
        audio_path = item["audio_path"]
        arr = str(audio_path).split("/")
        audio_name = str(arr[len(arr)-1]).replace(".wav", "")
        print(audio_name)

        ground_truth = item["ground_truth"]
        hybrid_predict = item["hybrid"]
        end2end_predict = item["end2end"]
        google_predict = item["google"]

        #print(hybrid_predict)
        #print(end2end_predict)
        #print(google_predict)

        lst_hybrid = ctm_making(audio_name, hybrid_predict)
        lst_end2end = ctm_making(audio_name, end2end_predict)
        lst_google = ctm_making(audio_name, google_predict)

        #for id in lst_hybrid:
        #    print(id)

        out_hybrid = "/Users/minhtien/PyCharmProjects/rossa/data/csj_voting/csj_new_augmentation/hybrid/" + audio_name + ".ctm"
        out_end2end = "/Users/minhtien/PyCharmProjects/rossa/data/csj_voting/csj_new_augmentation/end2end/" + audio_name + ".ctm"
        out_google = "/Users/minhtien/PyCharmProjects/rossa/data/csj_voting/csj_new_augmentation/google/" + audio_name + ".ctm"

        data_read_write.write_data(out_hybrid, lst_hybrid)
        data_read_write.write_data(out_end2end, lst_end2end)
        data_read_write.write_data(out_google, lst_google)

        #break

    print(len(data))
