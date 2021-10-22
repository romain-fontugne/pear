import appdirs
from datetime import timedelta
import os
import requests_cache

import sqlite3

CACHE_DIR = appdirs.user_cache_dir('pear', 'IHR')+"/ripe/"
URL = 'http://ftp.ripe.net/ripe/asnames/asn.txt'
CACHE_EXPIRATION = 1 # days

class ASName(object):
    def __init__(self, cache_db=None, cache_directory=CACHE_DIR, 
            cache_expiration=CACHE_EXPIRATION):
        
        self.names = {}

        self.cache_directory = cache_directory
        os.makedirs(self.cache_directory, exist_ok=True)
        
        if cache_db is None:
            self.cache_db = cache_directory+'pear.sql'
        else:
            self.cache_db = cache_db

        self.con = sqlite3.connect(self.cache_db)
        self.cur = self.con.cursor()
        try:
            # Create table
            self.cur.execute('''CREATE TABLE as_name 
                    (asn text, name text, country text)''')

            with requests_cache.CachedSession(self.cache_directory,
                    backend='filesystem',
                    expire_after=timedelta(days=cache_expiration)) as session:

                page = session.get(URL)

                for line in page.iter_lines(decode_unicode=True):
                    asn, _, name_cc = line.partition(' ')
                    name, _, cc = name_cc.rpartition(',')

                    self.cur.execute(
                            "INSERT INTO as_name VALUES (?,?,?)", 
                            (asn.strip(), name.strip(), cc.strip())
                            )

        except sqlite3.OperationalError:
            # The table already exists
            print('Using cached traceroutes')

        self.con.commit()
        self.con.close()

        # Keep a cursor open for reads
        self.con = sqlite3.connect(self.cache_db, check_same_thread=False)
        self.cur = self.con.cursor()

    def name(self, asn):
        """Return the name corresponding to the given ASN"""

        if asn is None:
            return ''

        # we need only the AS number
        if asn.startswith('AS'):
            asn = asn[2:]

        # remove curly brackets to sets with only one ASN
        if asn.startswith('{') and asn.endswith('}') and ',' not in asn:
            asn = asn[1:-1]

        if asn not in self.names:
            # get name from database
            self.cur.execute("select name from as_name where asn=? ", (asn,))
            res = self.cur.fetchall()
            name = ''
            if len(res) > 0:
                name = res[0][0]

            # cache results for next calls
            self.names[asn] = name
            
        return self.names[asn]

