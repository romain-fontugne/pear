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
        idx[cells[i].textContent.toLowerCase().trim()] = i;
    } 

    return idx
}

// Retrieve traffic data from table
function trafficSunburst(table, agg_column) {
  var router_key = {}; 
  var routers = {}; 
  var data = { 
    type: "sunburst",
    ids: [],
    labels: [],
    parents: [],
    values: [],
    branchvalues: 'total'
  }

  table_idx = findIndexes(table.rows[0].cells)

  var vol_threshold = 0
  if(table.rows.length>1000){
    vol_threshold = 10000000;
  }

  for (var i = 1; i < table.rows.length; i++) {
    let router = table.rows[i].cells[table_idx['router']].textContent.trim();
    let key = table.rows[i].cells[table_idx[agg_column]].textContent.trim();
    let vol = parseInt(table.rows[i].cells[table_idx['traffic volume']].textContent.trim());
    let prefix = table.rows[i].cells[table_idx['prefix']].textContent.toLowerCase().trim()

    
    if(vol > vol_threshold){
        data["ids"].push( router+key+prefix)
        data["parents"].push( router+key ); 
        data["labels"].push( prefix ); 
        data["values"].push( vol ); 
    }

    if(router+key in router_key){
            router_key[router+key].vol += vol; 
        }
    else{
            router_key[router+key] = {
                vol:vol,
                key: key,
                router: router
            }
    }

    if(router in routers){
            routers[router] += vol; 
        }
    else{
            routers[router] = vol; 
        }
  }

  for(const rkey in router_key){
    data['ids'].push(rkey)
    data['labels'].push(router_key[rkey].key)
    data['parents'].push(router_key[rkey].router)
    data['values'].push(router_key[rkey].vol)
  }

  for(const router in routers){
    data['ids'].push(router)
    data['labels'].push(router)
    data['parents'].push('')
    data['values'].push(routers[router])
  }

  return data;
}
//
// Retrieve traffic data from table
function rttBoxplot(table, selected_country) {
  traces = {}
  table_idx = findIndexes(table.rows[0].cells)
    
  for (var i = 1; i < table.rows.length; i++) {
    let country = table.rows[i].cells[table_idx['country']].textContent.trim();
    if(country == selected_country || selected_country == 'All'){
        let rtt = parseFloat(table.rows[i].cells[5].textContent.trim());

        // Plot ASN if a country is selected
        var agg = getCountryName(country);
        if(selected_country == country) agg = 'AS'+table.rows[i].cells[table_idx['asn']].textContent.trim();

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

// Retrieve traffic data from table
function rttDotplot(table, selected_country) {
  var data = { 
    type: 'scatter',
    mode: 'markers',
    x: [],
    y: [],
    marker: {
        color: 'rgba(156, 165, 196, 0.35)',
        line: {
        color: 'rgba(156, 165, 196, 1.0)',
        width: 1,
        },
        symbol: 'circle',
        size: 12
    }
  };

  table_idx = findIndexes(table.rows[0].cells)
    
  for (var i = 1; i < table.rows.length; i++) {
    let country = table.rows[i].cells[table_idx['country']].textContent.trim();
    if(country == selected_country || selected_country == 'All'){
        let rtt = parseFloat(table.rows[i].cells[5].textContent.trim());
        data["x"].push( rtt ); 

        // Plot ASN if a country is selected
        var agg = getCountryName(country);
        if(selected_country == country) agg = 'AS'+table.rows[i].cells[table_idx['asn']].textContent.trim();

        data["y"].push( agg );
    }
  }

  return data;
}

function drawTraffic(trafficTable, trafficPlot, agg_column) {
    console.log('reading data')
  var trafficData = trafficSunburst(
      document.getElementById(trafficTable), agg_column.toLowerCase().trim()
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
  //var rttData = rttDotplot(document.getElementById(rttTable), country);
  var rttData = rttBoxplot(document.getElementById(rttTable), country);
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
