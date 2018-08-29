# -*- coding: utf-8 -*-
import argparse
import json
import os
import re

from bs4 import BeautifulSoup
import pdftotree
import textract


def parseArgs():
    parser = argparse.ArgumentParser(description='Add filename of case.')
    parser.add_argument('casefile', type=str, nargs='+', help='filename of case')
    parser.add_argument('-v', '--verbose', help='increase output verbosity',
                        action='store_true')
    args = parser.parse_args()
    return args.casefile, args.verbose

def getSectionHeaders(casefile):
    tree = pdftotree.parse(casefile, html_path=None, model_type=None, model_path=None, favor_figures=True, visualize=False)
    parsed_html = BeautifulSoup(tree, features='html.parser')
    headers = parsed_html.find_all('section_header')
    titles = []
    footer = headers[-1].text
    for header in headers:
        title = header.text
        if len(title) < 75 and not title.isnumeric() and title[0].istitle():
            titles.append(title)
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
    return main_title.strip(), footer.strip(), final_headers

def parsePDF(casefile, verbose):
    pdf_results = {}
    sections = []
    main_title, footer, final_headers = getSectionHeaders(casefile)
    pdf_text = textract.process(casefile).decode()
    cleaned_text = cleanText(pdf_text, main_title, footer)
    with open(casefile[:-3] + 'txt', 'w') as text_file:
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

def cleanText(pdf_text, main_title, footer):
    case_disclaimer1 = "This case was developed from published sources. Funding for the development of this case was provided by Harvard Business School, and not by the company."
    case_disclaimer2 = "HBS cases are developed solely as the basis for class discussion. Cases are not intended to serve as endorsements, sources of primary data, or illustrations of effective or ineffective management."
    phone1 = "1-800-5457685"
    phone2 = "1-800-545-7685"
    copyright = "Copyright © "
    copyright1 = "President and Fellows of Harvard College."
    copyright2 = "To order copies or request permission to reproduce materials, call"
    copyright3 = "write Harvard Business School Publishing, Boston, MA 02163, or go to www.hbsp.harvard.edu/educators. "
    copyright4 = "This publication may not be digitized, photocopied, or otherwise reproduced, posted, or transmitted, without the permission of Harvard Business School."
    copyright5 = "write Harvard Business School Publishing, Boston, MA 02163, or go to http://www.hbsp.harvard.edu. No part of this publication may be reproduced, stored in a retrieval system, used in a spreadsheet, or transmitted in any form or by any means—electronic, mechanical, photocopying, recording, or otherwise—without the permission of Harvard Business School"
    joined_text = pdf_text.replace('\n', ' ').replace('_', '').replace(phone1, '').replace(phone2, '').replace(case_disclaimer1, '').replace(case_disclaimer2, '').replace(copyright, '').replace(copyright1, '').replace(copyright2, '').replace(copyright3, '').replace(copyright4, '').replace(copyright5, '').replace(footer, '').split()
    return ' '.join(joined_text)

if __name__ == '__main__':
    casefile, verbose = parseArgs()
    pdf_results = parsePDF(casefile[0], verbose)
    with open(casefile[0][:-3] + 'json', 'w') as outfile:
        outfile.write(json.dumps(pdf_results))
