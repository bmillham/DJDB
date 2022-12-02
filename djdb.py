#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from os.path import dirname, realpath, join, expanduser
import pickle
from gladeobjects import get_glade_objects, field_names
from LibScan import LibScan
# Hack to fix unicode issues in Python 2.7
#import sys
#reload(sys)
#sys.setdefaultencoding("UTF8")

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
