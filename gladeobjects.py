glade_objects = ('main_window', 'lblDirectory', 'lblCatalog', 'lblArtist', 'lblAlbum', 'lblTitle',
                 'pgrScan', 'preferences_dialog', 'cattreestore', 'catliststore', 'about_dialog', 'filechooserdialog1',
                 'firstrun_assistant', 'firstrun_assistant_database_box', 'import_db_page_new_box',
                 'setupdialog', 'setup_dialog_spinner', 'est_label', 'scanned_label', 'ignored_label',
                 'no_change_label', 'updated_label', 'bad_tags_label', 'new_label',
                 'database_server_entry', 'database_name_entry', 'database_user_entry', 'database_password_entry',
                 'create_database_switch', 'assistant1', 'import_db_label_server_confirm',
                 'import_db_label_database_confirm', 'import_db_label_user_confirm',
                 'import_db_label_password_confirm', 'import_db_label_question_confirm', 'import_db_label_catalog',
                 'assistant_db_entry_server1', 'assistant_db_entry_user1', 'assistant_db_entry_password1',
                 'assistant_db_entry_database1', 'existing_database_radiobutton', 'new_database_radiobutton',
                 'filechooserbutton1', 'new_catalog_entry', 
                 'new_catalog_dialog', 'new_catalog_name_entry',
                 'new_catalog_filechooser_button', 'warningwindow', 'warningsstore', 'database_message_dialog',
                 'button_scan_library', 'files_not_found_label', 'no_tags_label', 'artists_removed_label',
                 'albums_removed_label', 'warnings_label', 'create_catalog_box', 'prefix_entry',
                 'valid_filetypes_textview', 'valid_filetypes_textbuffer', 'dash_checkbutton', 'no_tracknumber_checkbutton',
                 'fix_spaces_checkbutton', 'db_error_messagedialog', 'prefix_change_messagedialog',
                 'ignorebitrate_checkbutton',
                 'preferences_imagemenuitem', 'changedwindow', 'changedstore', 'new_window', 'new_liststore',
                 'deleted_prefixes_label', 'added_prefixes_label', 'prefix_progressbar', 'upgrade_imagemenuitem',
                 'upgrade_dialog')
field_names = ('server', 'database', 'user', 'password')
assistant_object_names = ('assistant_db_entry', 'import_db_entry', 'import_db_label', 'new_db_label')

class MyGObject(object):
    """ Mimic a gobject basic functions with basic features that print
        instead of updating a gui. Used with the --no-gui option """
    def __init__(self):
        pass # Don't need to do anything on init

    """ Fake gobject methods here that just print """
    def set_text(self, text):
        print(text)

    def set_label(self, text):
        print(text)

    def clear(self):
        pass # Don't need to do anything here

    def set_sensitive(self, value):
        pass

    def set_fraction(self, value):
        pass

    def hide(self):
        pass

def get_glade_objects(builder):
    gobject = {}
    for o in glade_objects:
        if not builder:
            gobject[o] = MyGObject()
        else:
            gobject[o] = builder.get_object(o)
        if gobject[o] is None:
            print("WARNING: object {} not found".format(o))

    for o in assistant_object_names:
        gobject[o] = {}
        for f in field_names:
            if not builder:
                gobject[o][f] = MyGObject()
            else:
                gobject[o][f] = builder.get_object("{0}_{1}".format(o,f))

    gobject['FIELD_NAMES'] = field_names
    gobject['ASSISTANT_OBJECT_NAMES'] = assistant_object_names
    return gobject
