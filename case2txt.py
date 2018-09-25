# -*- coding: utf-8 -*-
import argparse
import json
import os
import re

from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import pdftotree
import textract


def parseArgs():
    parser = argparse.ArgumentParser(description='Add filename of case.')
    parser.add_argument('casefile', type=str, nargs='+', help='filename of case')
    args = parser.parse_args()
    return args.casefile

def getSectionHeaders(casefile):
    tree = pdftotree.parse('/code/uploads/' + casefile, html_path=None, model_type=None, model_path=None, favor_figures=True, visualize=False)
    parsed_html = BeautifulSoup(tree, features='html.parser')
    headers = parsed_html.find_all('section_header')
    titles = []
    remove_titles = []
    footer = headers[-1].text
    for header in headers:
        title = header.text
        if len(title) < 75 and not title.isnumeric() and title[0].istitle():
            titles.append(title)
        else:
            remove_titles.append(title)
    for i in range(0, len(titles)):
        exhibit_search = re.search('xhi', titles[i])
        if exhibit_search:
            exhibit_start = i
            break
    titles = titles[:exhibit_start]
    main_title = max(set(titles), key=titles.count)
    titles = [x.strip() for x in titles if x != main_title]
    final_headers = []
    for title in titles:
        split_title = title.split(' ')
        all_titles = []
        for splits in split_title:
            if len(splits) < 4:
                all_titles.append(True)
            elif len(splits) >= 4 and splits[0].istitle():
                if re.search(':', splits):
                    all_titles.append(False)
                else:
                    all_titles.append(True)
            else:
                all_titles.append(False)
        if all(all_titles):
            final_headers.append(title)
    return main_title.strip(), footer.strip(), final_headers, remove_titles

def parsePDF(casefile):
    pdf_results = {}
    sections = []
    main_title, footer, final_headers, remove_titles = getSectionHeaders(casefile)
    pdf_text = textract.process('/code/uploads/' + casefile).decode()
    cleaned_text = cleanText(pdf_text, main_title, footer, remove_titles)
    with open('/code/results/' + casefile[:-4] + '/' + casefile[:-3] + 'txt', 'w') as text_file:
        text_file.write(cleaned_text)
    first_section = cleaned_text[cleaned_text.find(main_title):cleaned_text.find(final_headers[0])]
    sections.append({'title': 'Introduction', 'text': first_section.replace(main_title, '').strip()})
    cleaned_text = cleaned_text.replace(first_section, '')
    for i in range(0, len(final_headers) - 1):
        cleaned_text = cleaned_text.replace(main_title, '')
        section = cleaned_text[cleaned_text.find(final_headers[i]):cleaned_text.find(final_headers[i+1])]
        sections.append({'title': final_headers[i], 'text': section.strip()})
        cleaned_text = cleaned_text.replace(section, ' ')
    final_section = cleaned_text[cleaned_text.find(final_headers[-1]):cleaned_text.find('Exhibit 1')]
    sections.append({'title': final_headers[-1], 'text': final_section.strip()})
    pdf_results['title'] = main_title
    pdf_results['sections'] = sections
    return pdf_results

def fuzzy_replace(search_str, replace_str, orig_str):
    l = len(search_str.split())
    splitted = orig_str.split()
    for i in range(len(splitted)-l+1):
        test = " ".join(splitted[i:i+l])
        if fuzz.ratio(search_str, test) > 75:
            before = " ".join(splitted[:i])
            after = " ".join(splitted[i+1:])
            return before + " " + replace_str + " " + after
        else:
            return orig_str

def cleanText(pdf_text, main_title, footer, remove_titles):
    copyright_clause = "(Copyright)(.*)(permission of Harvard Business School)"
    intention_clause = "(HBS cases)(.*)(effective or ineffective management)"
    joined_text = pdf_text.replace('\n', ' ').replace('_', '').replace(footer, '').split()
    joined_text = ' '.join(joined_text)
    joined_text = re.sub(copyright_clause, '', joined_text)
    joined_text = re.sub(intention_clause, '', joined_text)
    for title in remove_titles:
        joined_text = fuzzy_replace(title, '', joined_text)
    return joined_text

def convert(casefile):
    if not os.path.isdir('/code/results/' + casefile[:-4]):
        os.mkdir('/code/results/' + casefile[:-4])
    pdf_results = parsePDF(casefile)
    print('Parsing...Done')
    with open('/code/results/' + casefile[:-4] + '/' + casefile[:-3] + 'json', 'w') as outfile:
        outfile.write(json.dumps(pdf_results))

if __name__ == '__main__':
    casefile = parseArgs()
    convert(casefile[0])
