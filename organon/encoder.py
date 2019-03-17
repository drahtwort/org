"""
Encode your data.
"""
import os


from organon import utility

from lxml import etree
from copy import deepcopy



class EncodeCTS:

    def __init__(self, txt, bib, pers, cts_dir='', cts_ns='', cts_xml=''):
        self.txt = txt
        self.bib = bib
        self.pers = pers
        self.cts_dir = cts_dir + '/' + cts_ns + '/data/'
        self.ns_cts = 'urn:cts:'+cts_ns+':'
        self.ns_xml = '{http://www.w3.org/XML/1998/namespace}'
        self.ns_tei = '{http://www.tei-c.org/ns/1.0}'
        self.mod_path = cts_xml
        self.mod_xml = self.get_model()
        self.entries = self.bib.entries

        if not os.path.exists(self.cts_dir):
            os.makedirs(self.cts_dir)

    def get_model(self):
        return utility.read_xml_file(self.mod_path)

    def fill_bib(self, root, entry, pid):
        authors = entry.persons['Author']
        ref_str = ''

        for author in authors:
            fnames = [n.plaintext() for n in author.rich_first_names]
            mnames = [n.plaintext() for n in author.rich_middle_names]
            lnames = [n.plaintext() for n in author.rich_last_names]
            for f in fnames:
                if f:
                    ref_str = ref_str + f + " "
            for m in mnames:
                if m:
                    ref_str = ref_str + m + " "
            for l in lnames:
                if l:
                    ref_str = ref_str + l
            ref_str = ref_str + "; "

        ref_str = ref_str[:-2]

        author = root.find('.//'+self.ns_tei+'persName')
        author.text = ref_str

        title = root.find('.//'+self.ns_tei+'title')
        title.text = self.bib.refs[pid].split('(')[0][:-1]

        reference = root.find('.//'+self.ns_tei+'bibl')

        author = reference.find('.//'+self.ns_tei+'author')
        author.text = ref_str

        title = reference.find('.//'+self.ns_tei+'title')
        title.text = self.bib.refs[pid].split('(')[0][:-1]

        year = reference.find('.//'+self.ns_tei+'date')
        year.text = self.bib.refs[pid].split('(')[1][:-1]

        try:
            place = reference.find('.//' + self.ns_tei + 'pubPlace')
            place.text = entry.fields['Address']
        except KeyError:
            print("no address found for", pid)
            place = reference.find('.//' + self.ns_tei + 'pubPlace')
            place.getparent().remove(place)
        return root

    def fill_modell(self, pid):
        if pid in self.entries:
            entry = self.entries[pid]
        else:
            entry = False
        tree = deepcopy(self.mod_xml)
        root = tree.getroot()
        seg = pid.split('.')
        if entry != False:
            self.fill_bib(root, entry, pid)
        else:
            print("could not find bib for", pid)
        ed_key = seg[2]
        lang_key = ''.join([i for i in ed_key if not i.isdigit()])
        body = root.find('.//'+self.ns_tei+'body')
        body.attrib[self.ns_xml+'lang'] = lang_key
        body.attrib['n'] = self.ns_cts + pid
        for pssg in self.txt.content[pid]:
            p = etree.SubElement(body, 'p')
            p.attrib['n'] = pssg
            p.text = self.txt.content[pid][pssg]
        return tree

    def to_cts_xml(self):
        # print("creating files at following path:")
        print(self.cts_dir)
        for i in self.txt.identifiers:
            f = i + '.xml'
            fp = self.cts_dir + f
            tree = self.fill_modell(i)
            tree.write(fp, xml_declaration=True, encoding="UTF-8", pretty_print=True)
