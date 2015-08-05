

class Name(object):
    def __init__(self, tag, prefixes=[]):
        self._warnings = []
        self._fullname = tag
        self._discnumber = None
        self._discyear = None
        self._prefixes = prefixes
        self.get_prefix()

    @property
    def fullname(self):
        return self._fullname

    @property
    def prefix(self):
        return self._prefix

    @property
    def name(self):
        return self._name

    @property
    def warnings(self):
        return self._warnings

    @property
    def year(self):
        return self._discyear

    @year.setter
    def year(self, value):
        self._discyear = value

    @property
    def disc(self):
        return self._discnumber

    @disc.setter
    def disc(self, value):
        self._discnumber = value

    def get_prefix(self):
        l = self._fullname.split(" ", 1)
        if len(l) == 1 or l[0].lower() not in self._prefixes:
            self._prefix = None
            self._name = self._fullname
        else:
            self._prefix, self._name = l
