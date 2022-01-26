import appdirs
from collections import defaultdict
import glob
from iso3166 import countries
import json
import os
import sqlite3
import sys

from .as_graph import ASGraph
from .as_name import ASName
from .atlas_traceroute import AtlasTraceroute
from .bgp_table import BGPTable
from .sankey_plotter import SankeyPlotter
from .prefix_weights import PrefixWeights

CACHE_DIR = appdirs.user_cache_dir('pear', 'IHR')

def guess_config(sqlite_fname):
    """Guess configuration (temporary fix for compatibility with old versions)"""

    cities = {
            'us': ['nyc', 'sea', 'lax', 'sjc', 'abn'],
            'asia': ['sgp', 'hkg'],
            'eu': ['ldn'],
            'jp': ['tky', 'osk']
            }
    
    region = sqlite_fname.rpartition('/')[2].partition('_')[0]
    working_directory = sqlite_fname.rpartition('/')[0]+'/'
    prefix_fnames = [fname for fname in glob.glob(working_directory+'/mean_tput/*.csv')
        if fname.rpartition('/')[2].partition('0')[0] in cities[region]]

    # guess MRT file names from sqlite tables name
    con = sqlite3.connect(sqlite_fname)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    bgp_fnames = ['./'+table[0].partition('bgp_')[2] for table in tables if table[0].startswith('bgp_bview')]
    con.close()
    

    return {
            'asn': 2497,
            'weight_name': 'avg_bps',
            'prefix_fnames': prefix_fnames,
            'bgp_fnames': bgp_fnames,
            'atlas_msm_ids': [],
            }


class Pear():
    def __init__(self, sqlite_fname, ASN=None, weight_name=None, 
            atlas_msm_ids=[], prefix_fnames=[], bgp_fnames=[]):
        """Initiate pear instance either with raw data (all arguments required)
        or with a pre-computed database (only sqlite_fname is required)."""

        config = {
            'asn': ASN,
            'weight_name': weight_name,
            'prefix_fnames': prefix_fnames,
            'bgp_fnames': bgp_fnames,
            'atlas_msm_ids': atlas_msm_ids,
        }

        if ASN is None or weight_name is None or len(prefix_fnames)==0 or len(bgp_fnames)==0:
            # Load config from file if config is empty
            if os.path.exists(sqlite_fname+'.json'):
                with open(sqlite_fname+'.json', 'r') as fp:
                    config = json.load(fp)
            else:
                # temporary fix for compatibility with old versions
                config = guess_config(sqlite_fname)
                with open(sqlite_fname+'.json', 'w') as fp:
                    json.dump(config, fp)
        else:
            with open(sqlite_fname+'.json', 'w') as fp:
                json.dump(config, fp)

        print('config: ', config)
        self.ASN = config['asn']
        self.weight_name = config['weight_name']
        self.prefix_fnames = config['prefix_fnames']
        self.bgp_fnames = config['bgp_fnames']
        self.atlas_msm_ids = config['atlas_msm_ids']

        self.sqlite_db = sqlite_fname
        self.first_router = None
        self.ribs = {}
        self.flows = {}
        self.all_peers = set()
        print('Loading AS names')
        self.as_name = ASName(self.sqlite_db)

    def load(self):

        router2mrt = {}
        loaded_mrt = defaultdict(lambda:
                    {
                        'rib': None,
                        'processed_routers': set(),
                        'all_routers': set(),
                        'prefixes': []
                    }
                )

        # Match router names and MRT file names
        for prefix_fname in self.prefix_fnames:
            router_name = prefix_fname.rpartition('/')[2].rpartition('.')[0] 

            mrt_fname = self.bgp_fnames[0]
            if len(self.bgp_fnames) > 1:
                mrt_fname = [fname for fname in self.bgp_fnames if router_name in fname][0]
            router2mrt[router_name] = mrt_fname
            loaded_mrt[mrt_fname]['all_routers'].add(router_name)

        # Load traffic and BGP data
        for prefix_fname in self.prefix_fnames:
            router_name = prefix_fname.rpartition('/')[2].rpartition('.')[0] 
            if self.first_router is None:
                self.first_router = router_name

            # load prefix file and weights
            weights = PrefixWeights(prefix_fname, self.weight_name)
            self.flows[router_name] = weights

            # load routing data
            mrt_fname = router2mrt[router_name] 
            if loaded_mrt[mrt_fname]['rib'] is None:
                rib = BGPTable( self.ASN, cache_db=self.sqlite_db)
                sys.stderr.write(f'Reading BGP data for {router_name}\n')
                rib.load_bgp(mrt_fname)
                loaded_mrt[mrt_fname]['rib'] = rib

            rib = loaded_mrt[mrt_fname]['rib']
            self.ribs[router_name] = rib

            # Load things that need a full RIB
            self.traceroutes = AtlasTraceroute(self.ASN, rib, 
                    measurement_ids=self.atlas_msm_ids, cache_db=self.sqlite_db)

            
            loaded_mrt[mrt_fname]['prefixes'].extend(weights.prefixes())
            prefixes = loaded_mrt[mrt_fname]['prefixes']
            loaded_mrt[mrt_fname]['processed_routers'].add(router_name)

            # Clean RIB and cache if we are done with this RIB
            if not rib.iscached and ( 
                    len(loaded_mrt[mrt_fname]['processed_routers']) ==
                    len(loaded_mrt[mrt_fname]['all_routers'])
                    ):
                prefixes = loaded_mrt[mrt_fname]['prefixes']
                # Add selected prefixes if not globally rechable
                sys.stderr.write('Adding selected prefixes\n')
                rib.add_prefixes(prefixes)
                sys.stderr.write('Cleaning table\n')
                rib.clean_table(prefixes)
                sys.stderr.write('Adding prefixes info\n')
                rib.add_prefix_info(prefixes)

                rib.cache_rib()

            self.all_peers.update(rib.list_peers())



    def make_graphs(self):
        sp = SankeyPlotter(self.ASN, self.as_name)
        for router_name, rib in self.ribs.items():
            weights = self.flows[router_name]
            # Create AS graph
            sys.stderr.write('Building AS graph\n')
            graph = ASGraph(self.ASN, rib)
            graph.build_graph(weights.prefixes())

            sys.stderr.write('Computing weights\n')
            # compute edges/nodes weights
            graph.propagate_prefix_weight(weights.dataset, hop_power=0)
            #graph.top_nodes(10, weights, rib)

            sp.add_graph(graph, rib, aliases={self.ASN: router_name})

        # Prepare AS graph plot
    # plot_fname = self.graph_filename.format(
    #     ASN=args.ASN, prefixes=args.prefixes, weight_name=args.weight_name)
    # sp.plot(plot_fname)

        return sp

    def get_rib(self, router_name):

        if router_name is None or router_name not in self.ribs:
            router_name = self.first_router

        rib = self.ribs[router_name].list_prefixes()

        return router_name, rib

    def get_traffic(self, router_names, asn=None, country=None):

        traffic = {}

        for router_name in router_names:
            if router_name is None or router_name not in self.ribs:
                router_name = self.first_router

            if router_name in self.ribs:
                rib = self.ribs[router_name]

                if router_name not in traffic:
                    traffic[router_name] = {}

                for prefix, vol in self.flows[router_name].raw_weights().items():
                    info = rib.prefix_info(prefix)

                    print(prefix, info)

                    # Add country and AS names
                    info['country_name'] = ''
                    if 'country' in info and info['country'] is not None and info['country'] != 'ZZ':
                        info['country_name'] = countries.get(info['country']).name
                    info['originasn_name'] = self.as_name.name(info['originasn'])

                    if( (asn is None or asn in info['aspath']) 
                            and ( country is None or country == info['country']) ):

                        traffic[router_name][prefix] = {
                                'vol': vol, 
                                'info': info
                                }

        return traffic

    def get_all_peers(self):

        peers = {}
        for asn in self.all_peers:
            peers[asn] = {
                    'name': 'UNK',
                    'vol': 0
                    }

        return peers

    def get_router_names(self):
        return list(self.ribs.keys())

    def get_country_rtt(self, cc, asn=None):
        return self.traceroutes.country_stats(cc, asn)

    def get_countries(self, data_type='all'):
        ccs = set()
        if data_type in ['all', 'traceroute']: 
            ccs.update( self.traceroutes.country_code() )

        if data_type in ['all', 'traffic']: 
            for rib in self.ribs.values():
                ccs.update( rib.country_codes() )

        if None in ccs:
            ccs.remove(None)

        if 'ZZ' in ccs:
            ccs.remove('ZZ')

        return {cc: countries.get(cc).name for cc in sorted(ccs)}

