from bs4 import BeautifulSoup
import regex as re
from nltk import word_tokenize
import glob
from ctm_out import ctm_making
import data_read_write
import sys
import os
import unicodedata as ud

def syllablize(text):
    """
    tách thành các âm
    """
    text = ud.normalize('NFC', text)
    digits = r"[\d+\.,]+"
    email = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    #email = r"\S+@\S+"
    web = r'((www\.[^\s]+)|(https?://[^\s]+))'
    datetime = [
        r"\d{1,2}\/\d{1,2}(\/\d+)?",
        r"\d{1,2}-\d{1,2}(-\d+)?",
    ]
    word = r"\w+"
    owned = r"\w+'s"
    abbreviations = [
        r"[A-ZĐ]+\.",
        r"Tp\.",
        r"Mr\.", r"Mrs\.", r"Ms\.",
        r"Dr\.", r"ThS\."
    ]
    patterns = []
    patterns.extend(abbreviations)
    patterns.extend([web, email])
    patterns.extend(datetime)
    patterns.extend([owned, digits, word])
    patterns = "(" + "|".join(patterns) + ")"
    if sys.version_info < (3, 0):
        patterns = patterns.decode('utf-8')
    tokens = re.findall(patterns, text, re.UNICODE)
    return [token[0] for token in tokens]

def LoadTxt(path):
    #words = []
    with open(path, encoding='utf8') as fr:
        words = fr.read()
    words = words.replace("-lrb-", "")
    words = words.replace("-rrb-", "")
    words = words.replace(" 's", "'s")
    lstword = syllablize(words)
    return lstword
def LoadHtml(path):
    with open(path,'r') as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    doc = ""
    for x in soup.find_all('a', {'id': '1'}):
        doc += x.text + " "
    for x in soup.find_all('a', {'id': '2'}):
        doc += x.text + " "
    for x in soup.find_all('a', {'id': '3'}):
        doc += x.text
    doc = doc.replace("-lrb-", "")
    doc = doc.replace("-rrb-", "")
    doc = doc.replace(" 's", "'s")
    lstword = syllablize(doc)
    return lstword

if __name__ == '__main__':
    out_bandit = 'output/bandit/'
    out_tran_sl = 'output/trans_sl_w2v/'
    out_bilstm_pn = 'output/bilstm_pn_w2v/'
    in_bandit = '/home/long96nb/Downloads/CNN_DM_test_output/'
    in_trans_sl = '/home/long96nb/Documents/Trans_SL_W2v/ckpt-0.306844-33000/'
    in_bilstm_pn = '/home/long96nb/Documents/BiLSTM_PN_W2V/ckpt-2.653242-33000/'
    if str(sys.argv[1]) == 'bandit':
        for path in glob.glob(in_bandit + 'hyp.*.txt'):
            print(path)
            lst_text = LoadHtml(path)
            lst_bandit = ctm_making(path.split('.')[-2], lst_text)
            data_read_write.write_data(out_bandit + path.split('.')[-2] + '.ctm', lst_bandit)
    elif str(sys.argv[1]) == 'trans_sl_w2v':
        for path in os.listdir(in_trans_sl):
            print(path)
            lst_text = LoadTxt(in_trans_sl + path)
            lst_trans = ctm_making(path.split('.')[0], lst_text)
            data_read_write.write_data(out_tran_sl + path.split('.')[0] + '.ctm', lst_trans)
    else:
        for path in os.listdir(in_bilstm_pn):
            print(path)
            lst_text = LoadTxt(in_bilstm_pn + path)
            lst_bilstm = ctm_making(path.split('.')[0], lst_text)
            data_read_write.write_data(out_bilstm_pn + path.split('.')[0] + '.ctm', lst_bilstm)



