"""
Operate your data.
"""

import csv
import json

from lxml import etree
from lxml import html

from bs4 import BeautifulSoup as bs


def parse_html_file(path):
    print("parsing file:", path)
    parser = etree.HTMLParser(encoding='UTF-8', remove_blank_text=True)
    tree = None
    try:
        tree = etree.parse(path, parser=parser)
    except OSError:
        print('file', path, 'not found!')
    return tree

def write_html_file_pretty(path, root):
    root = html.tostring(root)
    doc = bs(root, features='lxml')
    pretty = doc.prettify()
    with open(path, 'w+', encoding='UTF-8') as f:
        f.write(pretty)

def create_html_delimiter(parent):
    pre = etree.SubElement(parent, 'pre')
    pre.text = '——————————————————————————————'
    # pre.text = '------------------------------'
    return parent

def create_html_text_node(text, parent):
    pre = etree.SubElement(parent, 'pre')
    pre.text = text
    return parent

def create_html_link_node(link, parent, ref, target_blank=False):
    pre = etree.SubElement(parent, 'pre')
    a = etree.SubElement(pre, 'a')
    a.set('href', ref)
    if target_blank:
        a.set('target','_blank')
    a.text = link
    return parent

# index_root.write(path + 'index.html', encoding="UTF-8", method='html')


def get_csv_rows(path):
    print("reading file:", path)
    rows = []
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for r in reader:
            rows.append(r)
    return rows


def read_json_file(path):
    print("reading file:", path)
    with open(path, "r") as f:
        data = json.load(f)
    return data


def write_json_file(path, data):
    print("creating file:", path)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=2))


def read_xml_file(path):
    print("reading file:", path)
    parser = etree.XMLParser(remove_blank_text=True, encoding='UTF-8')
    tree = None
    try:
        tree = etree.parse(path, parser=parser)
    except OSError:
        print('file', path, 'not found!')
    return tree


def write_xml_file(path, root):
    print("creating file:", path)
    tree = etree.ElementTree(root)
    tree.write(path, encoding="UTF-8")


def write_xml_file_pretty(path,root):
    print("creating file:", path)
    tree = etree.ElementTree(root)
    tree.write(path, encoding="UTF-8", pretty_print=True)
