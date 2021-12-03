var isoCountries = {
    'AF' : 'Afghanistan',
    'AX' : 'Aland Islands',
    'AL' : 'Albania',
    'DZ' : 'Algeria',
    'AS' : 'American Samoa',
    'AD' : 'Andorra',
    'AO' : 'Angola',
    'AI' : 'Anguilla',
    'AQ' : 'Antarctica',
    'AG' : 'Antigua And Barbuda',
    'AR' : 'Argentina',
    'AM' : 'Armenia',
    'AW' : 'Aruba',
    'AU' : 'Australia',
    'AT' : 'Austria',
    'AZ' : 'Azerbaijan',
    'BS' : 'Bahamas',
    'BH' : 'Bahrain',
    'BD' : 'Bangladesh',
    'BB' : 'Barbados',
    'BY' : 'Belarus',
    'BE' : 'Belgium',
    'BZ' : 'Belize',
    'BJ' : 'Benin',
    'BM' : 'Bermuda',
    'BT' : 'Bhutan',
    'BO' : 'Bolivia',
    'BA' : 'Bosnia And Herzegovina',
    'BW' : 'Botswana',
    'BV' : 'Bouvet Island',
    'BR' : 'Brazil',
    'IO' : 'British Indian Ocean Territory',
    'BN' : 'Brunei Darussalam',
    'BG' : 'Bulgaria',
    'BF' : 'Burkina Faso',
    'BI' : 'Burundi',
    'KH' : 'Cambodia',
    'CM' : 'Cameroon',
    'CA' : 'Canada',
    'CV' : 'Cape Verde',
    'KY' : 'Cayman Islands',
    'CF' : 'Central African Republic',
    'TD' : 'Chad',
    'CL' : 'Chile',
    'CN' : 'China',
    'CX' : 'Christmas Island',
    'CC' : 'Cocos (Keeling) Islands',
    'CO' : 'Colombia',
    'KM' : 'Comoros',
    'CG' : 'Congo',
    'CD' : 'Congo, Democratic Republic',
    'CK' : 'Cook Islands',
    'CR' : 'Costa Rica',
    'CI' : 'Cote D\'Ivoire',
    'HR' : 'Croatia',
    'CU' : 'Cuba',
    'CY' : 'Cyprus',
    'CZ' : 'Czech Republic',
    'DK' : 'Denmark',
    'DJ' : 'Djibouti',
    'DM' : 'Dominica',
    'DO' : 'Dominican Republic',
    'EC' : 'Ecuador',
    'EG' : 'Egypt',
    'SV' : 'El Salvador',
    'GQ' : 'Equatorial Guinea',
    'ER' : 'Eritrea',
    'EE' : 'Estonia',
    'ET' : 'Ethiopia',
    'FK' : 'Falkland Islands (Malvinas)',
    'FO' : 'Faroe Islands',
    'FJ' : 'Fiji',
    'FI' : 'Finland',
    'FR' : 'France',
    'GF' : 'French Guiana',
    'PF' : 'French Polynesia',
    'TF' : 'French Southern Territories',
    'GA' : 'Gabon',
    'GM' : 'Gambia',
    'GE' : 'Georgia',
    'DE' : 'Germany',
    'GH' : 'Ghana',
    'GI' : 'Gibraltar',
    'GR' : 'Greece',
    'GL' : 'Greenland',
    'GD' : 'Grenada',
    'GP' : 'Guadeloupe',
    'GU' : 'Guam',
    'GT' : 'Guatemala',
    'GG' : 'Guernsey',
    'GN' : 'Guinea',
    'GW' : 'Guinea-Bissau',
    'GY' : 'Guyana',
    'HT' : 'Haiti',
    'HM' : 'Heard Island & Mcdonald Islands',
    'VA' : 'Holy See (Vatican City State)',
    'HN' : 'Honduras',
    'HK' : 'Hong Kong',
    'HU' : 'Hungary',
    'IS' : 'Iceland',
    'IN' : 'India',
    'ID' : 'Indonesia',
    'IR' : 'Iran, Islamic Republic Of',
    'IQ' : 'Iraq',
    'IE' : 'Ireland',
    'IM' : 'Isle Of Man',
    'IL' : 'Israel',
    'IT' : 'Italy',
    'JM' : 'Jamaica',
    'JP' : 'Japan',
    'JE' : 'Jersey',
    'JO' : 'Jordan',
    'KZ' : 'Kazakhstan',
    'KE' : 'Kenya',
    'KI' : 'Kiribati',
    'KR' : 'Korea',
    'KW' : 'Kuwait',
    'KG' : 'Kyrgyzstan',
    'LA' : 'Lao People\'s Democratic Republic',
    'LV' : 'Latvia',
    'LB' : 'Lebanon',
    'LS' : 'Lesotho',
    'LR' : 'Liberia',
    'LY' : 'Libyan Arab Jamahiriya',
    'LI' : 'Liechtenstein',
    'LT' : 'Lithuania',
    'LU' : 'Luxembourg',
    'MO' : 'Macao',
    'MK' : 'Macedonia',
    'MG' : 'Madagascar',
    'MW' : 'Malawi',
    'MY' : 'Malaysia',
    'MV' : 'Maldives',
    'ML' : 'Mali',
    'MT' : 'Malta',
    'MH' : 'Marshall Islands',
    'MQ' : 'Martinique',
    'MR' : 'Mauritania',
    'MU' : 'Mauritius',
    'YT' : 'Mayotte',
    'MX' : 'Mexico',
    'FM' : 'Micronesia, Federated States Of',
    'MD' : 'Moldova',
    'MC' : 'Monaco',
    'MN' : 'Mongolia',
    'ME' : 'Montenegro',
    'MS' : 'Montserrat',
    'MA' : 'Morocco',
    'MZ' : 'Mozambique',
    'MM' : 'Myanmar',
    'NA' : 'Namibia',
    'NR' : 'Nauru',
    'NP' : 'Nepal',
    'NL' : 'Netherlands',
    'AN' : 'Netherlands Antilles',
    'NC' : 'New Caledonia',
    'NZ' : 'New Zealand',
    'NI' : 'Nicaragua',
    'NE' : 'Niger',
    'NG' : 'Nigeria',
    'NU' : 'Niue',
    'NF' : 'Norfolk Island',
    'MP' : 'Northern Mariana Islands',
    'NO' : 'Norway',
    'OM' : 'Oman',
    'PK' : 'Pakistan',
    'PW' : 'Palau',
    'PS' : 'Palestinian Territory, Occupied',
    'PA' : 'Panama',
    'PG' : 'Papua New Guinea',
    'PY' : 'Paraguay',
    'PE' : 'Peru',
    'PH' : 'Philippines',
    'PN' : 'Pitcairn',
    'PL' : 'Poland',
    'PT' : 'Portugal',
    'PR' : 'Puerto Rico',
    'QA' : 'Qatar',
    'RE' : 'Reunion',
    'RO' : 'Romania',
    'RU' : 'Russian Federation',
    'RW' : 'Rwanda',
    'BL' : 'Saint Barthelemy',
    'SH' : 'Saint Helena',
    'KN' : 'Saint Kitts And Nevis',
    'LC' : 'Saint Lucia',
    'MF' : 'Saint Martin',
    'PM' : 'Saint Pierre And Miquelon',
    'VC' : 'Saint Vincent And Grenadines',
    'WS' : 'Samoa',
    'SM' : 'San Marino',
    'ST' : 'Sao Tome And Principe',
    'SA' : 'Saudi Arabia',
    'SN' : 'Senegal',
    'RS' : 'Serbia',
    'SC' : 'Seychelles',
    'SL' : 'Sierra Leone',
    'SG' : 'Singapore',
    'SK' : 'Slovakia',
    'SI' : 'Slovenia',
    'SB' : 'Solomon Islands',
    'SO' : 'Somalia',
    'ZA' : 'South Africa',
    'GS' : 'South Georgia And Sandwich Isl.',
    'ES' : 'Spain',
    'LK' : 'Sri Lanka',
    'SD' : 'Sudan',
    'SR' : 'Suriname',
    'SJ' : 'Svalbard And Jan Mayen',
    'SZ' : 'Swaziland',
    'SE' : 'Sweden',
    'CH' : 'Switzerland',
    'SY' : 'Syrian Arab Republic',
    'TW' : 'Taiwan',
    'TJ' : 'Tajikistan',
    'TZ' : 'Tanzania',
    'TH' : 'Thailand',
    'TL' : 'Timor-Leste',
    'TG' : 'Togo',
    'TK' : 'Tokelau',
    'TO' : 'Tonga',
    'TT' : 'Trinidad And Tobago',
    'TN' : 'Tunisia',
    'TR' : 'Turkey',
    'TM' : 'Turkmenistan',
    'TC' : 'Turks And Caicos Islands',
    'TV' : 'Tuvalu',
    'UG' : 'Uganda',
    'UA' : 'Ukraine',
    'AE' : 'United Arab Emirates',
    'GB' : 'United Kingdom',
    'US' : 'United States',
    'UM' : 'United States Outlying Islands',
    'UY' : 'Uruguay',
    'UZ' : 'Uzbekistan',
    'VU' : 'Vanuatu',
    'VE' : 'Venezuela',
    'VN' : 'Viet Nam',
    'VG' : 'Virgin Islands, British',
    'VI' : 'Virgin Islands, U.S.',
    'WF' : 'Wallis And Futuna',
    'EH' : 'Western Sahara',
    'YE' : 'Yemen',
    'ZM' : 'Zambia',
    'ZW' : 'Zimbabwe'
};

function getCountryName (countryCode) {
    if (isoCountries.hasOwnProperty(countryCode)) {
        return isoCountries[countryCode];
    } else {
        return toString(countryCode);
    }
};

function findIndexes(cells){
    idx = {}

    for(var i=0; i<cells.length; i++){
        idx[cells[i].innerText.toLowerCase().trim()] = i;
    } 

    return idx
}

const MULT = {
    'kilobyte':  1000,
    'megabyte':  1000 ** 2,
    'gigabyte':  1000 ** 3,
    'terabyte':  1000 ** 4,
    'petabyte':  1000 ** 5,
    'exabyte':   1000 ** 6,
    'zetabyte':  1000 ** 7,
    'yottabyte': 1000 ** 8,
    'kb': 1000,
    'mb': 1000**2,
    'gb': 1000**3,
    'tb': 1000**4,
    'pb': 1000**5,
    'eb': 1000**6,
    'zb': 1000**7,
    'yb': 1000**8,
    'k': 1000,
    'm': 1000**2,
    'g': 1000**3,
    't': 1000**4,
    'p': 1000**5,
    'e': 1000**6,
    'z': 1000**7,
    'y': 1000**8,
}

// Convert human readable format to number (e.g. 1K to 1000)
function short2number(value){
    if( ! isNaN(value) ){
        return Number(value)
    }

    for( var suffix in MULT ){
        clean_value = value.toLowerCase().trim()
        if( clean_value.endsWith(suffix) ){
            var val_num = Number(clean_value.slice(0, -suffix.length) * MULT[suffix])
            return val_num
        }
    }

    return Number(value)
}

/**
 * Format bits as human-readable text.
 * 
 * @param value Number of bits or bytes.
 * @param si True to use metric (SI) units, aka powers of 1000. False to use 
 *           binary (IEC), aka powers of 1024.
 * @param dp Number of decimal places to display.
 * 
 * @return Formatted string.
 */
function number2short(value, si=true, dp=1) {
  const thresh = si ? 1000 : 1024;

  if (Math.abs(value) < thresh) {
    return value ;
  }

  const units = si 
    ? ['k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'] 
    : ['Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'];
  let u = -1;
  const r = 10**dp;

  do {
    value /= thresh;
    ++u;
  } while (Math.round(Math.abs(value) * r) / r >= thresh && u < units.length - 1);


  return value.toFixed(dp) + units[u];
}


// Retrieve traffic data from table
function trafficSunburst(table, agg_column) {
  var router_key = {}; 
  var routers = {}; 
  var data = { 
    type: "sunburst",
    ids: [],
    labels: [],
    text: [],
    parents: [],
    values: [],
    branchvalues: 'total',
    hoverinfo: 'label+text',
    textinfo: 'label'
  }

  table_idx = findIndexes(table.columns().header())
    console.log(table_idx)

  var rows = table.data()
  var vol_threshold = 0
  if(rows.length>1000){
    vol_threshold = 10000000;
  }

    console.log(agg_column)
  // Read the table
  for(var i = 0; i < rows.length; i++){

    let row = rows[i];
    let router = row[table_idx['router']].trim();
    let key = row[table_idx[agg_column]].trim();
    let key_name = row[table_idx[agg_column+' name']].trim();
    let vol_short = row[table_idx['traffic volume']].trim();
    let vol_value = short2number(vol_short);
    let prefix = row[table_idx['prefix']].toLowerCase().trim()
    let prefix_desc = row[table_idx['description']].trim()

    if(vol_value > vol_threshold){
        data["ids"].push( router+key+prefix)
        data["parents"].push( router+key ); 
        data["labels"].push( prefix ); 
        data["text"].push( prefix_desc + '<br>' + vol_short); 
        data["values"].push( vol_value ); 
    }

    if(router+key in router_key){
            router_key[router+key].vol += vol_value; 
        }
    else{
            router_key[router+key] = {
                vol:vol_value,
                key: key,
                key_name: key_name,
                router: router
            }
    }

    if(router in routers){
            routers[router] += vol_value; 
        }
    else{
            routers[router] = vol_value; 
        }
  }

  // add aggregations to the graph (country or ASes)
  for(const rkey in router_key){
    data['ids'].push(rkey)
    data['labels'].push(router_key[rkey].key)
    let vol_short = number2short(router_key[rkey].vol)
    data['text'].push( router_key[rkey].key_name + '<br>' + vol_short)
    data['parents'].push(router_key[rkey].router)
    data['values'].push(router_key[rkey].vol)
  }

  // add root (routers)
  for(const router in routers){
    data['ids'].push(router)
    data['labels'].push(router)
    data['parents'].push('')
    data['values'].push(routers[router])
    let vol_short = number2short(routers[router])
    data['text'].push(vol_short)
  }

  return data;
}
//
// Retrieve traffic data from table
function rttBoxplot(table, selected_country) {
  traces = {}
  table_idx = findIndexes(table.columns().header())
  var rows = table.data()
    
  for (var i = 1; i < rows.length; i++) {
    let row = rows[i]
    let country = row[table_idx['country']].trim();
    if(country == selected_country || selected_country == 'All'){
        let rtt = parseFloat(row[table_idx['min. rtt']].trim());

        // Plot ASN if a country is selected
        var agg = getCountryName(country);
        if(selected_country == country) agg = 'AS'+row[table_idx['asn']].trim();

        if(agg in traces){
            traces[agg]['x'].push( rtt )
        }
        else{ 
            traces[agg] = {
                type: 'box',
                x: [rtt],
                name: agg
            }
        }
    }
  }

  var traces_arr = [];
  for( agg in traces){
      traces_arr.push(traces[agg])
  }

  return traces_arr;
}

function drawTraffic(trafficTable, trafficPlot, agg_column) {
  var trafficData = trafficSunburst(
      trafficTable, agg_column.toLowerCase().trim()
  );
    console.log('plotting sunburst')
  trafficPlot = document.getElementById(trafficPlot);
  var layout = { 
    margin: {l:10, r:10, t:30, b:30},
  }
  Plotly.newPlot(trafficPlot, [trafficData], layout)
    console.log('finished plotting')
}

function drawRtt(rttTable, rttPlot, country) {
  var rttData = rttBoxplot(rttTable, country);
  plotDiv = document.getElementById(rttPlot);
  //let nb_countries = new Set(rttData.y).size
  var layout ={
    xaxis: {
        title: {
            text: 'min. RTT',
        },
        showgrid: false,
        showline: true,
        tickfont: {
            font: {
                color: 'rgb(102, 102, 102)'
            }
        },
        ticks: 'outside',
    },
    margin: {
        l: 100,
        r: 100,
        b: 100,
        t: 10
        },
    height: 150+15*rttData.length,
    showlegend: false,
    hovermode: 'closest'
  }
  
  Plotly.newPlot(plotDiv, rttData, layout)
}

// Sorting function for shorthand notations (e.g. 1M)
jQuery.fn.dataTableExt.oSort['traffic-asc'] = function(x,y) {
    x = short2number(x);
    y = short2number(y);
    return ((x < y) ? -1 : ((x > y) ? 1 : 0));
};

jQuery.fn.dataTableExt.oSort['traffic-desc'] = function(x,y) {
    x = short2number(x);
    y = short2number(y);
    return ((x < y) ? 1 : ((x > y) ? -1 : 0));
};

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function showHide(elem_id) {
  document.getElementById(elem_id).classList.toggle("show");
}

function filterFunction(elem_input, elem_list) {
  var input, filter, ul, li, a, i;
  input = document.getElementById(elem_input);
  filter = input.value.toUpperCase();
  div = document.getElementById(elem_list);
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

/* Rendering functions for datatables*/
function renderASN(data, type, row, meta){
    if ( type === "display" )
    {
        return '<a href="/as_details?asn='+data+'">'+data+'</a>'
    }
    return data
}

function renderCountry(data, type, row, meta){
    if ( type === "display" )
    {
        return '<a href="/country?cc='+data+'">'+isoCountries[data]+'</a>'
    }
    return data
}

function renderRouter(data, type, row, meta){
    if ( type === "display" )
    {
        return '<a href="/traffic?router='+data+'">'+data+'</a>'
    }
    return data
}

function renderTraffic(data, type, row, meta){
    if ( type === "display" )
    {
        return data+'bps'
    }
    return data
}

function renderAtlasProbe(data, type, row, meta){
    if ( type === "display" )
    {
        return '<a href="https://atlas.ripe.net/probes/'+data+'" target="_blank"> PB'+data+'</a>'
    }
    return data
}

function renderASpath(data, type, row, meta){
    if ( type === "display" )
    {
        var aPath = '';
        let asns = data.split(' ')

        for(var i=0; i<asns.length; i++){

            let asn = asns[i]

            if(isNaN(asn)){ 
                aPath += asn+' '
            }
            else{
                aPath += renderASN(asn)+' '
            }

        }
        return aPath
    }
    return data
}


