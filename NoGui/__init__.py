__author__ = 'brian'

from LibScan import LibScan
from gladeobjects import get_glade_objects

class NoGui(object):
    def __init__(self, configfile, options):
        print(f'DJDB: Scanning {options["db"]["database"]}@{options["db"]["server"]}')
        gobject = get_glade_objects(None)
        ls = LibScan(None, configfile, options, gobject)
        print('Starting scan')
        ls.scan_files()
