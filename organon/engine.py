"""
Craft your data.
"""

from organon import reader
from organon import biblio
from organon import encoder
from organon import static

class Engine:

    def __init__(self, txt_path='', pers_path='', bib_path='', desc_path='', facs_path=''):

        self.text = reader.Reader(txt_path=txt_path) if txt_path else None
        self.persons = reader.PersReader(path=pers_path) if pers_path else None
        self.reference = biblio.Biblio(path=bib_path) if bib_path else None
        self.description = reader.DescReader(path=desc_path) if desc_path else None
        self.facsimile = reader.FacsReader(path=facs_path) if facs_path else None


    def encode(self, cts_dir, cts_ns, cts_xml):
        return encoder.EncodeCTS(self.text, self.reference, self.persons, cts_dir, cts_ns, cts_xml) if self.text and self.reference else None

    def static(self, www_dir):
        return static.StaticHTML(www_dir, self.text, self.reference, self.persons, self.description, self.facsimile) if self.text else None
