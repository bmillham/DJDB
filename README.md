DJDB
====

DJDB is a simple replacement for Ampache for creating and maintaining a music library
-------------------------------------------------------------------------------------

###DJDB main intended use is for IDJC users who plan on using the DJRQ request site, or just don't want to use Ampache

DJDB is NOT a tagging tool, keeping in line with the linux idea of 'One program to do one thing'

Advantages to using DJDB vs. Ampache:
 1. Much smaller codebase.
 2. No webserver required.
 3. No problems with permissions since it runs as you, instead of as the webserver.
 4. Much faster scanning.
 5. No extra dependencies, if you have IDJC and use an Ampache database, you have everything you need.

To install DJDB, simply clone the repo into a directory, and run djdb.py. Follow the first run assistant prompts.

DJDB does not try to figure out tags based on filename. It only uses the tags in the files. So
it does not require internet access to run (unlike Ampache).

It also does not try to get album art.

DJDB does add a new field to the song table in the Ampache database. This will not prevent Ampache
from working, but could cause a problem if you try to update your version of Ampache.

DJDB can create a new Ampache database, but adds a few tables (only to new database, not to an existing
database) for future use with IDJC and a request web site.

DJDB will scan for removed files, and update the database accordingly (like the Ampache clean feature)

A few things about how DJDB handles tags:
 1. It looks for tags that begin/end with spaces, and removes those spaces before adding to the
    database. The tags in the file are not changed. You will see a warning about those so you
    can fix them with your favorite taging tool.
 2. It looks for tags with ' - ' and warns you about those. This is for future use with IDJC and
    a request site.
 3. Warns you about badly formatted date/track/discnumber tags

A few things that DJDB does very different from Ampache
 1. Ampache incorrectly calculates track length. A track of 60.9 is calculated as 60
    instead of 61. gAmp handles this correctly.
 2. Ampache seems to calculate the average bit rate of a file, instead of using what
    is reported in the file tags. gAmp uses the tags from the file.
 3. DJDB currently can not figure out if a file is CBR, VBR or ABR, so just uses
    VBR in the database for all file. Since IDJC does not use this information,
    it shouldn't be a problem.

Things that need to be done:
 1. Allow deleting a catalog.

Before trying out DJDB, please make a backup of your Ampache database, just to be safe.
I have had no problems with it corrupting my database, but safe is always the best thing!

