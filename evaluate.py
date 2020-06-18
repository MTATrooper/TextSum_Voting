import os
import sys
from create_ctm import LoadHtml
from data_read_write import write_data
import glob
from pyrouge import Rouge155
from pyrouge.utils import log

import tempfile
from os.path import join
import logging
import subprocess as sp


VOTE_OUT_PATH = 'evalua/vote'
REF_OUT_PATH = 'evalua/ref'

VOTE_IN_PATH = 'out_voting/'
REF_IN_PATH = '/home/long96nb/Downloads/CNN_DM_test_output/'

_ROUGE_PATH = '/home/long96nb/pyrouge/tools/ROUGE-1.5.5/'

def create_output(vote_path, ref_path):
    for path in os.listdir(vote_path):
        print('vote file: ' + path)
        doc = ""
        with open(os.path.join(vote_path, path), encoding='utf8') as fr:
            lines = fr.readlines()
            for line in lines:
                words = line.split()
                if words[2] != '*' and words[4] != '@':
                    doc += words[4] + " "
        with open(os.path.join(VOTE_OUT_PATH, path.split('.')[0] + ".txt"), 'w') as wr:
            wr.write(doc)

    for path in glob.glob(ref_path + 'ref.*.txt'):
        print('reference:' + path)
        lstword = LoadHtml(path)
        doc = ' '.join(lstword)
        with open(os.path.join(REF_OUT_PATH, path.split('.')[-2] + ".txt"), 'w') as wr:
            wr.write(doc)

def evaluate(vote_path, ref_path):
    r = Rouge155(rouge_dir = _ROUGE_PATH)
    # r.system_dir = '/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/system'
    # r.model_dir = '/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/model'

    r.system_dir = vote_path
    r.model_dir = ref_path

    r.system_filename_pattern = "(\d+).txt"
    r.model_filename_pattern = "#ID#.txt"

    output = r.convert_and_evaluate()
    print(output)
    with open('evalua/result.txt', 'w') as f:
        f.write(output)

def eval_rouge(dec_dir, ref_dir):
    """ evaluate by original Perl implementation"""
    # silence pyrouge logging
    assert _ROUGE_PATH is not None
    log.get_global_console_logger().setLevel(logging.WARNING)
    dec_pattern = '(\d+).txt'
    ref_pattern = '#ID#.txt'
    cmd = '-c 95 -r 1000 -l 61 -n 2 -m'
    with tempfile.TemporaryDirectory() as tmp_dir:
        Rouge155.convert_summaries_to_rouge_format(
            dec_dir, join(tmp_dir, 'dec'))
        Rouge155.convert_summaries_to_rouge_format(
            ref_dir, join(tmp_dir, 'ref'))
        Rouge155.write_config_static(
            join(tmp_dir, 'dec'), dec_pattern,
            join(tmp_dir, 'ref'), ref_pattern,
            join(tmp_dir, 'settings.xml'), system_id=1
        )
        cmd = (join(_ROUGE_PATH, 'ROUGE-1.5.5.pl')
               + ' -e {} '.format(join(_ROUGE_PATH, 'data'))
               + cmd
               + ' -a {}'.format(join(tmp_dir, 'settings.xml')))
        output = sp.check_output(cmd.split(' '), universal_newlines=True)
    print(output)
    with open('evalua/result.txt', 'w') as f:
        f.write(output)

if __name__ == '__main__':
    #create_output(VOTE_IN_PATH, REF_IN_PATH)
    #evaluate(VOTE_OUT_PATH, REF_OUT_PATH)
    eval_rouge(VOTE_OUT_PATH, REF_OUT_PATH)