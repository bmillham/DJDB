__author__ = 'brian'

from LibScan import LibScan

class NoGui(object):
    def __init__(self, configfile, options):
        print(f'DJDB: Scanning {options["db"]["database"]}@{options["db"]["server"]}')
        ls = LibScan(None, configfile, options, None)
        print('Starting scan')
        ls.scan_files()
