"""
Process your data.
"""

from organon import reader
from organon import biblio
from organon import encoder
from organon import static

class Engine:

    def __init__(self, txt_path='', pers_path='', bib_path='', desc_path='', facs_path=''):

        self.text = reader.PlainReader(txt_path=txt_path) if txt_path else None
        self.persons = reader.PersReader(path=pers_path) if pers_path else None
        self.reference = biblio.Biblio(path=bib_path) if bib_path else None
        self.description = reader.JsonReader(path=desc_path) if desc_path else None
        self.vocabulary = None
        if self.description:
            self.vocabulary = list(self.description.data.keys())
            self.vocabulary.sort()
        self.facsimile = reader.JsonReader(path=facs_path) if facs_path else None


    def encode(self, cts_dir, cts_ns, cts_xml):
        return encoder.EncodeCTS(self.text,
                                 self.reference,
                                 self.persons,
                                 cts_dir,
                                 cts_ns,
                                 cts_xml) if (self.text and self.reference) else None

    def static(self, www_dir):
        return static.StaticHTML(www_dir,
                                 self.text,
                                 self.reference,
                                 self.persons.data,
                                 self.description.data,
                                 self.facsimile.data) if (self.text and
                                                          self.reference and
                                                          self.persons and
                                                          self.description and
                                                          self.facsimile) else None
