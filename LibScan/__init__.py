# -*- coding: utf-8 -*- 
__author__ = 'brian'

from gi.repository import GObject
from Handler import Handler
from time import time, strftime, localtime
from SimpleTag import SimpleTag
#import mutagen
#import pymongo
import os

try:
    import pymysql
except ImportError:
    pymysql = False
    print("Failed to import pymysql")
else:
    pymysql.install_as_MySQLdb()

try:
    import MySQLdb as sql
except ImportError:
    print("Failed to import mysql!")
    
from string import Template
from Database.Ampache import Queries
#import re

# Filetypes supported. If you find a filetype not being scanned, add it here.

valid_filetypes = ["aac", "adif", "adts", "mid", '669', 'amf', 'ams', 'dsm', 'far', 'it', 'med', 'mod',
                   'mt2', 'mtm', 'okt', 's3m', 'stm', 'ult', 'gdm', 'xm', "ape", "mp3", "mp2",
                   'mp4', 'm4a', 'm4v', "mpc", "mp+", "spc", "tta", "vgm", "wav", "wv", "wma", "ogg",
                   "oga", "flac", "oggflac", "spx", "ogv", "opus"]

modes = ('abr', 'vbr', 'cbr')

class LibScan(Handler):
    def __init__(self, builder, configfile, options, gobject):
        print('Initilize libscan', builder)
        self.default_prefixes =  ('the', 'a', 'an', 'die', 'ein', 'le', 'les', 'la')
        self.cursor = None
        self.db = None
        self.full_scan = False
        self.options = options
        self._valid_filetypes = valid_filetypes
        super(LibScan, self).__init__(builder, configfile, options, gobject)
        self.estimated_total_files = 0
        self.genre_by_id = []
        self.genre_by_name = []


    def scan_files(self, estimate=False):
        self.fcount = 0
        self.files_skipped = 0
        self.files_bad = 0
        self.files_no_tags = 0
        self.new_tracks = 0
        self.gobject['warningsstore'].clear()
        self.gobject['changedstore'].clear()
        self.gobject['button_scan_library'].set_label("Abort Scan")
        self.gobject['preferences_imagemenuitem'].set_sensitive(False)

        if self.full_scan:
            print("Ignoring file time to run full scan")
        try:
            self.cursor.execute(Queries.add_modification_time)
        except:
            print("Field already in database")

        print("Getting genre list")
        self.genre_by_id = {}
        self.genre_by_name = {}
        self.cursor.execute(Queries.select_all_genre)
        for r in self.cursor.fetchall():
            self.genre_by_id[r['id']] = r['name'].lower().strip()
            self.genre_by_name[r['name'].lower().strip()] = r['id']

        print("Getting catalogs")
        self.cursor.execute(Queries.get_catalogs)
        self.catalog_list = []
        for r in self.cursor.fetchall():
            self.catalog_list.append({'id': r['cid'], 'name': r['name'], 'paths': [r['path']]})
        if not estimate and not self.options['no_gui']:
            self.gobject['pgrScan'].set_text(None)
            
        self.start_time = time()
        self.mismatch = 0
        self.skipped = 0
        self.warnings_count = 0
        self._changed_iters = {}

        self.cursor.execute("SET autocommit = 0")
        for c in self.catalog_list:
            added_to_catalog = 0
            changed_in_catalog = 0
            self.catalog_id = c['id']
            for d in c['paths']:
                self.gobject['lblCatalog'].set_text('%s (%s)' % (c['name'], d))
                for folder, subs, files in os.walk(str(d)):
                    if not estimate:
                        self.cursor.execute("START TRANSACTION")
                    if not self.scan_running:
                        self.gobject['lblCatalog'].set_text('Scan Aborted')
                        self.gobject['button_scan_library'].set_label("Scan Library")
                        self.gobject['preferences_imagemenuitem'].set_sensitive(True)
                        self.estimate_completed = True
                        self.full_scan = False
                        self.cursor.execute("COMMIT")
                        if self.options['no_gui']:
                            pass
                        else:
                            x = yield False
                    self.gobject['lblDirectory'].set_text(folder.replace(str(d) + os.path.sep, ""))
                    # Directories begining with .Trash (or .trash etc.) and 0000 are ignored
                    # TODO: add ability to cofigure directories to ignore
                    subs[:] = [sub for sub in subs if sub[:6].lower() != '.trash' and sub [:4] != '0000']
                    subs.sort(key=str.lower)
                    if estimate:
                        self.fcount += len(files)
                        self.gobject['est_label'].set_text(str(self.fcount))
                    else:
                        try:
                            self.fraction = float(self.fcount) / float(self.estimated_total_files)
                        except ZeroDivisionError:
                            self.fraction = 0.0
                        artists = []
                        for file in files:
                            self.fcount += 1
                            f, x = os.path.splitext(os.path.join(folder, file))
                            if x[1:].lower() not in self._valid_filetypes:
                                self.files_skipped += 1
                                continue
                            self.cursor.execute(Queries.select_song_by_filename, (f+x,))
                            if self.cursor.rowcount > 1:
                                for row in self.cursor.fetchall():
                                    if row['file'] == f+x:
                                        r = row
                            elif self.cursor.rowcount == 1:
                                r = self.cursor.fetchone()
                            else:
                                if self.add_new_track(f+x):
                                    added_to_catalog += 1
                            
                                self.update_display()
                                continue
                            self.modification_time = t = int(os.path.getmtime(f+x))
                            if r['modification_time'] == t and not self.full_scan:
                                self.skipped += 1
                                self.gobject['lblArtist'].set_text(r['artist_name'])
                                self.gobject['lblAlbum'].set_text(r['album_name'])
                                self.gobject['lblTitle'].set_text(r['title'])
                                self.update_display()
                                continue
                            info = SimpleTag(f+x, self.options['program'])
                            #print(f"got info from simpletag {info}")
                            if info.warnings:
                                self.add_warnings(info.warnings)
                            if not info.raw_tags:
                                self.files_bad += 1
                                continue
                            self.gobject['lblAlbum'].set_text(info.album.fullname)
                            self.gobject['lblTitle'].set_text(info.title)
                            if info is not None:
                                if self.cursor.rowcount == 0:
                                    print("No match in the database for %s" % f+x)
                                else:
                                    if self.check_tags(r, info):
                                        self.mismatch += 1
                                        self.update_info(r, info)
                                        changed_in_catalog += 1
                                    else:
                                        self.skipped += 1
                                        self.cursor.execute(Queries.update_song_modification_time, (info.modification_time, r['sid']))
                                    if info.genre is not None:
                                        if r['genreid'] is None:
                                            #print(f"No genre '{info.genre}' in database")
                                            if info.genre.lower() in self.genre_by_name.keys():
                                                #print(f"Adding genre {info.genre} for {r['artist_name']} - {r['title']} - {r['album_name']}")
                                                self.cursor.execute(Queries.insert_tag_map, (self.genre_by_name[info.genre.lower()], r['sid']))
                                            else:
                                                #print(f'Genre "{info.genre}" is not in tag table')
                                                self.cursor.execute(Queries.insert_tag, (info.genre,))
                                                new_id = self.cursor.lastrowid
                                                self.cursor.execute(Queries.insert_tag_map, (new_id, r['sid']))
                                                self.genre_by_id[new_id] = info.genre.lower()
                                                self.genre_by_name[info.genre.lower()] = new_id
                                        elif info.genre.lower() != self.genre_by_id[r['genreid']]:
                                            print(f"Genre mismatch. Tag: '{info.genre}', DB: {r['genreid']} ({self.genre_by_id[r['genreid']]})")
                                            #print(self.genre_by_name)
                                            if info.genre.lower() in self.genre_by_name.keys():
                                                print(f"Update genre to {self.genre_by_name[info.genre.lower()]}")
                                                #self.cursor.execute(Queries.insert_tag_map, (self.genre_by_name[info.genre.lower()], r['sid']))
                                                self.cursor.execute(Queries.update_tag_map, (self.genre_by_name[info.genre.lower()], r['sid']))
                                            else:
                                                #print(f"Adding Genre {info.genre} to tag table")
                                                self.cursor.execute(Queries.insert_tag, (info.genre,))
                                                new_id = self.cursor.lastrowid
                                                #self.cursor.execute(Queries.insert_tag_map, (new_id, r['sid']))
                                                self.genre_by_id[new_id] = info.genre.lower()
                                                self.genre_by_name[info.genre.lower()] = new_id
                                                #print(f"Update genre to {info.genre} for {r['artist_name']} - {r['title']} - {r['album_name']})")
                                                self.cursor.execute(Queries.update_tag_map, (self.genre_by_name[info.genre.lower()], r['sid']))
                                        else:
                                            #print("Genre is OK")
                                            pass
                                    else:
                                        #print(f"No genre found for {r['file']}")
                                        pass
                                if info.artist.fullname not in artists:
                                    artists.append(info.artist.fullname)
                                    self.gobject['lblArtist'].set_text(", ".join(artists))
                                    #if len(artists) > 1:
                                    #    if not self.options['no_gui']:
                                    #        yield True
                            else:
                                self.files_no_tags += 1
                            self.update_display()
                        self.cursor.execute("COMMIT")
                        self.gobject['pgrScan'].set_fraction(self.fraction)
                    #if not self.options['no_gui']:
                    #    yield True
            if added_to_catalog:
                print("Files were added to the catalog")
                self.cursor.execute(Queries.update_catalog_addition_time, (int(time()), self.catalog_id))
            if changed_in_catalog or added_to_catalog:
                print("Files were updated in the catalog")
                self.cursor.execute(Queries.update_catalog_update_time, (int(time()), self.catalog_id))

        self.scan_running = False
        print("Scan Completed")
        self.estimated_total_files = self.fcount
        if not estimate:
            self.gobject['pgrScan'].set_fraction(1.0)
            self.update_display()
            #if not self.options['no_gui']:
            #    yield True
            print("Checking for removed songs")
            self.cursor.execute(Queries.select_all_songs)
            to_check = self.cursor.rowcount
            checked = 0
            files_not_found = 0
            self.gobject['pgrScan'].set_fraction(0.0)
            self.gobject['pgrScan'].set_text("Checking for removed files")
            #if not self.options['no_gui']:
            #    yield True
            for row in self.cursor.fetchall():
                checked += 1
                fraction = float(checked) / float(to_check)
                self.gobject['pgrScan'].set_fraction(fraction)
                if not os.path.isfile(row['file']):
                    #print("File not found: ", row)
                    files_not_found += 1
                    self.gobject['files_not_found_label'].set_text(str(files_not_found))
                    self.add_warnings({'filename': row['file'], 'NOT FOUND': 'File not found',
                                      'artist': row['artist_name'],
                                      'album': row['album_name'],
                                      'title': row['title']})
                    self.cursor.execute(Queries.delete_missing_file, (row['sid'],))
                    #if not self.options['no_gui']:
                    #    yield True
                #if checked % 25:
                #    if not self.options['no_gui']:
                #        yield True
            self.gobject['pgrScan'].set_fraction(0.0)
            self.gobject['pgrScan'].set_text("Checking for orphaned albums")
            #if not self.options['no_gui']:
            #    yield True
            self.cursor.execute(Queries.delete_orphan_albums)
            self.gobject['albums_removed_label'].set_text(str(self.cursor.rowcount))
            self.gobject['pgrScan'].set_text("Checking for orphaned artists")
            self.gobject['pgrScan'].set_fraction(0.5)
            #if not self.options['no_gui']:
            #    yield True
            self.cursor.execute(Queries.delete_orphan_artists)
            self.gobject['artists_removed_label'].set_text(str(self.cursor.rowcount))
            self.gobject['pgrScan'].set_text("Completed")
            self.gobject['pgrScan'].set_fraction(1.0)
            self.gobject['button_scan_library'].set_label("Scan Library")
            self.gobject['preferences_imagemenuitem'].set_sensitive(True)
            self.full_scan = False
        else:
            self.estimate_completed = True
            self.scan_running = True
            #if not self.options['no_gui']:
            #    task1 = self.scan_files(estimate=False)
            #    GObject.idle_add(task1.__next__)
        print('nogui', self.options['no_gui'])
        if not self.options['no_gui']:
            pass
            #yield False
        else:
            print('no gui')

    def update_display(self):
        if self.options['no_gui']:
            return
        t = time()
        self.ave2 = (t - self.start_time) / self.fcount
        self.fleft = self.estimated_total_files - self.fcount
        self.ttf = (self.ave2 * self.fleft) / 60
        when_done = strftime("%X", localtime(t + (self.ave2 * self.fleft)))
        self.gobject['est_label'].set_text(str(self.estimated_total_files))
        self.gobject['scanned_label'].set_text(str(self.fcount))
        self.gobject['ignored_label'].set_text(str(self.files_skipped))
        self.gobject['no_change_label'].set_text(str(self.skipped))
        self.gobject['updated_label'].set_text(str(self.mismatch))
        self.gobject['bad_tags_label'].set_text(str(self.files_bad))
        self.gobject['new_label'].set_text(str(self.new_tracks))
        self.gobject['no_tags_label'].set_text(str(self.files_no_tags))
        self.gobject['warnings_label'].set_text(str(self.warnings_count))
        self.gobject['files_not_found_label'].set_text('0')
        self.gobject['artists_removed_label'].set_text('0')
        self.gobject['albums_removed_label'].set_text('0')
        self.gobject['pgrScan'].set_text("%.1f%% (Ave: %.3f, Finish: %s)" % (self.fraction * 100.0, self.ave2, when_done,))

    def check_tags(self, db_row, info):
        res = []
        res.append(self.check_item(db_row, 'artist_short', info.artist.name))
        res.append(self.check_item(db_row, 'artist_prefix', info.artist.prefix))
        res.append(self.check_item(db_row, 'album_short', info.album.name))
        res.append(self.check_item(db_row, 'album_prefix', info.album.prefix))
        res.append(self.check_item(db_row, 'title', info.title))
        res.append(self.check_item(db_row, 'year', info.year))
        res.append(self.check_item(db_row, 'track', info.tracknumber))
        res.append(self.check_item(db_row, 'discnumber', info.discnumber))
        res.append(self.check_item(db_row, 'discyear', info.year))
        if not self.options['program']['ignore_bitrate']:
            res.append(self.check_item(db_row, 'bitrate', info.bitrate))
        res.append(self.check_item(db_row, 'rate', info.sample_rate))
        res.append(self.check_item(db_row, 'time', info.length))
        res.append(self.check_item(db_row, 'size', info.size))

        if True in res:
            return True
        else:
            return False

    def check_item(self, db_row, db_key, tag):
        if db_row[db_key] != tag:
            self.add_changes(db_row['sid'], db_row['file'], db_key, tag, db_row[db_key])
            return True
        return False

    def update_info(self, row, info):
        #print("Update info: ", info, fname)
        artist_id = self.update_table('artist', info.artist)
        album_id = self.update_table('album', info.album)
        try:
            self.cursor.execute(Queries.update_song, (artist_id, album_id, info.title,
                          info.year, info.sample_rate, info.bitrate, info.size, info.length,
                          info.tracknumber, info.modification_time, time(), row['sid']))
        except:
            print("Error updating song:", info.title)
            print("Possible bad bitrate, setting to 0 and trying again. Bitrate:", info.bitrate)
            self.cursor.execute(Queries.update_song, (artist_id, album_id, info.title,
                          info.year, info.sample_rate, 0, info.size, info.length,
                          info.tracknumber, info.modification_time, time(), row['sid']))

    def update_table(self, table, info):
        queryt = Template(Queries.select_artist_or_album)
        fields = [info.name]
        if info.prefix is None:
            p = "AND prefix IS NULL"
        else:
            p = "AND prefix = %s"
            fields.append(info.prefix)
        if table == 'album':
            if info.disc is None:
                dtemp = "AND disk IS NULL"
            else:
                dtemp = "AND disk = %s"
                fields.append(info.disc)
            ytemp = "AND year = %s"
            fields.append(info.year)
        else:
            dtemp = ''
            ytemp = ''
        query = queryt.substitute(table=table, prefix=p, disc=dtemp, year=ytemp)
        self.cursor.execute(query, fields)
        if self.cursor.rowcount == 0:
            if table == 'album':
                id = self.insert_new_album(info)
            else:
                id = self.insert_new_artist(fields)
        else:
            id = None
            for r in self.cursor.fetchall():
                if r['full_name'] == info.fullname:
                    id = r['id']
                    break
            if id is None:
                if table == 'artist':
                    id = self.insert_new_artist(fields)
                else:
                    id = self.insert_new_album(info)
        return id

    def insert_new_album(self, info):
        self.cursor.execute(Queries.insert_album, (info.name, info.prefix, info.disc, info.year))
        return self.cursor.lastrowid

    def insert_new_artist(self, fields):
        if len(fields) == 1:
            fields.append(None)
        self.cursor.execute(Queries.insert_artist, fields)
        return self.cursor.lastrowid

    def add_new_tag_map(self, info, track_id):
        if info.genre is not None:
            if info.genre.lower() in self.genre_by_name.keys():
                #print(f"Adding genre {info.genre} to {track_id}")
                self.cursor.execute(Queries.insert_tag_map, (self.genre_by_name[info.genre.lower()], track_id))
            else:
                #print(f"Adding new Genre {info.genre} to tag table")
                self.cursor.execute(Queries.insert_tag, (info.genre,))
                new_id = self.cursor.lastrowid
                self.genre_by_id[new_id] = info.genre.lower()
                self.genre_by_name[info.genre.lower()] = new_id
                #print(f"Adding genre {info.genre} for {track_id}")
                self.cursor.execute(Queries.insert_tag_map, (self.genre_by_name[info.genre.lower()], track_id))

    def add_new_track(self, file):
        try:
            info = SimpleTag(file, self.options['program'])
        except:
            print(f'Bad tags in {file}')
            self.files_bad += 1
            return False
        if info.warnings:
            self.add_warnings(info.warnings)
            
        if not info.raw_tags:
            self.files_bad += 1
            return False
        art_id = self.update_table('artist', info.artist)
        alb_id = self.update_table('album', info.album)
        now = int(time())
        values = [alb_id, art_id, file, self.catalog_id, now, now, info.title, info.year, info.bitrate, info.sample_rate,
             info.size, info.length, info.tracknumber, info.modification_time]
        try:
            self.cursor.execute(Queries.insert_song, values)
        except pymysql.err.DataError:
            print(f'Bad year found in {file}: {info.year}')
            values[7] = 0 # Zero the year if invalid
            self.cursor.execute(Queries.insert_song, values)
        self.add_new_tag_map(info, self.cursor.lastrowid)
        self.new_tracks += 1
        self.gobject['lblArtist'].set_text(info.artist.fullname)
        self.gobject['lblAlbum'].set_text(info.album.fullname)
        self.gobject['lblTitle'].set_text(info.title)
        self.gobject['new_liststore'].append((info.artist.fullname, info.album.fullname, info.title, info.tracknumber, file))
        return True

    def add_warnings(self, warnings):
        self.warnings_count += 1
        fp, fn = os.path.split(warnings['filename'])
        wsa = self.gobject['warningsstore'].append
        parent = wsa(None, (0, fn, 'path', fp))
        for tag, warning in warnings.items():
            if tag == 'filename':
                continue
            if type(warning) is list:
                parent1 = wsa(parent, (0, None, tag, warning[0]))
                for w in warning[1:]:
                    wsa(parent1, (0, None, None, w))
            else:
                wsa(parent, (0, None, tag, warning))

    def add_changes(self, id, file, tag, filetag, dbtag):
        csa = self.gobject['changedstore'].append
        if id in self._changed_iters:
            csa(self._changed_iters[id], (None, None, tag, str(filetag), str(dbtag)))
        else:
            self._changed_iters[id] = csa(None, (id, file, tag, str(filetag), str(dbtag)))

    def get_current_prefixes(self):
        print("Looking for current prefixes")
        prefixes = set()
        for table in ('album', 'artist'):
            self.cursor.execute(Queries.get_current_prefixes.format(table))
            for row in self.cursor.fetchall():
                if row['prefix']:
                    prefixes.add(row['prefix'].lower())
        self._prefixes = list(prefixes)

    def update_prefixes(self):
        self.gobject['deleted_prefixes_label'].set_text(", ".join(self.deleted))
        self.gobject['added_prefixes_label'].set_text(", ".join(self.added))
        self.gobject['prefix_progressbar'].set_fraction(0.0)
        #if not self.options['no_gui']:
        #    yield True
        for table in ('artist', 'album'):
            for p in self.deleted:
                self.cursor.execute(Queries.get_prefixes_to_delete.format(table), (p,))
                if self.cursor.rowcount > 0:
                    total = float(self.cursor.rowcount)
                    count = 0.0
                    for row in self.cursor.fetchall():
                        count += 1.0
                        name = row['prefix'] + " " + row['name']
                        self.cursor.execute(Queries.update_deleted_prefix.format(table), (name, row['id']))
                        self.gobject['prefix_progressbar'].set_fraction(count / total)
                        #if not self.options['no_gui']:
                        #    yield True
            for p in self.added:
                pp = p + " %"
                self.cursor.execute(Queries.get_prefixes_to_add.format(table), (pp,))
                if self.cursor.rowcount > 0:
                    total = float(self.cursor.rowcount)
                    count = 0.0
                    for row in self.cursor.fetchall():
                        count += 1.0
                        try:
                            prefix, name = row['name'].split(" ", 1)
                        except:
                            print("Not changing to a prefix, only one value: ", row['name'])
                        else:
                            self.cursor.execute(Queries.update_added_prefix.format(table), (name, prefix, row['id']))
                        self.gobject['prefix_progressbar'].set_fraction(count / total)
                        #if not self.options['no_gui']:
                        #    yield True
        self.gobject['prefix_progressbar'].set_fraction(0.0)
        self.gobject['prefix_progressbar'].set_text('Completed')
        self.gobject['prefix_change_messagedialog'].hide()
        #if not self.options['no_gui']:
        #    yield False
