#!/home/long96nb/miniconda3/bin/python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.getcwd())

import os
from subprocess import *
import data_read_write

rover_path = "/home/long96nb/Desktop/SCTK/bin/"

out_path = "/home/long96nb/Desktop/TextSum_Voting/out_voting/"

in_trans = "/home/long96nb/Desktop/TextSum_Voting/output/trans_sl_w2v/"
in_bilstm = "/home/long96nb/Desktop/TextSum_Voting/output/bilstm_pn_w2v/"
in_bandit = "/home/long96nb/Desktop/TextSum_Voting/output/bandit/"

def voting_2_method(hybrid, end2end, outfile):
    call([rover_path + './rover', '-h', hybrid, 'ctm', '-h', end2end, 'ctm', '-o', outfile, '-m', 'oracle'])

def voting_3_method(trans, bilstm, bandit, outfile):
    call([rover_path + './rover', '-h', trans, 'ctm', '-h', bilstm, 'ctm',
          '-h', bandit, 'ctm', '-o', outfile, '-m', 'oracle'])

if __name__ == "__main__":
    bandit_files = data_read_write.list_files(in_bandit)

    for item in bandit_files:

        print("voting for the file...", item)
        infile_bandit = in_bandit + item
        infile_trans = in_trans + item
        infile_bilstm = in_bilstm + item

        out_file = out_path + item

        #voting_2_method(infile_hybrid, in_end2end, out_file)
        voting_3_method(infile_trans, infile_bilstm, infile_bandit, out_file)

        #break