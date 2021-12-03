import argparse
import os
import json
from iso3166 import countries

from flask import Flask, render_template
from flask import request
from flask_basicauth import BasicAuth

from pear.pear import Pear

parser = argparse.ArgumentParser()
parser.add_argument('ASN', type=int,
                    help='ASN of the network manageed by the user')
#parser.add_argument('-c', '--route_collector', type=str, default='rrc06',
        #help="BGP route collector that peers with given ASN"),
parser.add_argument('-b', '--bgp_data', type=str, nargs='+', 
        help="MRT files containing a RIB for monitored prefixes"),
parser.add_argument('-p', '--prefixes', type=str, nargs='+', 
        help="CSV files with a list of selected prefixes and optional traffic volume"),
parser.add_argument('-w', '--weight_name', type=str, default='avg_bps',
        help="Name of the column in the csv file used for prefix weights"),
parser.add_argument('--atlas_msm', default=[], nargs='+',
        help="Atlas traceroute measurement IDs to use of RTT results"),
parser.add_argument('-d','--db', default=None, 
        help="SQLite database to cache computed data"),
parser.add_argument('--serverless', action='store_true',
        help="Compute database if needed, don't start the web server."),
args = parser.parse_args()

# Initiate Flask app
app = Flask(__name__)

# set basic authentication if there is a auth.json file
if os.path.exists('auth.json'):
    auth = json.load(open('auth.json'))
    app.config['BASIC_AUTH_USERNAME'] = auth['username']
    app.config['BASIC_AUTH_PASSWORD'] = auth['password']
    app.config['BASIC_AUTH_FORCE'] = True
    basic_auth = BasicAuth(app)

# Main app
pear = Pear(args.ASN, args.weight_name, atlas_msm_ids=args.atlas_msm, 
        cache_db=args.db)
# Load all data (traffic and routing)
pear.load(args.prefixes, args.bgp_data)
# Prepare AS graphs
plotter = pear.make_graphs()

def search(keyword):
    try:
        if keyword.startswith('AS') and int(keyword[2:]):
            return as_details( keyword[2:] )
        if int(keyword):
            return as_details( keyword )
    except:
        pass

    try:
       return country( countries.get(keyword).alpha2 )
    except:
        pass
        
    return index(no_search=True)


# Views
@app.route('/')
def index(no_search=False):

    if 'search' in request.args and not no_search:
        return search(request.args.get('search'))

    min_traffic = request.args.get('min_traffic', plotter.minimum_traffic)
    max_traffic = 1000000000
    plotter.plot( int(min_traffic) )
    return render_template('index.html', asgraph=plotter.to_json(),
            min_traffic=min_traffic,
            max_traffic=max_traffic
            )

@app.route('/routing')
def routing():

    if 'search' in request.args:
        return search(request.args.get('search'))

    rib=[]
    router_name = request.args.get('router', None)
    selected_router, rib = pear.get_rib(router_name)

    return render_template('routing-table.html', 
            rib=rib, 
            router_names=pear.get_router_names(),
            selected_router=selected_router
            )

@app.route('/traffic')
def traffic():

    if 'search' in request.args:
        return search(request.args.get('search'))

    all_routers = pear.get_router_names() 
    selected_router = request.args.get('router')
    router_names = []
    if selected_router is None or selected_router == 'All':
        selected_router = 'All'
        router_names = all_routers
    else:
        router_names = [selected_router]

    traffic = pear.get_traffic(router_names)

    return render_template('traffic-table.html', 
            flows=traffic,
            router_names=all_routers,
            selected_router=selected_router
            ) 

@app.route('/peers')
def peers():

    if 'search' in request.args:
        return search(request.args.get('search'))


    peers = pear.get_all_peers()
    return render_template('peers-table.html', peers=peers) 

@app.route('/as_details')
def as_details(asn=None):

    if asn is None:
        if 'search' in request.args:
            return search(request.args.get('search'))

        asn = request.args.get('asn', None)

    all_routers = pear.get_router_names() 

    traffic = pear.get_traffic(all_routers, asn=asn)
    selected_country = request.args.get('country', None)
    country_rtt = pear.get_country_rtt(selected_country, asn)
    
    routers_list = ['All']
    routers_list.extend(all_routers)

    return render_template('as.html', 
            flows=traffic,
            asn=asn,
            as_name=pear.as_name.name(asn),
            traceroutes=country_rtt, 
            all_country_code=pear.get_countries(),
            selected_country=selected_country
            ) 

@app.route('/country')
def country(cc=None):

    if cc is None:
        if 'search' in request.args:
            return search(request.args.get('search'))

        cc = request.args.get('cc', None)

    country_name = ''
    if cc is not None:
        country_name = countries.get(cc).name

    all_routers = pear.get_router_names() 

    traffic = pear.get_traffic(all_routers, country=cc)
    country_rtt = pear.get_country_rtt(cc)
    
    return render_template('country.html', 
            flows=traffic,
            cc=cc,
            country_name=country_name,
            traceroutes=country_rtt, 
            all_country_code=pear.get_countries()
            ) 


@app.route('/rtt')
def rtt():

    if 'search' in request.args:
        return search(request.args.get('search'))


    selected_country = request.args.get('country')
    country_rtt = pear.get_country_rtt(selected_country)
    if(selected_country is None):
        selected_country = 'All'
    return render_template('rtt-table.html', 
            traceroutes=country_rtt, 
            all_country_code=pear.get_countries('traceroute'),
            selected_country=selected_country
            ) 


if not args.serverless:
    app.run(debug=True)
