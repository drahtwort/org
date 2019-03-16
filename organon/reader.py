"""
Read the textual data.
"""

import os

from organon import utility

class FacsReader:

    def __init__(self, path):
        self.path = path
        self.data = utility.read_json_file(self.path)

class DescReader:

    def __init__(self, path):
        self.path = path
        self.data = utility.read_json_file(self.path)

class PersReader:

    def __init__(self, path=''):
        self.path = path
        self.data = {}
        if path:
            self.data = self._get_data()

    def _get_data(self):
        rows = utility.get_csv_rows(self.path)
        header = rows[0]
        data = {}
        for j in range(1, len(rows)):
            idx = rows[j][0]
            data[idx] = {}
            i = 1
            while i < len(rows[j]):
                data[idx][header[i]] = rows[j][i]
                i = i + 1
        return data

class Reader:

    def __init__(self, txt_path=''):
        self.base = txt_path
        self.paths = self._get_txt_filepaths()
        self.content = self._get_txt_content()
        self.identifiers = self._get_txt_identifiers()
        self.levels = self._get_txt_levels()

    def _get_txt_filepaths(self):
        paths = []
        for root, dirs, files in os.walk(self.base):
            for name in files:
                path = os.path.join(root, name)
                if name.endswith(".txt"):
                    paths.append(path)
        return paths

    def _get_txt_content(self):
        content = {}
        for i, path in enumerate(self.paths):
            with open(path) as f:
                key = path.split("/")[-1:][0].replace(".txt","")
                lines = f.readlines()
                content[key] = {}
                for j, line in enumerate(lines):
                    content[key][str(j)] = line.strip()
        return content

    def _get_txt_identifiers(self):
        idx = list(self.content.keys())
        idx.sort()
        return idx

    def _get_txt_levels(self):
        data = {}
        for k in self.identifiers:
            level = k.split('.')
            author = level[0]
            work = level[1]
            edition = level[2]
            if author not in data:
                data[author] = {}
            if work not in data[author]:
                data[author][work] = {}
            if edition not in data[author][work]:
                data[author][work][edition] = {}
            text = self.content[k]
            for passage in text:
                data[author][work][edition][passage] = text[passage]
        return data
