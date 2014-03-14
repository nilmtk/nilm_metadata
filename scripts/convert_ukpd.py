from __future__ import print_function, division
from datetime import datetime
from os import popen, listdir
from os.path import join, isfile, expanduser
import pytz
import yaml
from collections import OrderedDict

RAW_UKPD_DATA_PATH = "/data/mine/vadeec/merged"
OUTPUT_FILENAME = "~/workspace/schemas/nilm_metadata/examples/ukpd_dataset.yaml"
OUTPUT_FILENAME = expanduser(OUTPUT_FILENAME)

TIMEZONE = "Europe/London"
TZ = pytz.timezone(TIMEZONE)
N_BULDINGS = 4

dataset = {
    "title": "UK Power Dataset",
    "short_title": "UKPD",
    "subject": "Disaggregated domestic electricity demand",
    "geospatial_coverage": "Southern England",
    "publisher": "UK Energy Research Centre Energy Data Centre (UKERC EDC)",
    "data_formats_and_locations": [{
        "name": "CSV (NILMTK schema)",
        "raw_data_location": "http://www.doc.ic.ac.uk/~dk3810/data",
        "cleaned_data_location": "TODO"
    }],
    "creators": ["Kelly, Jack"],
    "contact": "jack.kelly@imperial.ac.uk",
    "institution": "Imperial College London", 
    "description": (
        "Appliance-by-appliance and whole-home power demand for 4 UK homes."
        " Appliance data was recorded once every 6 seconds.  Whole-home data"
        " was recorded once every 6 seconds for 2 homes and additionally at"
        " 16kHz for the other 2 homes.  Detailed metadata is included."
    ),
    "publication_date": "2014-03-14",
    "related_documents": [(
        "The following poster describes the metering setup and provides some analyses:"
        " Jack Kelly and William Knottenbelt." 
        " Smart Meter Disaggregation: Data Collection & Analysis."
        " UK Energy Research Council Summer School Ph.D. poster session."
        " June 2013. PDF: http://www.doc.ic.ac.uk/~dk3810/writing/UKERC_poster2013_v2.pdf"
    )], 
    "mains_voltage": {
        "nominal": 230,
        "tolerance_upper_bound": 6, 
        "tolerance_lower_bound": 10
    },
    "items": "buildings",
    "number_of_items": N_BULDINGS, 
    "geo_location": {
        "country": "GB", 
        "locality": "London",
        "latitude": 51.464462, 
        "longitude": -0.076544
    }, 
    "timezone": TIMEZONE,
    "schema": "https://github.com/nilmtk/nilm_metadata/tree/v0.1.0",
    "funding": [
        "Jack Kelly's PhD is funded by an EPSRC DTA", 
        "Hardware necessary for this project was funded from"
        " Jack Kelly's Intel EU PhD Fellowship"],
    "rights_list": [{
        "name": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "uri": "http://creativecommons.org/licenses/by/4.0/"
    }],
    "description_of_subjects": "3 MSc students and 1 PhD student."
}

building_metadata = {
    1: {
        "rooms": [
            {"name": "lounge", "floor": 0},
            {"name": "hall", "instance": 1,  "floor": 0},
            {"name": "hall", "instance": 2,  "floor": 1},
            {"name": "kitchen", "floor": 0},
            {"name": "utility", "floor": 0},
            {"name": "dining room", "floor": 0},
            {"name": "bedroom", "instance": 1, "floor": 1, 
             "description": "master bedroom"},
            {"name": "bedroom", "instance": 2, "floor": 1, 
             "description": "kid's bedroom"},
            {"name": "study", "instance": 1, "floor": 1, 
             "description": "occasionally used as a spare bedroom "},
            {"name": "bathroom", "instance": 1, "floor": 1, 
             "description": "shower + bath + toilet + sink + cupboards "
             "+ hot water tank + boiler + solar thermal pumping station"}
        ]
    },
    2: {},
    3: {},
    4: {}
}

appliances_for_each_building = {
    1: [
        {
            'parent': 'Worcester~Greenstar 30CDi Conventional natural gas',
            'room': {'name': 'bathroom'},
            'original_name': 'boiler',
            'year_of_purchase': 2011
        },
        {
            'parent': 'Navitron~Solar Thermal Pumping Station',
            'room': {'name': 'bathroom'},
            'original_name': 'solar_thermal_pump',
            'year_of_purchase': 2011
        },
        {
            'parent': 'HP~ProBook 6450b',
            'original_name': 'laptop',
            'year_of_purchase': 2010,
            'room': {'name': 'study'}
        },
        {
            'parent': 'washer dryer',
            'original_name': 'washing_machine',
            'year_of_purchase': 2007,
            'manufacturer': 'Hotpoint',
            'brand': 'Aquarius',
            'model': 'WD420 1200 spin',
            'room': {'name': 'utility'}
        },
        {
            'parent': 'dish washer',
            'original_name': 'dishwasher',
            'year_of_purchase': 2007,
            'manufacturer': 'Whirlpool / Ikea',
            'model': 'DWH B10',
            'room': {'name': 'kitchen'}
        },
        {
            'parent': 'television',
            'original_name': 'tv',
            'year_of_manufacture': 2001,
            'manufacturer': 'Panasonic',
            'components': [
                {
                    'parent': 'CRT screen',
                    'display_format': 'PAL',
                    'diagonal_size': 34
                }
            ],
            'room': {'name': 'lounge'}
        },
        {
            'parent': 'light',
            'original_name': 'kitchen_lights',
            'description': '10 50W downlights in the kitchen ceiling',
            'subtype': 'ceiling downlight',
            'room': {'name': 'kitchen'},
            'main_room_light': True,
            'components': [
                {
                    'parent': 'incandescent lamp',
                    'count': 10,
                    'nominal_consumption': { 'on_power': 50 }
                },
                {
                    'parent': 'dimmer', 'subtype': 'TRIAC'
                }
            ],
            'nominal_consumption': { 'on_power': 500 },
            'dates_active': [{'end': '2013-04-25T07:59:00+01:00'}]
        },
        {
            'parent': 'light',
            'original_name': 'kitchen_lights',
            'description': '10 LED downlights in the kitchen ceiling',
            'subtype': 'ceiling downlight',
            'main_room_light': True,
            'components': [
                {
                    'parent': 'LED lamp',
                    'count': 10,
                    'manufacturer': 'Philips',
                    'model': 'Dimmable MASTER LED 10W MR16 GU5.3 24degrees 2700K 12v',
                    'nominal_consumption': { 'on_power': 10 }
                },
                {
                    'parent': 'dimmer', 'subtype': 'TRIAC'
                }
            ],
            'nominal_consumption': { 'on_power': 100 },
            'dates_active': [{'start': '2013-04-25T08:00:00+01:00'}]
        },
        {
            'parent': 'HTPC',
            'original_name': 'htpc',
            'year_of_purchase': 2008,
            'room': {'name': 'lounge'}
        },
        {
            'parent': 'kettle',
            'original_name': 'kettle',
            'year_of_purchase': 2007,
            'room': {'name': 'kitchen'}
        },
        {
            'parent': 'toaster',
            'original_name': 'toaster',
            'year_of_purchase': 2009,
            'room': {'name': 'kitchen'}
        },
        {
            'parent': 'fridge freezer',
            'subtype': 'fridge on top',
            'original_name': 'fridge',
            'year_of_purchase': 2010,
            'room': {'name': 'kitchen'}
        },
        {
            'parent': 'microwave',
            'original_name': 'microwave',
            'room': {'name': 'kitchen'},
            'year_of_purchase': 2006
        },
        {
            'parent': 'computer monitor',
            'original_name': 'lcd_office',
            'room': {'name': 'study'},
            'components': [
                {
                    'parent': 'flat screen',
                    'display_technology': 'LCD',
                    'diagonal_size': 24,
                    'manufacturer': 'Dell'
                }
            ],
            'year_of_purchase': 2010
        },
        {
            'parent': 'audio system',
            'original_name': 'hifi_office',
            'room': {'name': 'study'},
            'components': [
                {
                    'parent': 'audio amplifier',
                    'year_of_purchase': 2012,
                    'components': [ {'parent': 'DAC'} ]
                },
                {
                    'parent': 'radio',
                    'year_of_purchase': 1995
                },
                {
                    'parent': 'CD player',
                    'year_of_purchase': 1995
                }
            ]
        },
        {
            'parent': 'breadmaker',
            'original_name': 'breadmaker',
            'room': {'name': 'kitchen'},
            'year_of_purchase': 2010
        },
        {
            'parent': 'audio amplifier',
            'original_name': 'amp_livingroom',
            'room': {'name': 'lounge'},
            'year_of_purchase': 2004
        },
        {
            'parent': 'broadband router',
            'original_name': 'adsl_router',
            'room': {'name': 'hall'},
            'year_of_purchase': 2006
        },
        {
            'parent': 'light',
            'original_name': 'livingroom_s_lamp',
            'room': {'name': 'lounge'},
            'subtype': 'floor standing',
            'year_of_purchase': 2006,
            'components': [{'parent': 'compact fluorescent lamp'}]
        },
        {
            'parent': 'soldering iron',
            'original_name': 'soldering_iron',
            'room': {'name': 'study'},
            'year_of_purchase': 2011
        },
        {
            'parent': 'ethernet switch',
            'original_name': 'gigE_&_USBhub',
            'subtype': '1gigabit',
            'room': {'name': 'study'},
            'year_of_purchase': 2008
        },
        {
            'parent': 'USB hub',
            'original_name': 'gigE_&_USBhub',
            'room': {'name': 'study'},
            'year_of_purchase': 2008
        },
        {
            'parent': 'vacuum cleaner',
            'original_name': 'hoover',
            'year_of_purchase': 2008
        },
        {
            'parent': 'light',
            'instance': 2,
            'subtype': 'table',
            'original_name': 'kitchen_dt_lamp',
            'room': {'name': 'kitchen'},
            'components': [
                {'parent': 'incandescent lamp'},
                {'parent': 'dimmer', 'number_of_dimmer_levels': 3 }
            ],
            'year_of_purchase': 2006
        },
        {
            'parent': 'light',
            'instance': 3,
            'subtype': 'floor standing',
            'original_name': 'bedroom_ds_lamp',
            'room': {'name': 'bedroom', 'instance': 1},
            'components': [
                {'parent': 'incandescent lamp'},
                {'parent': 'dimmer', 'subtype': 'TRIAC'}
            ],
            'year_of_purchase': 2006
        },
        {
            'parent': 'light',
            'instance': 4,
            'subtype': 'floor standing',
            'original_name': 'livingroom_s_lamp2',
            'room': {'name': 'lounge'},
            'year_of_purchase': 2006,
            'components': [{'parent': 'compact fluorescent lamp'}]
        },
        {
            'parent': 'tablet computer charger',
            'original_name': 'iPad_charger',
            'room': {'name': 'lounge'},
            'year_of_purchase': 2012,
            'manufacturer': 'Apple'
        },
        {
            'parent': 'active subwoofer',
            'original_name': 'subwoofer_livingroom',
            'room': {'name': 'lounge'},
            'year_of_purchase': 2003
        },
        {
            'parent': 'light',
            'instance': 5,
            'original_name': 'livingroom_lamp_tv',
            'room': {'name': 'lounge'},
            'year_of_purchase': 2006,
            'components': [{'parent': 'compact fluorescent lamp'}],
            'subtype': 'mood',
            'description': 'throws light onto the wall behind the television'
        },
        {
            'parent': 'radio',
            'subtype': 'DAB',
            'original_name': 'DAB_radio_livingroom',
            'room': {'name': 'lounge'},
            'year_of_purchase': 2012
        },
        {
            'parent': 'light',
            'instance': 6,
            'subtype': 'floor standing',
            'original_name': 'kitchen_lamp2',
            'components': [{'parent': 'compact fluorescent lamp'}],
            'room': {'name': 'kitchen'},
            'year_of_purchase': 2006
        },
        {
            'parent': 'wireless phone charger',
            'original_name': 'kitchen_phone&stereo',
            'room': {'name': 'kitchen'},
            'year_of_purchase': 2009
        },
        {
            'parent': 'audio system',
            'original_name': 'kitchen_phone&stereo',
            'room': {'name': 'kitchen'},
            'year_of_purchase': 2009
        },
        {
            'parent': 'light',
            'instance': 7,
            'original_name': 'utilityrm_lamp',
            'room': {'name': 'utility'},
            'components': [{'parent': 'linear fluorescent lamp'}],
            'year_of_purchase': 2006
        },
        {
            'parent': 'mobile phone charger',
            'original_name': 'samsung_charger',
            'room': {'name': 'bedroom', 'instance': 1},
            'year_of_purchase': 2012,
            'manufacturer': 'Samsung'
        },
        {
            'parent': 'light',
            'instance': 8,
            'subtype': 'table',
            'components': [
                {'parent': 'incandescent lamp'},
                {'parent': 'dimmer', 'number_of_dimmer_levels': 3 }
            ],
            'original_name': 'bedroom_d_lamp',
            'room': {'name': 'bedroom', 'instance': 1},
            'year_of_purchase': 2006
        },
        {
            'parent': 'coffee maker',
            'original_name': 'coffee_machine',
            'room': {'name': 'kitchen'},
            'year_of_purchase': 2010
        },
        {
            'parent': 'radio',
            'subtype': 'analogue',
            'original_name': 'kitchen_radio',
            'room': {'name': 'kitchen'},
            'year_of_purchase': 2004
        },
        {
            'parent': 'charger',
            'original_name': 'bedroom_chargers',
            'room': {'name': 'bedroom', 'instance': 1},
            'description': 'mobile phone charger and baby monitor RX charger',
            'year_of_purchase': 2006
        },
        {
            'parent': 'hair dryer',
            'original_name': 'hair_dryer',
            'room': {'name': 'bedroom', 'instance': 1},
            'year_of_purchase': 2013
        },
        {
            'parent': 'hair straighteners',
            'original_name': 'straighteners',
            'room': {'name': 'bedroom', 'instance': 1},
            'year_of_purchase': 2006
        },
        {
            'parent': 'clothes iron',
            'original_name': 'iron',
            'room': {'name': 'bedroom', 'instance': 1},
            'year_of_purchase': 2006
        },
        {
            'parent': 'oven',
            'original_name': 'gas_oven',
            'room': {'name': 'kitchen'},
            'fuel': 'natural gas',
            'year_of_purchase': 2000
        },
        {
            'parent': 'computer',
            'original_name': 'data_logger_pc',
            'do_not_inherit': ['control'],
            'control': ['always on'],
            'description': 'data logging PC',
            'cpu': 'Intel Atom',
            'room': {'name': 'hall'},
            'year_of_purchase': 2012
        },
        {
            'parent': 'light',
            'instance': 9,
            'subtype': 'table',
            'components': [{'parent': 'incandescent lamp'}],
            'year_of_purchase': 2006,
            'original_name': 'childs_table_lamp',
            'room': {'name': 'bedroom', 'instance': 2}
        },
        {
            'parent': 'light',
            'instance': 10,
            'subtype': 'floor standing',
            'description': 'reading lamp',
            'original_name': 'childs_ds_lamp',
            'components': [{'parent': 'LED lamp'}, {'parent': 'dimmer'}],
            'room': {'name': 'bedroom', 'instance': 2},
            'year_of_purchase': 2006
        },
        {
            'parent': 'baby monitor',
            'original_name': 'baby_monitor_tx',
            'subtype': 'baby unit',
            'room': {'name': 'bedroom', 'instance': 2},
            'year_of_purchase': 2011
        },
        {
            'parent': 'charger',
            'original_name': 'battery_charger',
            'room': {'name': 'study'},
            'year_of_purchase': 2008
        },
        {
            'parent': 'light',
            'instance': 11,
            'components': [{'parent': 'compact fluorescent lamp'}],
            'original_name': 'office_lamp1',
            'subtype': 'mood',
            'room': {'name': 'study'},
            'year_of_purchase': 2006
        },
        {
            'parent': 'light',
            'instance': 12,
            'components': [{'parent': 'compact fluorescent lamp'}],
            'original_name': 'office_lamp2',
            'subtype': 'mood',
            'room': {'name': 'study'},
            'year_of_purchase': 2006

        },
        {
            'parent': 'light',
            'instance': 13,
            'components': [{'parent': 'compact fluorescent lamp'}],
            'original_name': 'office_lamp3',
            'subtype': 'table',
            'room': {'name': 'study'},
            'year_of_purchase': 2006
        },
        {
            'parent': 'desktop computer',
            'original_name': 'office_pc',
            'room': {'name': 'study'},
            'year_of_purchase': 2007
        },
        {
            'parent': 'fan',
            'subtype': 'desk',
            'original_name': 'office_fan',
            'room': {'name': 'study'},
            'year_of_purchase': 2006
        },
        {
            'parent': 'printer',
            'subtype': 'LED',
            'original_name': 'LED_printer',
            'room': {'name': 'study'},
            'year_of_purchase': 2012
        }
    ],
    2: [],
    3: [],
    4: []
}

def load_labels(data_dir):
    """Loads data from labels.dat file.

    Parameters
    ----------
    data_dir : str

    Returns
    -------
    labels : dict
         mapping channel numbers (ints) to appliance names (str)
    """
    filename = join(data_dir, 'labels.dat')
    with open(filename) as labels_file:
        lines = labels_file.readlines()

    labels = {}
    for line in lines:
        line = line.split(' ')
        # TODO add error handling if line[0] not an int
        labels[int(line[0])] = line[1].strip()

    return labels

def chan_for_label(target, labels):
    for chan, label in labels.iteritems():
        if label == target:
            return chan
    raise KeyError()

def _line_to_datetime(line):
    timestamp = line.partition(" ")[0]
    return datetime.fromtimestamp(float(timestamp), tz=TZ)

def end_time(filename):
    last_line = popen("tail -n 1 %s" % filename).read()
    return _line_to_datetime(last_line)

def start_time(filename):
    first_line = popen("head -n 1 %s" % filename).read()
    return _line_to_datetime(first_line)

def timeframe(start, end):
    return {'start': start.isoformat(), 'end': end.isoformat()}

dataset['buildings'] = []
dataset_start = None
dataset_end = None
for building_i in range(1,N_BULDINGS+1):
    building = building_metadata[building_i]
    building['building_id'] = building_i
    building.update({'utilities': {'electric': {'meters': [], 'appliances': []}}})
    building['dataset'] = dataset['short_title']
    dataset['buildings'].append(building)
    building_path = join(RAW_UKPD_DATA_PATH, 'house_{:d}'.format(building_i))
    electric = building['utilities']['electric']

    #--------- METERS -------------------------------
    mains = join(building_path, 'mains.dat')
    mains_exists =  isfile(mains)
    labels = load_labels(building_path)
    building_start = None
    building_end = None
    meters = electric['meters']
    chans = labels.keys() # we want to process meters in order
    chans.sort()
    for chan in chans:
        label = labels[chan]
        fname = join(building_path, 'channel_{:d}.dat'.format(chan))
        start = start_time(fname)
        end = end_time(fname)
        if building_start is None or start < building_start:
            building_start = start
        if building_end is None or end > building_end:
            building_end = end

        meter = {'meter_id': chan,
                 'dates_active': [ timeframe(start, end) ],
                 'original_name': label,
                 'data_location': 'house_{:d}/channel_{:d}.dat'.format(building_i, chan)}
        if label == 'aggregate':
            meter.update({"site_meter": True,
                          'parent': 'EDFEnergy~EcoManagerWholeHouseTx'})
        elif building_i == 1 and label == 'kitchen_lights':
            meter.update({"submeter_of": chan_for_label('lighting_circuit', labels),
                          'parent': 'CurrentCost~Tx'})
        elif building_i == 1 and label in ['boiler', 'solar_thermal_pump', 'lighting_circuit']:
            meter.update({"submeter_of": 0 if mains_exists else 1,
                          'parent': 'CurrentCost~Tx'})            
        else:
            meter.update({"submeter_of": 0 if mains_exists else 1,
                          'parent': 'EDFEnergy~EcoManagerTxPlug'})

        meters.append(meter)
        
    if mains_exists:
        meters.append({
            'parent': 'JackKelly~SoundCardPowerMeter',
            'dates_active': [timeframe(start_time(mains), end_time(mains))],
            'site_meter': True,
            'meter_id': len(meters),
            'data_location': 'house_{:d}/mains.dat'.format(building_i)
        })

    building['temporal_coverage'] = timeframe(building_start, building_end)
    if dataset_start is None or building_start < dataset_start:
        dataset_start = start
    if dataset_end is None or building_end > dataset_end:
        dataset_end = end

    #------------ APPLIANCES --------------------
    appliances = appliances_for_each_building[building_i]

    # infer meter IDs from original_name and labels.dat
    for i in range(len(appliances)):
        appliance = appliances[i]
        appliance['meter_ids'] = [chan_for_label(appliance['original_name'], labels)]
    
    electric['appliances'] = appliances
    
dataset['temporal_coverage'] = timeframe(dataset_start, dataset_end)
    
with open(OUTPUT_FILENAME, 'w') as fh:
    yaml.dump(dataset, fh)

print("done")
