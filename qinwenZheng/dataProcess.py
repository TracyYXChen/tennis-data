from bs4 import BeautifulSoup
import pandas as pd
import quopri
import re

def decode_mht_file(mht_file_path):
    encode = "ISO-8859-1"
    with open(mht_file_path, 'r', encoding=encode) as file:
        content = file.read()
    # extract HTML part from .mht file
    html_part_match = re.search('Content-Type: text/html(.*)', content, flags=re.S | re.I)
    if html_part_match:
        html_part = html_part_match.group(1)
    # decode the quoted printable string
    decoded_html = quopri.decodestring(html_part).decode(encode)
    return decoded_html

# replace with your .mht file path
mht_file_path = 'raw/Tennis Abstract_ Qinwen Zheng WTA Match Results, Splits, and Analysis.mht'
decoded_html = decode_mht_file(mht_file_path)

soup = BeautifulSoup(decoded_html, 'html.parser')
table = soup.find('table', {'id': 'matches'})
df = pd.read_html(str(table))[0]
df.to_csv(f'processed/zheng_career_matches.csv', index=False)

