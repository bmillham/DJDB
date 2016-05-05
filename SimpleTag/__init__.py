from .map import tag_to_db_map
from .fix_track_disc import fix_track_disc
from .parse_year import parse_year
from Name import Name
from mutagen import File
import os

default_options = {
                   'prefixes': ('the', 'a', 'le', 'die', 'les', 'la'), 
                   'tracknumber_warning': False,
                   'dash_warning': False,
                   'fix_spaces': True,
                  }

class SimpleTag(object):
    def __init__(self, filename=None, options=None):
        #print "Simpletag initialized with: ", filename
        self._filename = filename
        self.options = options
        if self.options is None:
            self.options = default_options
        else:
            self.options = options
        self._warnings = {'filename': filename}
        self._tracknumber = None
        self._discnumber = None
        self._artist = None
        self._album = None
        self._title = None
        self._year = None
        try:
            self._raw_tags = File(filename, easy=True)
        except:
            self._raw_tags = False
            self._warnings['ERROR'] = "Error reading tags"
            #print "Error reading tags: ", filename
        else:
            if self._raw_tags is None:
                self._warnings['WARNING'] = "No tags"
            self._fetch_tags()

    def _fetch_tags(self):
        self._title = self._string_tag('title')
        self._artist = Name(self._string_tag('artist'), self.options['prefixes'])
        w = self._artist.warnings
        if len(w) > 0:
            self._warnings['artist'] = w
        self._album = Name(self._string_tag('album'), self.options['prefixes'])
        w = self._album.warnings
        if len(w) > 0:
            self._warnings['album'] = w
        self._year = parse_year(self, 'date')
        self._discyear = parse_year(self, 'discyear')
        if self._discyear == 0 and self._year != 0:
            self._discyear = self._year
        self._tracknumber = fix_track_disc(self, 'tracknumber', self.options['tracknumber_warning'])
        self._discnumber = fix_track_disc(self, 'discnumber')
        self.album.year = self._discyear
        self.album.disc = self._discnumber
        try:
            self._bitrate = self._raw_tags.info.bitrate
        except:
            self._bitrate = 0
        try:
            self._sample_rate = self._raw_tags.info.sample_rate
        except:
            self._sample_rate = 0
        try:
            self._length = self._raw_tags.info.length
        except:
            self._length = 0
        else:
            self._length = int(round(float(self._length)))
        self._size = os.path.getsize(self._filename)
        self._modification_time = int(os.path.getmtime(self._filename))

    def _string_tag(self, field):
        if self._raw_tags is None:
            self._raw_tags = {}
            self.warnings = (field, "No tags in file")
        try:
            t = self._raw_tags[field][0]
        except:
            t = u'UNKNOWN'
            self.warnings = (field, "Missing required tag")
            self._raw_tags[field] = [t]
        if t is None or t == '':
            t = u'UNKNOWN'
            self.warnings = (field, "Empty required string tag")
            self._raw_tags[field] = [t]
        """Strip leading/trailing spaces. Does not actually fix the tags."""
        if self.options['fix_spaces']:
            f = t.strip()
            if f != t:
                w = "Leading/trailing spaces (fixed in database): `%s`" % t
                self.warnings = ((field, w))
                t = f
        """Warn about ' - ' in names"""
        if ' - ' in t and self.options['dash_warning']:
            self.warnings = ((field, "Found ' - ' (not fixed in database): %s" % t))
        return t

    @property
    def raw_tags(self):
        return self._raw_tags

    @property
    def title(self):
        return self._title

    @property
    def year(self):
        return self._year

    @property
    def tracknumber(self):
        return self._tracknumber

    @property
    def discnumber(self):
        return self._discnumber
 
    @property
    def warnings(self):
        """ There will always be 1 warning, the filename, so only expose the warnings
            if there are more than just the filename"""
        if len(self._warnings) > 1:
            return self._warnings
        else:
            return None

    @warnings.setter
    def warnings(self, values):
        try:
            field, value = values
        except ValueError:
            raise ValueError("Pass an iterable with 2 values")
        else:
            if field in self._warnings:
                if type(self._warnings[field]) is list:
                    self._warnings[field].append(value)
                else:
                    self._warnings[field] = [self._warnings[field], value]
            else:
                self._warnings[field] = value

    @property
    def artist(self):
        return self._artist

    @property
    def album(self):
        return self._album

    @property
    def bitrate(self):
        return self._bitrate

    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def length(self):
        return self._length

    @property
    def size(self):
        return self._size

    @property
    def modification_time(self):
        return self._modification_time
