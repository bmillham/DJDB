"""
    Keep all SQL in here to easier maintenence, and clean up reading the code
"""

update_catalog_name = "UPDATE catalog SET name = %s WHERE id = %s"
update_catalog_update_time = "UPDATE catalog SET last_update = %s WHERE id = %s"
update_catalog_addition_time = "UPDATE catalog SET last_add = %s WHERE id = %s"
get_catalogs = """SELECT catalog.id AS cid, name, path
                  FROM catalog
                  LEFT JOIN catalog_local ON catalog.id = catalog_id
                  WHERE enabled = 1
                  ORDER BY name"""
add_modification_time = "ALTER TABLE song ADD modification_time INT(11) unsigned DEFAULT 0"
select_song_by_filename = """SELECT song.id AS sid, file, catalog, album, song.year, artist,
                                    title, bitrate, rate, mode, size, time, track,
                                    song.mbid, played, enabled, update_time,
                                    addition_time, update_time, modification_time,
                                    concat_ws(" ", artist.prefix, artist.name) AS artist_name,
                                    concat_ws(" ", album.prefix, album.name) AS album_name,
                                    artist.name AS artist_short,
                                    artist.prefix AS artist_prefix,
                                    album.name AS album_short,
                                    album.prefix AS album_prefix,
                                    album.disk AS discnumber,
                                    album.year AS discyear
                             FROM song
                             LEFT JOIN artist ON artist.id = song.artist
                             LEFT JOIN album ON album.id = song.album
                             WHERE file = %s"""
select_all_songs = """SELECT song.id AS sid,
                             file,
                             title,
                             concat_ws(" ", artist.prefix, artist.name) AS artist_name,
                             concat_ws(" ", album.prefix, album.name) AS album_name
                       FROM song
                       LEFT JOIN artist ON artist.id = song.artist
                       LEFT JOIN album ON album.id = song.album"""

update_song_modification_time = 'UPDATE song SET modification_time = %s WHERE id = %s'
update_song = """UPDATE song SET artist=%s,
                                 album=%s,
                                 title=%s,
                                 year=%s,
                                 rate=%s,
                                 bitrate=%s,
                                 size=%s,
                                 time=%s,
                                 track=%s,
                                 modification_time=%s,
                                 update_time=%s
                             WHERE id = %s"""
# Uses a Template
select_artist_or_album = """SELECT *,
                                   CONCAT_WS(" ", prefix, name) AS full_name
                            FROM $table
                            WHERE name = %s $prefix $disc $year"""
insert_album = "INSERT INTO album (name, prefix, disk, year) VALUES (%s,%s,%s,%s)"
insert_artist = "INSERT INTO artist (name, prefix) VALUES (%s, %s)"
insert_song = """INSERT INTO song (album,
                                   artist,
                                   file,
                                   catalog,
                                   update_time,
                                   addition_time,
                                   title,
                                   year,
                                   bitrate,
                                   rate,
                                   size,
                                   time,
                                   track,
                                   modification_time)
                        VALUES (%s)""" % ",".join(['%s']*14)

delete_orphan_albums = "DELETE FROM album WHERE id NOT IN (SELECT album FROM song)"
delete_orphan_artists = "DELETE FROM artist WHERE id NOT IN (SELECT artist FROM song)"
delete_missing_file = "DELETE FROM song WHERE id = %s"

get_current_prefixes = "SELECT prefix FROM {} GROUP BY prefix"
get_prefixes_to_delete = "SELECT id, prefix, name FROM {} WHERE prefix = %s"
update_deleted_prefix = "UPDATE {} SET name = %s, prefix = NULL WHERE id = %s"
get_prefixes_to_add = "SELECT id, name FROM {} WHERE name LIKE %s AND prefix IS NULL"
update_added_prefix = "UPDATE {} SET name = %s, prefix = %s WHERE id = %s"

