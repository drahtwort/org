"""
Reference the textual data.
"""

from pybtex.database import parse_file


class Biblio:

    def __init__(self, path=''):
        self.path = path    
        self.file = self.get_file()
        self.entries = self.file.entries # self.get_entries()
        self.bibkeys = self.entries.keys()
        self.authors = self.get_authors()
        self.refs = self.get_refs()
        self.refs_bib = self.get_refs_bib()
        self.refs_years = self.get_refs_year()
        self.years = list(self.refs_years.keys())
        self.years.sort()

    def get_file(self):
        print("reading file:",self.path)
        file = parse_file(self.path, bib_format="bibtex")
        return file

    def get_authors(self):
        authors = []
        for val in self.entries.values():
            try:
                author = val.persons['Author']
                for a in author:
                    fname = [n.plaintext() for n in a.rich_first_names]
                    mname = [n.plaintext() for n in a.rich_middle_names]
                    lname = [n.plaintext() for n in a.rich_last_names]
                    total = fname + mname + lname
                    name = " ".join(total)
                    if name not in authors:
                        authors.append(name)
                    else:
                        continue
            except KeyError:
                continue
        authors.sort()
        return authors

    def get_refs(self):
        references = {}
        for bkey in self.bibkeys:
            ref_str = ""
            if bkey in self.entries:
                entry = self.entries[bkey]
                title = entry.rich_fields.get('Title').plaintext()
                if "35" not in title:
                    title = title.split('.')[0]
                year = entry.rich_fields.get('Year').plaintext()
                ref_str += title + " ("+year+")"
                references[bkey] = ref_str
        return references

    def get_refs_year(self):
        references = {}
        for bkey in self.bibkeys:
            ref_str = ""
            if bkey in self.entries:
                entry = self.entries[bkey]
                try:
                    authors = entry.persons['Author']
                    for author in authors:
                        # fnames = [n.plaintext() for n in author.rich_first_names]
                        # mnames = [n.plaintext() for n in author.rich_middle_names]
                        lnames = [n.plaintext() for n in author.rich_last_names]
                        # for f in fnames:
                        #     if f:
                        #         ref_str = ref_str + f + " "
                        # for m in mnames:
                        #     if m:
                        #         ref_str = ref_str + m + " "
                        for l in lnames:
                            if l:
                                ref_str = ref_str + l
                        ref_str = ref_str + " / "
                    ref_str = ref_str[:-3]+", "
                    # title = entry.fields['Title']
                    title = entry.rich_fields.get('Title').plaintext()
                    if "35" not in title:
                        title = title.split('.')[0]
                    year = entry.fields['Year']
                    ref_str = ref_str + title + " ("+year+")"
                    if year in references:
                        tmp = references[year]
                        tmp.append((bkey, ref_str))
                        references[year] = tmp
                    else:
                        references[year] = [(bkey, ref_str)]
                except KeyError:
                    continue
            else:
                print("no bib entry found for", bkey)
        return references

    def get_refs_bib(self):
        references = {}
        for bkey in self.bibkeys:
            ref_str = ""
            if bkey in self.entries:
                entry = self.entries[bkey]
                try:
                    authors = entry.persons['Author']
                    for author in authors:
                        fnames = [n.plaintext() for n in author.rich_first_names]
                        # mnames = [n.plaintext() for n in author.rich_middle_names]
                        lnames = [n.plaintext() for n in author.rich_last_names]
                        for f in fnames:
                            if f:
                                ref_str = ref_str + f[0] + ". "
                        # for m in mnames:
                        #     if m:
                        #         ref_str = ref_str + m + " "
                        for l in lnames:
                            if l:
                                ref_str = ref_str + l
                        ref_str = ref_str + " / "
                    ref_str = ref_str[:-3]+", "
                    # title = entry.fields['Title']
                    title = entry.rich_fields.get('Title').plaintext()
                    if "35" not in title:
                        title = title.split('.')[0]
                    year = entry.fields['Year']
                    ref_str = ref_str + title + " ("+year+")"
                    references[bkey] = ref_str
                except KeyError:
                    continue
            else:
                print("no bib entry found for", bkey)
        return references

    def get_ref(self,bibkey):
        entry = None
        try:
            entry = self.entries[bibkey]
        except KeyError:
            print("no entry found with given key",bibkey,"!")
        ref = None
        if entry is not None:
            t = entry.type
            if t == 'incollection':
                ref =  self.get_ref_incoll(entry)
            elif t == 'article':
                ref = self.get_ref_article(entry)
            elif t == 'book':
                ref = self.get_ref_book(entry)
            else:
                print("no style defined for given genre", t,"!")
                print("could not generate reference!")
            return ref
        else:
            return ref

    def get_ref_article(self, entry):
        # Autoren, Titel, Journal, Volume, Nr., Year, Pages
        return None

    def get_ref_incoll(self, entry):
        return None

    def get_ref_book(self, entry):
        ref = ''
        authors = entry.person['Author']
        for author in authors:
            fnames = [n.plaintext() for n in author.rich_first_names]
            mnames = [n.plaintext() for n in author.rich_middle_names]
            lnames = [n.plaintext() for n in author.rich_last_names]
            for f in fnames:
                if f:
                    ref = ref + f + " "
            for m in mnames:
                if m:
                    ref = ref + m + " "
            for l in lnames:
                if l:
                    ref = ref + l
            ref = ref + "; "
        ref = ref[:-2] + ", "
        # title = entry.fields['Title']
        title = entry.rich_fields.get('Title').plaintext()
        ref = ref + title + ", "
        year = entry.fields['Year']
        # Autoren, Titel, Ort: Verlag Jahr.
        return None
