from __future__ import print_function, division
from datetime import datetime
from os import popen, listdir
from os.path import join, isfile
import pytz
import yaml
from collections import OrderedDict

PATH = "/data/mine/vadeec/merged"
TIMEZONE = "Europe/London"
TZ = pytz.timezone(TIMEZONE)
N_BULDINGS = 4

# TODO: 
# both appliances and meters should be a list, not a dict
# appliance name is defined by parent, not given
# meters need an 'id'

dataset = {
    "name": "UKPD",
    "full_name": "UK Power Dataset",
    "urls": ["http://www.doc.ic.ac.uk/~dk3810/data"], 
    "contact": "jack.kelly@imperial.ac.uk", 
    "citations": [""], 
    "mains_voltage": {
        "nominal": 230,
        "tolerance_upper_bound": 6, 
        "tolerance_lower_bound": 10
    },
    "number_of_buildings": N_BULDINGS, 
    "geo_location": {
        "city": "London",
        "country": "UK", 
        "latitude": 51.464462, 
        "longitude": -0.076544
    }, 
    "timezone": TIMEZONE,
    "institution": "Imperial College London", 
    "description": "Recording from 4 domestic homes in or near to London, UK.\n"
}

appliance_map = {
    1: [
        {
            'parent': 'Worcester~Greenstar CDi Conventional',
            'instance': 1,
            'room': {'name': 'bathroom', 'instance': 1},
            'original_name': 'boiler'
        }
    ]
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

dataset['buildings'] = {}
for building_i in range(1,N_BULDINGS+1):
    building = {'utilities': {'electric': {'meters': [], 'appliances': []}}}
    dataset['buildings'][building_i] = building
    building_path = join(PATH, 'house_{:d}'.format(building_i))
    electric = building['utilities']['electric']

    #--------- METERS -------------------------------
    mains = join(building_path, 'mains.dat')
    mains_exists =  isfile(mains)
    labels = load_labels(building_path)
    building_start = None
    building_end = None
    meters = electric['meters']
    for chan, label in labels.iteritems():
        fname = join(building_path, 'channel_{:d}.dat'.format(chan))
        start = start_time(fname)
        end = end_time(fname)
        if building_start is None or start < building_start:
            building_start = start
        if building_end is None or end > building_end:
            building_end = end

        meter = {'id': chan,
                 'dates_active': [ timeframe(start, end) ],
                 'original_label': label}
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
            'id': len(meters)})

    building['timeframe'] = timeframe(building_start, building_end)

    #------------ APPLIANCES --------------------
    appliances = electric['appliances']
        
    

print(yaml.dump(dataset))
