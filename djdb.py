#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import argparse

parser = argparse.ArgumentParser(description="Create/update an Ampache database for IDJC")
parser.add_argument('-n', '--no-gui',
                    action='store_true',
                    help='Just run the scan with no gui')
args = parser.parse_args()

if not args.no_gui:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gladeobjects import get_glade_objects, field_names
    from LibScan import LibScan

from os.path import dirname, realpath, join, expanduser
import pickle

home = expanduser("~")
configfile = join(home, ".djdb.p")
gladefile = join(dirname(realpath(__file__)), "djdb.glade")
print('loading pickle')
try:
    options = pickle.load(open(configfile, "rb"))
except:
    options = None
try:
    if 'ignore_bitrate' not in options['program']:
        print("ignore_bitrate was not in options, setting to default of True")
        options['program']['ignore_bitrate'] = True
except:
    # No file
    pass

options['no_gui'] = args.no_gui
if args.no_gui:
    from NoGui import NoGui
    ng = NoGui(configfile, options)
    exit(0)

print('starting builder')
builder = Gtk.Builder()
try:
    builder.add_from_file(gladefile)
except Exception as e:
    print("Unable to find glade file: ", gladefile, e)
    exit()
print('getting objects')
gobject = get_glade_objects(builder)
print('connecting signals')
builder.connect_signals(LibScan(builder, configfile, options, gobject))

if options is None:
    print("No options file, running setup")
    #gobject['firstrun_assistant'].show_all() 
    gobject['assistant1'].show_all()
else:
    gobject['main_window'].show_all()
    gobject['main_window'].set_title('DJDB: {}@{}'.format(options['db']['database'], options['db']['server']))
print('starting main')
Gtk.main()
