import re

def fix_track_disc(self, tag_field, tracknumber_warning=False):
    """ Fix track and disc info. Supports 1/x style, 1.x style and (1,x) style tags"""
    try:
        tag = self._raw_tags[tag_field][0]
    except:
        if tag_field == 'tracknumber' and tracknumber_warning: # Only warn about missing track numbers
            self.warnings = ((tag_field, "No track number"))
        return 0
    
    if "/" in tag: # Check for 1/x track numbers
        tracknumber, tot = tag.split("/")
    elif "." in tag: # Check for 1.x track numbers
        tracknumber, tot = tag.split('.')
    elif "," in tag: # Check for (1,x) or 1,x track numbers
        tracknumber, tot = tag.split(",")
        tracknumber = re.sub(r"[\D]", "", tracknumber)
    else:
        tracknumber = tag
    try:
        tn = int(tracknumber)
    except:
        self.warnings = ((tag_field, "Failed to parse: {}".format(tag)))
        tn = 0
    #self._warnings.append(tag_field)
    return tn