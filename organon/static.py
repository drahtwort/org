"""
Generate static content.
"""

import os
import shutil

from lxml import etree
from copy import deepcopy
from unidecode import unidecode

from organon import utility


class StaticHTML:

    def __init__(self, www, txt, bib, pers, desc, facs):

        self.txt = txt
        self.bib = bib

        self.models = {}

        self.desc = desc
        self.pers = pers
        self.facs = facs
        self.levels = self.txt.levels

        self.curr_path = www
        # hard coded paths?
        self.model_path = self.curr_path + '/resources/html/'
        self.model_file = self.model_path + 'section.html'
        # what happens if model file isnt found? handle it!
        self.model = utility.parse_html_file(self.model_file)

        self.corp_path = self.curr_path + '/corp/'
        self.corp_group_path = self.corp_path + 'group/'
        self.corp_work_path = self.corp_path + 'work/'
        self.corp_ed_path = self.corp_path + 'edition/'
        self.corp_pass_path = self.corp_path + 'passage/'
        # self.pass_path = self.curr_path + 'pass/'
        # self.pers_path = self.curr_path + 'pers/'

        self.facs_path= self.curr_path + 'facs/'
        self.desc_path = self.curr_path + 'desc/'

    def process_sections(self):
        self.create_section('CORPUS', self.corp_path)
        self.process_corpus()
        self.create_subsection('GROUP', self.corp_group_path, model=self.models['CORPUS']['content'], parent='CORPUS')
        self.process_group()
        self.create_subsection('EDITION', self.corp_ed_path, model=self.models['CORPUS']['content'], parent='CORPUS')
        self.process_edition()
        self.create_subsection('PASSAGE', self.corp_pass_path, model=self.models['CORPUS']['content'], parent='CORPUS')
        self.process_passage()
        # self.create_section('DESCRIPTOR', self.desc_path)
        # self.process_descriptor()
        # self.create_section('FACSIMILE', self.facs_path)
        # self.process_facsimile()

    def create_section(self, name, path='', model=None):
        self.models[name] = {}
        if os.path.exists(path):
            print("delete directory:", path)
            shutil.rmtree(path)
            print("create directory:", path)
            os.makedirs(path)
        else:
            print("create directory:", path)
            os.makedirs(path)
        if model:
            index_root = deepcopy(model)
        else:
            index_root = deepcopy(self.model)
        sec_name = 'Drahtwort: ' + name.lower().capitalize()
        title = index_root.find("head/title")
        title.text = sec_name
        index_body = index_root.find("body")
        index_body = utility.create_html_text_node(name, index_body)
        index_body = utility.create_html_delimiter(index_body)
        self.models[name]['index'] = index_root
        if model:
            root = deepcopy(model)
        else:
            root = deepcopy(self.model)
        title = root.find("head/title")
        title.text = sec_name
        body = root.find("body")
        body = utility.create_html_link_node(name, body, './')
        body = utility.create_html_delimiter(body)
        self.models[name]['content'] = root

    def create_subsection(self, name, path='', model=None, parent=''):
        self.models[name] = {}
        if os.path.exists(path):
            print("delete directory:", path)
            shutil.rmtree(path)
            print("create directory:", path)
            os.makedirs(path)
        else:
            print("create directory:", path)
            os.makedirs(path)
        if model:
            index_root = deepcopy(model)
            links = index_root.findall('body/pre/a')
            links[0].set('href','../../')
            links[1].set('href','../')
            links = index_root.findall('head/link')
            links[0].set('href','../../resources/css/dw.css')
            links[1].set('href','../../../favicon-96x96.png')
        else:
            index_root = deepcopy(self.model)
        sec_name = 'Drahtwort: ' + name.lower().capitalize()
        title = index_root.find("head/title")
        title.text = sec_name
        index_body = index_root.find("body")
        index_body = utility.create_html_text_node(name, index_body)
        index_body = utility.create_html_delimiter(index_body)
        self.models[name]['index'] = index_root
        if model:
            root = deepcopy(model)
            links = root.findall('body/pre/a')
            links[0].set('href','../../')
            links[1].set('href','../')
            links = root.findall('head/link')
            links[0].set('href','../../resources/css/dw.css')
            links[1].set('href','../../../favicon-96x96.png')
        else:
            root = deepcopy(self.model)
        title = root.find("head/title")
        title.text = sec_name
        body = root.find("body")
        body = utility.create_html_link_node(name, body, './')
        body = utility.create_html_delimiter(body)
        self.models[name]['content'] = root

    def process_corpus(self):
        index_root = deepcopy(self.models['CORPUS']['index'])
        index_body = index_root.find('body')
        utility.create_html_link_node('GROUP',index_body,'./group/')
        utility.create_html_link_node('EDITION',index_body,'./edition/')
        utility.create_html_link_node('PASSAGE',index_body,'./passage/')
        utility.create_html_delimiter(index_body)
        utility.write_html_file_pretty(self.corp_path + 'index.html', index_root)

    def process_edition(self):
        index_root = deepcopy(self.models['EDITION']['index'])
        index_body = index_root.find('body')
        for year in self.bib.years:
            for pub in self.bib.refs_years[year]:
                urn, meta = pub
                if urn in self.txt.content:
                    f = './' + urn + '.html'
                    utility.create_html_link_node(meta,index_body,f)
                    content = self.txt.content[urn]
                    # passages = list(content.keys())
                    root = deepcopy(self.models['EDITION']['content'])
                    body = root.find('body')
                    utility.create_html_text_node(meta,body)
                    utility.create_html_delimiter(body)
                    for i, k in enumerate(content):
                        if i:
                            utility.create_html_delimiter(body)
                        # re.findall(r"'(.*?)'", content[k][0])
                        utility.create_html_text_node(content[k], body)
                    utility.create_html_delimiter(body)
                    utility.write_html_file_pretty(self.corp_ed_path + f[2:], root)
                else:
                    print("edition: can not find material", urn)
                    continue
        utility.create_html_delimiter(index_body)
        utility.write_html_file_pretty(self.corp_ed_path + 'index.html', index_root)

    def process_passage(self):
        index_root = deepcopy(self.models['PASSAGE']['index'])
        index_body = index_root.find('body')
        for year in self.bib.years:
            for pub in self.bib.refs_years[year]:
                urn, meta = pub
                if urn in self.txt.content:
                    f = urn
                    utility.create_html_link_node(meta,index_body,'./' + f+'-1.html')
                    content = self.txt.content[urn]
                    passages = list(content.keys())
                    for i, k in enumerate(content):
                        root = deepcopy(self.models['PASSAGE']['content'])
                        body = root.find('body')
                        utility.create_html_text_node(meta,body)
                        utility.create_html_delimiter(body)
                        # re.findall(r"'(.*?)'", content[k][0])
                        utility.create_html_text_node(content[k], body)
                        utility.create_html_delimiter(body)
                        if i < len(passages) - 1:
                            np = i + 1
                            next_fp = './' + f + '-' + passages[np] + '.html'
                            utility.create_html_link_node('==>',body,next_fp)
                        fp = self.corp_pass_path + f + '-' + k + '.html'
                        utility.write_html_file_pretty(fp, root)
                else:
                    print("passage: can not find material", urn)
                    continue
        utility.create_html_delimiter(index_body)
        utility.write_html_file_pretty(self.corp_pass_path + 'index.html', index_root)

    def process_group(self):
        index_root = deepcopy(self.models['GROUP']['index'])
        index_body = index_root.find('body')
        a = list(self.levels.keys())
        a.sort()
        for auth in a:
            if auth in self.pers:
                name = self.pers[auth]['Forename']+' '+self.pers[auth]['Surname']
                pers_fp = './' + auth + '.html'
                utility.create_html_link_node(name,index_body,pers_fp)
                pers_index = deepcopy(self.models['GROUP']['content'])
                pers_body = pers_index.find('body')
                utility.create_html_text_node(name,pers_body)
                utility.create_html_delimiter(pers_body)
                for ref in self.bib.refs:
                    if auth in ref:
                        if ref in self.txt.content:
                            utility.create_html_link_node(self.bib.refs[ref],pers_body,'./' + ref + '.html')
                            root = deepcopy(self.models['GROUP']['content'])
                            body = root.find('body')
                            utility.create_html_link_node(name,body,pers_fp)
                            utility.create_html_delimiter(body)
                            utility.create_html_text_node(self.bib.refs[ref],body)
                            utility.create_html_delimiter(body)
                            content = self.txt.content[ref]
                            passages = list(content.keys())
                            for i, k in enumerate(content):
                                utility.create_html_text_node(content[k], body)
                                utility.create_html_delimiter(body)
                            fp = self.corp_group_path + ref + '.html'
                            utility.write_html_file_pretty(fp, root)
                        else:
                            print("group: can not find material", ref)

            else:
                print("group: can not find author", auth)
                continue
            utility.create_html_delimiter(pers_body)
            pers_fp = self.corp_group_path + auth + '.html'
            utility.write_html_file_pretty(pers_fp, pers_index)
        utility.create_html_delimiter(index_body)
        utility.write_html_file_pretty(self.corp_group_path + 'index.html', index_root)

    def process_facsimile(self):
        index_root = deepcopy(self.models['FACSIMILE']['index'])
        index_body = index_root.find('body')
        for fac in self.facs:
            utility.create_html_link_node(fac,index_body,self.facs[fac],True)
        utility.create_html_delimiter(index_body)
        utility.write_html_file_pretty(self.facs_path + 'index.html', index_root)

    def process_descriptor(self):
        index_root = deepcopy(self.models['DESCRIPTOR']['index'])
        index_body = index_root.find('body')
        descs = list(self.desc.keys())
        descs.sort()
        for desc in descs:
            desc_fp = './'+unidecode(desc).lower() + '.html'
            utility.create_html_link_node(desc,index_body,desc_fp)
            urns = self.desc[desc]
            desc_index = deepcopy(self.models['DESCRIPTOR']['content'])
            desc_body = desc_index.find('body')
            utility.create_html_text_node(desc, desc_body)
            utility.create_html_delimiter(desc_body)
            for urn in urns:
                if urn in self.txt.content:
                    if urn in self.bib.refs_bib:
                        meta = self.bib.refs_bib[urn]
                    else:
                        meta = urn
                        print("desc: could not find reference for", urn)
                    fp = './' + unidecode(desc).lower() + '_' + urn + '.html'
                    utility.create_html_link_node(meta,desc_body,fp)
                    passages = urns[urn]
                    text = ''
                    for p in passages:
                        passage = p.split("-")
                        if len(passage) > 1:
                            start = int(passage[0])
                            finish = int(passage[1])
                            text = ''
                            for i in range(start, finish+1):
                                content = self.txt.content[urn][str(i)]
                                text += content + '\n\n'
                        else:
                            content = self.txt.content[urn][passage[0]]
                            text += content + '\n\n'
                else:
                    print("desc: can not find material", urn)
                    continue
                text = text[:-2]
                root = deepcopy(self.models['DESCRIPTOR']['content'])
                body = root.find('body')
                utility.create_html_link_node(desc,body,desc_fp)
                utility.create_html_delimiter(body)
                utility.create_html_text_node(meta,body)
                utility.create_html_delimiter(body)
                utility.create_html_text_node(text,body)
                utility.create_html_delimiter(body)
                fp = self.desc_path + unidecode(desc).lower() + '_' + urn + '.html'
                utility.write_html_file_pretty(fp, root)
            utility.create_html_delimiter(desc_body)
            desc_fp = self.desc_path + unidecode(desc).lower() + '.html'
            utility.write_html_file_pretty(desc_fp, desc_index)
        utility.create_html_delimiter(index_body)
        utility.write_html_file_pretty(self.desc_path + 'index.html', index_root)
