from gi.repository import Gtk, GObject
import os
import cPickle
from time import sleep, time
import MySQLdb as sql
from Database.Ampache import Queries

ADD_DIR_STRING = 'Add New Directory'

import_database_fields = ('import_database_server_entry', 'import_database_name_entry', 'import_database_user_entry', 'import_database_password_entry')

class Handler(object):
    from guiobjects import _on_pulse_timeout, _build_catalog_tree

    def __init__(self, builder, configfile, options, gobject):
        self.builder = builder
        self.configfile = configfile
        self.options = options
        get_object = builder.get_object
        self.scan_running = False
        self.gobject = gobject
        self._build_catalog_tree()
        self.import_db_entry = {}
        self.import_db_label = {}
        self.assistant_db_entry = {}
        self.new_db_label = {}
        self.cursor = None
        self.db_connect()

    def db_connect(self, *args):
        try:
            self.db = sql.connect(db=self.options['db']['database'], user=self.options['db']['user'],
                                  passwd=self.options['db']['password'], host=self.options['db']['server'], charset='utf8')
        except:
            print "Failed to connect to the database"
            self.db = None
        else:
            self.db.autocommit(True)
            self.cursor = self.db.cursor(sql.cursors.DictCursor)
            self.cursor.execute("set time_zone = '-00:00'")

    def on_firstrun_assistant_cancel(self, *args):
        print "Aborting assistant"
        Gtk.main_quit(*args)

    def on_assistant1_cancel(self, *args):
        try:
            if self._creating_new_database:
                self.gobject['assistant1'].hide()
                self._creating_new_database = False
        except:
            Gtk.main_quit(*args)

    def on_assistant_db_server_entry_changed(self, *args):
        self.gobject['firstrun_assistant'].set_page_complete(self.gobject['firstrun_assistant_database_box'], True)

    def import_db_page_box_show_cb(self, *args):
        print "Showing db box"

    def switch1_notify_cb(self, switch, *args):
        self._enable_import_box(switch.get_active())

    def _enable_import_box(self, value):
        for w in self.gobject['import_db_entry'].values():
            self._set_entry(w, value)
        if value:
            self.gobject['import_db_page_new_box'].set_opacity(1.0)
        else:
            self.gobject['import_db_page_new_box'].set_opacity(0.25)

    def _set_entry(self, widget, value):
        widget.set_can_focus(value)
        widget.set_editable(value)

    def on_firstrun_assistant_prepare(self, *args):
        pages = args[0].get_n_pages()
        page = args[0].get_current_page()
        if page == pages - 1:
            for f in self.gobject['FIELD_NAMES']:
                self.gobject['new_db_label'][f].set_text(self.gobject['assistant_db_entry'][f].get_text())
                self.gobject['import_db_label'][f].set_text(self.gobject['import_db_entry'][f].get_text())

    def on_assistant1_prepare(self, *args):
        pages = args[0].get_n_pages()
        page = args[0].get_current_page()
        try:
            new_database = self._create_new_database
        except:
            new_database = False
        if new_database:
            self.gobject['new_database_radiobutton'].set_active(True)
            args[0].set_current_page(1)
            self._create_new_database=False
            self._creating_new_database = True
            page = 1
        if page == 1:
            self.on_new_database_radiobutton_toggled(self.gobject['new_database_radiobutton'])
        if page == pages - 1:
            self.database_server = self.gobject['assistant_db_entry_server1'].get_text()
            self.gobject['import_db_label_server_confirm'].set_text(self.database_server)
            self.database_user = self.gobject['assistant_db_entry_user1'].get_text()
            self.gobject['import_db_label_user_confirm'].set_text(self.database_user)
            self.database_password = self.gobject['assistant_db_entry_password1'].get_text() 
            pw = "*" * len(self.database_password)
            self.gobject['import_db_label_password_confirm'].set_text(pw)
            self.database = self.gobject['assistant_db_entry_database1'].get_text()
            self.gobject['import_db_label_database_confirm'].set_text(self.database)
            if self.gobject['new_database_radiobutton'].get_active():
                self.gobject['import_db_label_question_confirm'].set_text('Create a new database')
                self.catalog_dir = self.gobject['filechooserbutton1'].get_filename()
                self.catalog_name = self.gobject['new_catalog_entry'].get_text()
                self.gobject['import_db_label_catalog'].set_text("Creating catalog {1} using directory {0}".format(self.catalog_dir, self.catalog_name))
                self.create_new_database = True
            else:
                self.gobject['import_db_label_question_confirm'].set_text('Using an existing database')
                self.gobject['import_db_label_catalog'].set_text("Using catalogs in the database")
                self.create_new_database = False

    def on_firstrun_assistant_apply(self, *args):
        print self.configfile
        if self.options is None:
            self.options = {}
            self.options['db'] = {}
            self.options['import_db'] = {}
            for f in self.gobject['FIELD_NAMES']:
                self.options['db'][f] = self.gobject['assistant_db_entry'][f].get_text()
                self.options['import_db'][f] = self.gobject['import_db_entry'][f].get_text()
        cPickle.dump(self.options, open(self.configfile, "wb"))
        self.gobject['setupdialog'].show_all()
        self.gobject['setup_dialog_spinner'].start()
        GObject.timeout_add_seconds(5, self.firstrun_finished)

    def on_assistant1_apply(self, *args):
        print "Applying"
        self.options = {}
        self.options['db'] = {}
        self.options['db']['database'] = self.database
        self.options['db']['server'] = self.database_server
        self.options['db']['user'] = self.database_user
        self.options['db']['password'] = self.database_password
        if self.create_new_database:
            print "Connecting to the server"
            # Special case connection to the server. Connect without a database
            # so the new database can be created
            try:
                self.db = sql.connect(user=self.database_user, passwd=self.database_password, host=self.database_server, charset='utf8')
            except:
                print "Failed to connect to the database server"
                print self.database_user, self.database_password, self.database_server
            else:
                self.create_database()
                self._prefixes = self.default_prefixes
        else:
            self.db_connect()
            if not self.db:
                print "failed to connect to the database"
                self.gobject['db_error_messagedialog'].show()
                return
            self.get_current_prefixes()
        if 'program' not in self.options:
            self.options['program'] = {}
        #self.options['program']['prefixes'] = self._prefixes
        self.options['program']['prefixes'] = self._prefixes
        self.options['program']['tracknumber_warning'] = False
        self.options['program']['dash_warning'] = True
        self.options['program']['fix_spaces'] = True
        cPickle.dump(self.options, open(self.configfile, "wb"))
        self.gobject['assistant1'].hide()
        try:
            if self._creating_new_database:
                pass
        except: 
            self.gobject['main_window'].show()

    def create_database(self):
        from LibScan.mysql_ampache import database_tables, database_creator, catalog_creator, catalog_local_creator
        self.db.autocommit(True)
        cursor = self.db.cursor()
        print "Creating the database"
        cursor.execute(database_creator % self.database)
        cursor.execute("USE `{}`".format(self.database))
        print "Creating the tables"
        for table, creator in database_tables.iteritems():
            print "Creating table {}".format(table)
            cursor.execute(creator)
        print "Tables created"
        print "Creating catalog entry"
        now = int(time())
        cursor.execute(catalog_creator, (self.catalog_name, now, now, now))
        new_cat_id = cursor.lastrowid
        print "Created catalog entry, creating local entry"
        cursor.execute(catalog_local_creator, (self.catalog_dir, new_cat_id))
        print "Created local entry"
        print "Reconnecting to the new database"
        self.db_connect()


    def firstrun_finished(self):
        print "Firstrun done"
        self.gobject['setupdialog'].hide()
        self.gobject['firstrun_assistant'].hide()
        self.gobject['main_window'].show_all()
        return False

    def catEdited(self, *args):
        print "Cat edited: ", args

    def dirEdited(self, *args):
        print "Dir Edited: ", args

    def dirClicked(self, *args):
        print "Dir column clicked: ", args

    def getSelectedFolder(self, *args):
        print "Selected: ", self.gobject['filechooserdialog1'].get_filename()
        self.catTree.set_value(self.current_iter, 1, self.gobject['filechooserdialog1'].get_filename())
        self.gobject['filechooserdialog1'].hide()

    def closeFileChooser(self, *args):
        self.gobject['filechooserdialog1'].hide()
        return True

    def btnPressEvent(self, *args):
        treepath, treeviewcolumn, x, y = args[0].get_path_at_pos(args[1].x, args[1].y)
        if treeviewcolumn.get_title() != 'Add\nDirectory' and treeviewcolumn.get_title() != 'Remove\nDirectory':
            return
        self.current_iter = self.catTree.get_iter(treepath)
        value = self.catTree.get_value(self.current_iter, 1)
        if value is None:
            return
        if value == ADD_DIR_STRING:
            path = value = os.path.expanduser('~')
            self.gobject['filechooserdialog1'].set_current_folder(path)
        else:
            path, folder = os.path.split(value)
            self.gobject['filechooserdialog1'].set_current_folder(path)
            self.gobject['filechooserdialog1'].select_filename(value)
        self.gobject['filechooserdialog1'].show_all()

    def on_button_full_scan_library_clicked(self, *args):
        print "Running full scan"
        self.full_scan = True
        self.on_button_scan_library_clicked(*args)

    def on_button_scan_library_clicked(self, *args):
        if not self.db:
            self.gobject['database_message_dialog'].show()
            print "Database not connected"
            return

        if self.scan_running:
            print "Stop Scan"
            self.scan_running = False
        else:
            if self.estimated_total_files > 0:
                print "Estimate already run, scanning files now"
                self.scan_running = True
                task = self.scan_files(estimate=False)
                GObject.idle_add(task.next)
                return True
            self.scan_running = True
            self.estimate_completed = False
            self._pulse_timeout_id = GObject.timeout_add(600, self._on_pulse_timeout, None)
            task = self.scan_files(estimate=True)
            GObject.idle_add(task.next)
            self.gobject['pgrScan'].set_text('Estimating Files')
            print "Estimate Started"

    def on_button_exit_clicked(self, *args):
        Gtk.main_quit(*args)

    def on_main_window_destroy(self, *args):
        print "Window Destroyed"
        self.on_button_exit_clicked(args)

    def on_menu_file_quit_activate(self, *args):
        self.on_button_exit_clicked(args)

    def on_button_preferences_close(self, *args):
        """ Reset preferences """
        print "Close Prefs"
        self.gobject['preferences_dialog'].hide()
        self.gobject['database_server_entry'].set_text(self.options['db']['server']) 
        self.gobject['database_name_entry'].set_text(self.options['db']['database']) 
        self.gobject['database_user_entry'].set_text(self.options['db']['user']) 
        self.gobject['database_password_entry'].set_text(self.options['db']['password'])

    def on_main_window_menu_help_submenu_about_activate(self, *args):
        self.gobject['about_dialog'].run()
        self.gobject['about_dialog'].hide()

    def on_menu_edit_properties_selected(self, *args):
        self.gobject['preferences_dialog'].show_all()

    def on_preferences_dialog_show(self, *args):
        self._build_catalog_tree()
        self.gobject['database_server_entry'].set_text(self.options['db']['server'])
        self.gobject['database_name_entry'].set_text(self.options['db']['database'])
        self.gobject['database_user_entry'].set_text(self.options['db']['user'])
        self.gobject['database_password_entry'].set_text(self.options['db']['password'])
        self.gobject['prefix_entry'].set_text(", ".join(self.options['program']['prefixes']))
        self.gobject['no_tracknumber_checkbutton'].set_active(self.options['program']['tracknumber_warning'])
        self.gobject['fix_spaces_checkbutton'].set_active(self.options['program']['fix_spaces'])
        self.gobject['dash_checkbutton'].set_active(self.options['program']['dash_warning'])
        self.gobject['valid_filetypes_textbuffer'].set_text(", ".join(self._valid_filetypes))
    
    def on_preferences_dialog_delete_event(self, *args):
        self.gobject['preferences_dialog'].hide()
        return True

    def on_new_catalog_button_clicked(self, *args):
        self.gobject['new_catalog_dialog'].show()

    def on_new_catalog_dialog_ok_button_clicked(self, *args):
        from LibScan.mysql_ampache import catalog_creator, catalog_local_creator
        print "OK Clicked"
        name = self.gobject['new_catalog_name_entry'].get_text()
        dir = self.gobject['new_catalog_filechooser_button'].get_filename()
        if name == '' or dir is None:
            print "Blank dir or name"
            self.gobject['new_catalog_dialog'].hide()
            return
        exists = False
        # Prevent creating identical catalog names
        # For now, also prevent more than one catalog per directory.
        #  This may change in the future, as it could be usefull
        for store in self.gobject['cattreestore']:
            dirname, id, new_name = store[1:4]
            if dir == dirname or name == new_name:
                print "Not creating catalog, already exists"
                exists = True
        if not exists:
            print "Creating catalog entry"
            now = int(time())
            self.cursor.execute(catalog_creator, (name, now, now, now))
            new_cat_id = self.cursor.lastrowid
            print "Created catalog entry, creating local entry"
            self.cursor.execute(catalog_local_creator, (dir, new_cat_id))
            print "Created local entry"
            self._build_catalog_tree()
        self.gobject['new_catalog_dialog'].hide()

    def on_new_catalog_cancel_button_clicked(self, *args):
        self.gobject['new_catalog_dialog'].hide()

    def on_new_catalog_dialog_delete_event(self, *args):
        self.gobject['new_catalog_dialog'].hide()
        return True

    def on_preferences_ok_button_clicked(self, *args):
        """ TODO: Check if there are actually changes to the DB info before trying to reconnect """
        self.gobject['preferences_dialog'].hide()
        self.options['db']['server'] = self.gobject['database_server_entry'].get_text()
        self.options['db']['database'] = self.gobject['database_name_entry'].get_text()
        self.options['db']['user'] = self.gobject['database_user_entry'].get_text()
        self.options['db']['password'] = self.gobject['database_password_entry'].get_text()
        new_prefixes = [x.lower().strip() for x in self.gobject['prefix_entry'].get_text().split(",") if x.strip() != '']
        self.saved_prefixes = set(self.options['program']['prefixes'])
        self.new_prefixes = set(new_prefixes)
        self.deleted = self.saved_prefixes - self.new_prefixes
        self.added = self.new_prefixes - self.saved_prefixes
        if len(self.added) > 0 or len(self.deleted) > 0:
            self.gobject['deleted_prefixes_label'].set_text(", ".join(self.deleted))
            self.gobject['added_prefixes_label'].set_text(", ".join(self.added))
            self.gobject['prefix_change_messagedialog'].show()
        if 'program' not in self.options:
            self.options['program'] = {}
        self._prefixes = new_prefixes
        self.options['program']['prefixes'] = self._prefixes
        self.options['program']['tracknumber_warning'] = self.gobject['no_tracknumber_checkbutton'].get_active()
        self.options['program']['fix_spaces'] = self.gobject['fix_spaces_checkbutton'].get_active()
        self.options['program']['dash_warning'] = self.gobject['dash_checkbutton'].get_active()
        self.gobject['main_window'].set_title('DJDB: {}@{}'.format(self.options['db']['database'], self.options['db']['server']))
        cPickle.dump(self.options, open(self.configfile, "wb"))
        self.gobject['preferences_dialog'].hide()
        try:
            self.db.close()
        except:
            pass
        self.cursor = None
        self.db_connect()
        for store in self.gobject['cattreestore']:
            id, new_name, tip, old_name = store[2:]
            if new_name != old_name:
                self.cursor.execute(Queries.update_catalog_name, (new_name, id))

    def on_preferences_dialog_catalog_entry_edited(self, *args):
        store_id, new_name = args[1:]
        self.gobject['cattreestore'][int(store_id),0][3] = new_name

    def on_warningmenuitem_activate(self, *args):
        self.gobject['warningwindow'].show()

    def on_warningwindow_delete_event(self, *args):
        self.gobject['warningwindow'].hide()
        return True

    def on_database_message_dialog_response(self, *args):
        print "Response: ", args
        self.gobject['database_message_dialog'].hide()

    def on_database_message_dialog_delete_event(self, *args):
        self.gobject['database_message_dialog'].hide()
        return True

    def on_new_database_radiobutton_toggled(self, *args):
        if args[0].get_active():
            self.gobject['create_catalog_box'].show()
        else:
            self.gobject['create_catalog_box'].hide()

    def on_db_error_messagedialog_delete_event(self, *args):
        self.gobject['db_error_messagedialog'].hide()
        return True

    def on_db_error_messagedialog_response(self, *args):
        self.gobject['db_error_messagedialog'].hide()

    def on_prefix_change_messagedialog_response(self, *args):
        if args[1] == -8:
            task = self.update_prefixes()
            GObject.idle_add(task.next)
        else:
            self.gobject['prefix_change_messagedialog'].hide()
    def on_prefix_change_messagedialog_delete_event(self, *args):
        self.gobject['prefix_change_messagedialog'].hide()
        return True

    def on_new_database_menuitem_activate(self, *args):
        self._create_new_database = True
        self.gobject['assistant1'].show()

    def on_changedmenuitem_activate(self, *args):
        self.gobject['changedwindow'].show()

    def on_changedwindow_delete_event(self, *args):
        self.gobject['changedwindow'].hide()
        return True

    def on_new_window_delete_event(self, *args):
        self.gobject['new_window'].hide()
        return True

    def on_new_tracks_menuitem_activate(self, *args):
        self.gobject['new_window'].show()
    