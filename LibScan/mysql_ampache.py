database_creator = """CREATE DATABASE `%s` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci"""

catalog_creator = """INSERT INTO catalog (name, catalog_type, last_update, last_clean, last_add,
                     enabled, rename_pattern, sort_pattern)
                     VALUES (%s, 'local', %s, %s, %s, 1, '%%a - %%T - %%t', '%%a/%%A')"""

catalog_local_creator = """INSERT INTO catalog_local (path, catalog_id) VALUES (%s, %s)"""

database_tables = {}
database_constraints = {}

database_tables['access_list'] = """CREATE TABLE IF NOT EXISTS `access_list` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `start` varbinary(255) NOT NULL,
  `end` varbinary(255) NOT NULL,
  `level` smallint(3) unsigned NOT NULL DEFAULT '5',
  `type` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `user` int(11) NOT NULL,
  `enabled` tinyint(1) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `start` (`start`),
  KEY `end` (`end`),
  KEY `level` (`level`),
  KEY `enabled` (`enabled`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['accounts'] = """
CREATE TABLE IF NOT EXISTS `accounts` (
  `id` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
"""

database_tables['account_groups'] = """
CREATE TABLE IF NOT EXISTS `account_groups` (
  `account_id` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `group_id` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  KEY `account_id` (`account_id`),
  KEY `group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
"""

database_tables['album'] = """CREATE TABLE IF NOT EXISTS `album` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `prefix` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `mbid` varchar(36) CHARACTER SET utf8 DEFAULT NULL,
  `year` int(4) unsigned NOT NULL DEFAULT '1984',
  `disk` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `year` (`year`),
  KEY `disk` (`disk`),
  FULLTEXT KEY `name_2` (`name`),
  FULLTEXT KEY `idjc` (`name`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['artist'] = """CREATE TABLE IF NOT EXISTS `artist` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `prefix` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `mbid` varchar(1369) CHARACTER SET utf8 DEFAULT NULL,
  `summary` text CHARACTER SET utf8,
  `placeformed` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `yearformed` int(4) DEFAULT NULL,
  `last_update` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  FULLTEXT KEY `name_2` (`name`),
  FULLTEXT KEY `idjc` (`name`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['broadcast'] = """CREATE TABLE IF NOT EXISTS `broadcast` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` int(11) unsigned NOT NULL,
  `name` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `description` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `is_private` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `song` int(11) unsigned NOT NULL DEFAULT '0',
  `started` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `listeners` int(11) unsigned NOT NULL DEFAULT '0',
  `key` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['catalog'] = """CREATE TABLE IF NOT EXISTS `catalog` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `catalog_type` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `last_update` int(11) unsigned NOT NULL DEFAULT '0',
  `last_clean` int(11) unsigned DEFAULT NULL,
  `last_add` int(11) unsigned NOT NULL DEFAULT '0',
  `enabled` tinyint(1) unsigned NOT NULL DEFAULT '1',
  `rename_pattern` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `sort_pattern` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `gather_types` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `enabled` (`enabled`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['catalog_local'] = """CREATE TABLE IF NOT EXISTS `catalog_local` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `path` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `catalog_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['catalog_remote'] = """CREATE TABLE IF NOT EXISTS `catalog_remote` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uri` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `catalog_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['channel'] = """CREATE TABLE IF NOT EXISTS `channel` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `description` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `url` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `interface` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `port` int(11) unsigned NOT NULL DEFAULT '0',
  `fixed_endpoint` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `object_type` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `object_id` int(11) unsigned NOT NULL,
  `is_private` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `random` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `loop` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `admin_password` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `start_date` int(11) unsigned NOT NULL DEFAULT '0',
  `max_listeners` int(11) unsigned NOT NULL DEFAULT '0',
  `peak_listeners` int(11) unsigned NOT NULL DEFAULT '0',
  `listeners` int(11) unsigned NOT NULL DEFAULT '0',
  `connections` int(11) unsigned NOT NULL DEFAULT '0',
  `stream_type` varchar(8) CHARACTER SET utf8 DEFAULT NULL,
  `bitrate` int(11) unsigned NOT NULL DEFAULT '128',
  `pid` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['democratic'] = """CREATE TABLE IF NOT EXISTS `democratic` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `cooldown` tinyint(4) unsigned DEFAULT NULL,
  `level` tinyint(4) unsigned NOT NULL DEFAULT '25',
  `user` int(11) NOT NULL,
  `primary` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `base_playlist` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `level` (`level`),
  KEY `primary_2` (`primary`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['dynamic_playlist'] = """CREATE TABLE IF NOT EXISTS `dynamic_playlist` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `user` int(11) NOT NULL,
  `date` int(11) unsigned NOT NULL,
  `type` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['dynamic_playlist_data'] = """CREATE TABLE IF NOT EXISTS `dynamic_playlist_data` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `dynamic_id` int(11) unsigned NOT NULL,
  `field` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `internal_operator` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `external_operator` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `value` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['groups'] = """
CREATE TABLE IF NOT EXISTS `groups` (
  `id` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
"""

database_tables['group_perms'] = """
CREATE TABLE IF NOT EXISTS `groups` (
  `id` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
"""

database_tables['image'] = """CREATE TABLE IF NOT EXISTS `image` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `image` mediumblob NOT NULL,
  `mime` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `size` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `object_type` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `object_id` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `object_type` (`object_type`),
  KEY `object_id` (`object_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['ip_history'] = """CREATE TABLE IF NOT EXISTS `ip_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `ip` varbinary(255) DEFAULT NULL,
  `date` int(11) unsigned NOT NULL DEFAULT '0',
  `agent` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `username` (`user`),
  KEY `date` (`date`),
  KEY `ip` (`ip`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['listeners'] = """
CREATE TABLE IF NOT EXISTS `listeners` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current` int(11) NOT NULL DEFAULT '0',
  `max` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1
"""

database_tables['live_stream'] = """CREATE TABLE IF NOT EXISTS `live_stream` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `site_url` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `url` varchar(4096) CHARACTER SET utf8 DEFAULT NULL,
  `genre` int(11) unsigned NOT NULL DEFAULT '0',
  `catalog` int(11) unsigned NOT NULL DEFAULT '0',
  `codec` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `catalog` (`catalog`),
  KEY `genre` (`genre`),
  KEY `name` (`name`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['localplay_httpq'] = """CREATE TABLE IF NOT EXISTS `localplay_httpq` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `owner` int(11) NOT NULL,
  `host` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `port` int(11) unsigned NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `access` smallint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['localplay_mpd'] = """CREATE TABLE IF NOT EXISTS `localplay_mpd` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `owner` int(11) NOT NULL,
  `host` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `port` int(11) unsigned NOT NULL DEFAULT '6600',
  `password` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `access` smallint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['localplay_shoutcast'] = """CREATE TABLE IF NOT EXISTS `localplay_shoutcast` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `owner` int(11) NOT NULL,
  `pid` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `playlist` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `local_root` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `access` smallint(4) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['mistags'] = """
CREATE TABLE IF NOT EXISTS `mistags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `track_id` int(11) NOT NULL,
  `reported_by` text NOT NULL,
  `reported` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `artist` text NOT NULL,
  `album` text NOT NULL,
  `title` text NOT NULL,
  `comments` varchar(2000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8
"""

database_tables['now_playing'] = """CREATE TABLE IF NOT EXISTS `now_playing` (
  `id` varchar(64) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `object_id` int(11) unsigned NOT NULL,
  `object_type` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `user` int(11) NOT NULL,
  `expire` int(11) unsigned NOT NULL DEFAULT '0',
  `insertion` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `expire` (`expire`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['object_count'] = """CREATE TABLE IF NOT EXISTS `object_count` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `object_type` enum('album','artist','song','playlist','genre','catalog','live_stream','video') CHARACTER SET utf8 DEFAULT NULL,
  `object_id` int(11) unsigned NOT NULL DEFAULT '0',
  `date` int(11) unsigned NOT NULL DEFAULT '0',
  `user` int(11) unsigned NOT NULL,
  `agent` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `object_type` (`object_type`),
  KEY `object_id` (`object_id`),
  KEY `userid` (`user`),
  KEY `date` (`date`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['played'] = """CREATE TABLE IF NOT EXISTS `played` (
  `played_id` int(11) NOT NULL AUTO_INCREMENT,
  `track_id` int(11) NOT NULL,
  `date_played` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `played_by` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `played_by_me` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`played_id`),
  UNIQUE KEY `song_and_time` (`track_id`,`date_played`),
  KEY `track_id` (`track_id`),
  KEY `played_by_me` (`played_by_me`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['permissions'] = """
CREATE TABLE IF NOT EXISTS `permissions` (
  `id` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
"""


database_tables['player_control'] = """CREATE TABLE IF NOT EXISTS `player_control` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` int(11) unsigned NOT NULL,
  `cmd` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `value` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `object_type` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `object_id` int(11) unsigned NOT NULL,
  `send_date` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['playlist'] = """CREATE TABLE IF NOT EXISTS `playlist` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `type` enum('private','public') CHARACTER SET utf8 DEFAULT NULL,
  `date` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `type` (`type`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['playlist_data'] = """CREATE TABLE IF NOT EXISTS `playlist_data` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `playlist` int(11) unsigned NOT NULL DEFAULT '0',
  `object_id` int(11) unsigned DEFAULT NULL,
  `object_type` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `track` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `playlist` (`playlist`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['preference'] = """CREATE TABLE IF NOT EXISTS `preference` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `value` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `level` int(11) unsigned NOT NULL DEFAULT '100',
  `type` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `catagory` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `catagory` (`catagory`),
  KEY `name` (`name`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['rating'] = """CREATE TABLE IF NOT EXISTS `rating` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `object_type` enum('artist','album','song','steam','video') CHARACTER SET utf8 DEFAULT NULL,
  `object_id` int(11) unsigned NOT NULL DEFAULT '0',
  `rating` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_rating` (`user`,`object_type`,`object_id`),
  KEY `object_id` (`object_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['recommendation'] = """CREATE TABLE IF NOT EXISTS `recommendation` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `object_type` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `object_id` int(11) unsigned NOT NULL,
  `last_update` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['recommendation_item'] = """CREATE TABLE IF NOT EXISTS `recommendation_item` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `recommendation` int(11) unsigned NOT NULL,
  `recommendation_id` int(11) unsigned DEFAULT NULL,
  `name` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `rel` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `mbid` varchar(1369) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['requestlist'] = """CREATE TABLE IF NOT EXISTS `requestlist` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `songID` int(11) NOT NULL DEFAULT '0',
  `t_stamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `host` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `msg` text CHARACTER SET utf8,
  `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `code` mediumint(9) NOT NULL DEFAULT '0',
  `ETA` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `status` enum('played','ignored','pending','new') CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `t_stamp` (`t_stamp`),
  KEY `songID` (`songID`),
  KEY `status` (`status`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['search'] = """CREATE TABLE IF NOT EXISTS `search` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `type` enum('private','public') CHARACTER SET utf8 DEFAULT NULL,
  `rules` mediumtext COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `logic_operator` varchar(3) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['session'] = """CREATE TABLE IF NOT EXISTS `session` (
  `id` varchar(256) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `username` varchar(16) CHARACTER SET utf8 DEFAULT NULL,
  `expire` int(11) unsigned NOT NULL DEFAULT '0',
  `value` longtext COLLATE utf8_unicode_ci NOT NULL,
  `ip` varbinary(255) DEFAULT NULL,
  `type` varchar(16) CHARACTER SET utf8 DEFAULT NULL,
  `agent` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `expire` (`expire`),
  KEY `type` (`type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['session_stream'] = """CREATE TABLE IF NOT EXISTS `session_stream` (
  `id` varchar(64) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `user` int(11) unsigned NOT NULL,
  `agent` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `expire` int(11) unsigned NOT NULL,
  `ip` varbinary(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['share'] = """CREATE TABLE IF NOT EXISTS `share` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` int(11) unsigned NOT NULL,
  `object_type` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `object_id` int(11) unsigned NOT NULL,
  `allow_stream` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `allow_download` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `expire_days` int(4) unsigned NOT NULL DEFAULT '0',
  `max_counter` int(4) unsigned NOT NULL DEFAULT '0',
  `secret` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `counter` int(4) unsigned NOT NULL DEFAULT '0',
  `creation_date` int(11) unsigned NOT NULL DEFAULT '0',
  `lastvisit_date` int(11) unsigned NOT NULL DEFAULT '0',
  `public_url` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['site_options'] = """
CREATE TABLE IF NOT EXISTS `site_options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `show_title` text NOT NULL,
  `menu_background_color` text NOT NULL,
  `menu_foreground_color` text NOT NULL,
  `menu_highlight_background` text NOT NULL,
  `menu_highlight_foreground` text NOT NULL,
  `table_header_background` text NOT NULL,
  `table_header_foreground` text NOT NULL,
  `sort_header_background` text NOT NULL,
  `sort_header_foreground` text NOT NULL,
  `sort_odd_background` text NOT NULL,
  `sort_odd_foreground` text NOT NULL,
  `sort_even_background` text NOT NULL,
  `sort_even_foreground` text NOT NULL,
  `show_time` text NOT NULL,
  `show_end` text NOT NULL,
  `limit_requests` int(11) NOT NULL DEFAULT '0',
  `offset` int(11) NOT NULL DEFAULT '0',
  `catalog` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8
"""

database_tables['song'] = """CREATE TABLE IF NOT EXISTS `song` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `file` varchar(512) CHARACTER SET utf8 DEFAULT NULL,
  `catalog` int(11) unsigned NOT NULL DEFAULT '0',
  `album` int(11) unsigned NOT NULL DEFAULT '0',
  `year` mediumint(4) unsigned NOT NULL DEFAULT '0',
  `artist` int(11) unsigned NOT NULL DEFAULT '0',
  `title` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `bitrate` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `rate` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `mode` enum('abr','vbr','cbr') CHARACTER SET utf8 DEFAULT NULL,
  `size` int(11) unsigned NOT NULL DEFAULT '0',
  `time` smallint(5) unsigned NOT NULL DEFAULT '0',
  `track` smallint(5) unsigned DEFAULT NULL,
  `mbid` varchar(36) CHARACTER SET utf8 DEFAULT NULL,
  `played` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `enabled` tinyint(1) unsigned NOT NULL DEFAULT '1',
  `update_time` int(11) unsigned DEFAULT '0',
  `addition_time` int(11) unsigned DEFAULT '0',
  `modification_time` int(11) unsigned DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `album` (`album`),
  KEY `artist` (`artist`),
  KEY `update_time` (`update_time`),
  KEY `addition_time` (`addition_time`),
  KEY `catalog` (`catalog`),
  KEY `played` (`played`),
  KEY `enabled` (`enabled`),
  KEY `file` (`file`(333)),
  FULLTEXT KEY `idjc` (`title`),
  FULLTEXT KEY `title` (`title`,`file`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['song_data'] = """CREATE TABLE IF NOT EXISTS `song_data` (
  `song_id` int(11) unsigned NOT NULL,
  `comment` text COLLATE utf8_unicode_ci,
  `lyrics` text COLLATE utf8_unicode_ci,
  `label` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `catalog_number` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `language` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `waveform` mediumblob,
  UNIQUE KEY `song_id` (`song_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['song_preview'] = """CREATE TABLE IF NOT EXISTS `song_preview` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `session` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `artist` int(11) DEFAULT NULL,
  `artist_mbid` varchar(1369) CHARACTER SET utf8 DEFAULT NULL,
  `title` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `album_mbid` varchar(36) CHARACTER SET utf8 DEFAULT NULL,
  `mbid` varchar(36) CHARACTER SET utf8 DEFAULT NULL,
  `disk` int(11) DEFAULT NULL,
  `track` int(11) DEFAULT NULL,
  `file` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['stream_playlist'] = """CREATE TABLE IF NOT EXISTS `stream_playlist` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `sid` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `url` text COLLATE utf8_unicode_ci NOT NULL,
  `info_url` text COLLATE utf8_unicode_ci,
  `image_url` text COLLATE utf8_unicode_ci,
  `title` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `author` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `album` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `time` smallint(5) DEFAULT NULL,
  `codec` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sid` (`sid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['suggestions'] = """CREATE TABLE IF NOT EXISTS `suggestions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `album` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `artist` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `suggestor` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `comments` varchar(2048) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['tag'] = """CREATE TABLE IF NOT EXISTS `tag` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  UNIQUE KEY `name` (`name`),
  KEY `map_id` (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['tag_map'] = """CREATE TABLE IF NOT EXISTS `tag_map` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tag_id` int(11) unsigned NOT NULL,
  `object_id` int(11) unsigned NOT NULL,
  `object_type` varchar(16) CHARACTER SET utf8 DEFAULT NULL,
  `user` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `object_id` (`object_id`),
  KEY `object_type` (`object_type`),
  KEY `user_id` (`user`),
  KEY `tag_id` (`tag_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['tmp_browse'] = """CREATE TABLE IF NOT EXISTS `tmp_browse` (
  `id` int(13) NOT NULL AUTO_INCREMENT,
  `sid` varchar(128) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `object_data` longtext COLLATE utf8_unicode_ci,
  PRIMARY KEY (`sid`,`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['tmp_playlist'] = """CREATE TABLE IF NOT EXISTS `tmp_playlist` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `session` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `type` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `object_type` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `session` (`session`),
  KEY `type` (`type`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['tmp_playlist_data'] = """CREATE TABLE IF NOT EXISTS `tmp_playlist_data` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tmp_playlist` int(11) unsigned NOT NULL,
  `object_type` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `object_id` int(11) unsigned NOT NULL,
  `track` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tmp_playlist` (`tmp_playlist`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['update_info'] = """CREATE TABLE IF NOT EXISTS `update_info` (
  `key` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `value` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  UNIQUE KEY `key` (`key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['user'] = """CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `fullname` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `email` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `website` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `apikey` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `password` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `access` tinyint(4) unsigned NOT NULL,
  `disabled` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `last_seen` int(11) unsigned NOT NULL DEFAULT '0',
  `create_date` int(11) unsigned DEFAULT NULL,
  `validation` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['user_catalog'] = """CREATE TABLE IF NOT EXISTS `user_catalog` (
  `user` int(11) unsigned NOT NULL,
  `catalog` int(11) unsigned NOT NULL,
  `level` smallint(4) unsigned NOT NULL DEFAULT '5',
  KEY `user` (`user`),
  KEY `catalog` (`catalog`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['user_flag'] = """CREATE TABLE IF NOT EXISTS `user_flag` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `object_id` int(11) unsigned NOT NULL,
  `object_type` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `date` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_userflag` (`user`,`object_type`,`object_id`),
  KEY `object_id` (`object_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['user_preference'] = """CREATE TABLE IF NOT EXISTS `user_preference` (
  `user` int(11) NOT NULL,
  `preference` int(11) unsigned NOT NULL DEFAULT '0',
  `value` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  KEY `user` (`user`),
  KEY `preference` (`preference`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['user_shout'] = """CREATE TABLE IF NOT EXISTS `user_shout` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `text` text COLLATE utf8_unicode_ci NOT NULL,
  `date` int(11) unsigned NOT NULL,
  `sticky` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `object_id` int(11) unsigned NOT NULL,
  `object_type` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `data` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sticky` (`sticky`),
  KEY `date` (`date`),
  KEY `user` (`user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['user_vote'] = """CREATE TABLE IF NOT EXISTS `user_vote` (
  `user` int(11) unsigned NOT NULL,
  `object_id` int(11) unsigned NOT NULL,
  `date` int(11) unsigned NOT NULL,
  KEY `user` (`user`),
  KEY `object_id` (`object_id`),
  KEY `date` (`date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['video'] = """CREATE TABLE IF NOT EXISTS `video` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `file` varchar(4096) CHARACTER SET utf8 DEFAULT NULL,
  `catalog` int(11) unsigned NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `video_codec` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `audio_codec` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `resolution_x` mediumint(8) unsigned NOT NULL,
  `resolution_y` mediumint(8) unsigned NOT NULL,
  `time` int(11) unsigned NOT NULL,
  `size` bigint(20) unsigned NOT NULL,
  `mime` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `addition_time` int(11) unsigned NOT NULL,
  `update_time` int(11) unsigned DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `file` (`file`(333)),
  KEY `enabled` (`enabled`),
  KEY `title` (`title`),
  KEY `addition_time` (`addition_time`),
  KEY `update_time` (`update_time`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_tables['wanted'] = """CREATE TABLE IF NOT EXISTS `wanted` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `artist` int(11) DEFAULT NULL,
  `artist_mbid` varchar(1369) CHARACTER SET utf8 DEFAULT NULL,
  `mbid` varchar(36) CHARACTER SET utf8 DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `year` int(4) DEFAULT NULL,
  `date` int(11) unsigned NOT NULL DEFAULT '0',
  `accepted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_wanted` (`user`,`artist`,`mbid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

database_constraints['account_groups'] = """
ALTER TABLE `account_groups`
  ADD CONSTRAINT `account_groups_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`),
  ADD CONSTRAINT `account_groups_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`)
"""

database_constraints['group_perms'] = """
ALTER TABLE `group_perms`
  ADD CONSTRAINT `group_perms_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`),
  ADD CONSTRAINT `group_perms_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`)
"""

