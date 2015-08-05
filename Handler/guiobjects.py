from Database.Ampache import Queries

def _on_pulse_timeout(self, *args):
    if self.estimate_completed:
        self.gobject['pgrScan'].set_fraction(0.0)
        self.gobject['pgrScan'].set_text('Idle')
        return False
    self.gobject['pgrScan'].pulse()
    return True

def _build_catalog_tree(self):
    if self.cursor is not None:
        self.gobject['catliststore'].clear()
        self.gobject['cattreestore'].clear()
        self.cursor.execute(Queries.get_catalogs)
        for r in self.cursor.fetchall():
            self.gobject['cattreestore'].append((0, r['path'], r['cid'], r['name'],
                                                 "Double Click on the Catalog Name to change",
                                                 r['name']))
            self.gobject['catliststore'].append((r['cid'], r['name']))
