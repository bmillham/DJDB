def parse_year(self, field):
    try:
        year = find_year(self._raw_tags[field][0])
    except:
        year = 0
    return year

def find_year(tag):
    """Find year in a date, supports various date formats"""
    if '-' in tag:
        for a in tag.split('-'):
            if len(a) == 4:
                year = a
    else:
        year = tag
    try:
        year = int(year)
    except:
        year = 0
    return year