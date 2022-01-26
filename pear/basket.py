import arrow
from glob import glob
from pear.pear import Pear
import os

class Basket():
    """Manage a set of pear instances. Keep in memory only the latest pears that
    are accessed."""

    def __init__(self, db_folder, max_pears=20):
        # Initialize 

        self.db_folder = db_folder
        self.max_pears = max_pears
        self.basket = {}

    def get(self, session, request={}):
        
        if( 'db-file' in request.args 
                and request.args.get('db-folder')+'/'+request.args.get('db-file') 
                in self.list()):
            pear = self.load(request.args.get('db-folder')+'/'+request.args.get('db-file'))
        elif 'pear' in session:
            pear = self.load(session['pear'])
        else:
            latest_db = self.latest()
            pear = self.load(latest_db)
        
        session['pear'] = pear['fname'] 

        return pear['pear'], pear['plotter']

    def load(self, db_fname):
        """Returns the pear and plotter instances corresponding to given database.
        db_fname should be relative to this basket db_folder."""

        print('LOADING: ', db_fname)
        if db_fname in self.basket:
            self.basket[db_fname]['last_get'] = arrow.now()

        else:
            pear = Pear(sqlite_fname=self.db_folder+db_fname)
            # Load all data (traffic and routing)
            pear.load()
            # Prepare AS graphs
            plotter = pear.make_graphs()

            self.basket[db_fname] = {
                'fname': db_fname,
                'pear': pear,
                'plotter': plotter,
                'last_get': arrow.now().timestamp()
                }

            self.gc()

        return self.basket[db_fname]

    def gc(self):
        """Garbage Collector: Remove old pears if the maximum number of pears 
        is exceeded."""

        while len(self.basket) > self.max_pears:
            oldest = min(self.basket, key=lambda x: self.basket[x]['last_get'])
            del self.basket[oldest]

    def list(self):
        """List databases found in the given folder and its subfolders.

        The returned file names are relative to the basket db_folder."""

        dbs = glob(self.db_folder+'/**/*.sql', recursive=True)

        for db in dbs:
            # Make sure we have the config file with the database (JSON)
            # TODO uncomment this when json are implemented
            # if os.path.exists(db+'.json'):
               yield db.replace(self.db_folder, '')

    def latest(self):
        """Returns path to the newest database."""

        latest_timestamp = 0 
        latest_db = '' 

        for db in self.list():
            modification_time = os.path.getmtime(self.db_folder+db)
            if latest_timestamp < modification_time:
                latest_timestamp = modification_time 
                latest_db = db

        return latest_db
