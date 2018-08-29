# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
import argparse
import json

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


def parseArgs():
    parser = argparse.ArgumentParser(description='Add filename of case.')
    parser.add_argument('casefile', type=str, nargs='+', help='filename of case')
    parser.add_argument('-v', '--verbose', help='increase output verbosity',
                        action='store_true')
    args = parser.parse_args()
    return args.casefile, args.verbose

def summarize(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    stemmer = Stemmer("english")

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words("english")

    for sentence in summarizer(parser.document, 5):
        sentence = str(sentence).replace(',', '').split()
        for words in sentence:
            words = words.strip()
            if not words[0].isnumeric():
                start_word = words
                break
        sentence = sentence[sentence.index(start_word):]
        print(' '.join(sentence))

if __name__ == "__main__":
    casefile, verbose = parseArgs()
    with open(casefile[0][:-3] + 'json', 'r') as infile:
        case = json.loads(infile.read())
        for section in case['sections']:
            print(section['title'])
            print('\n')
            summarize(section['text'])
            print('\n')
            print('-----------------------------------------------------------')
