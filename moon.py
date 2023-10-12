from utils import LunarHelper, TAT
from skyfield.api import load
from datetime import datetime

import argparse
import os
import shutil
import json

parser = argparse.ArgumentParser(description='Create a moon image from a given date, time, and location.')
parser.add_argument('-d', '--date', help='Date in format YYYY-mm-dd')
parser.add_argument('-t', '--time', help='Time in format HH:MM:SS - according to UTC)')
parser.add_argument('-l', '--location', help='Location in format "lat,lon"')
parser.add_argument('-o', '--output', help='Output file name without extension (no slashes...)')

args = parser.parse_args()

date = args.date
time = args.time
location = args.location
output = args.output

# Check formats
if date and not TAT.valid_date(date):
    print("Error: Date is not in the correct format (YYYY-mm-dd)")
    exit(1)
if time and not TAT.valid_time(time):
    print("Error: Time is not in the correct format (HH:MM:SS)")
    exit(1)
if location and not TAT.valid_location(location):
    print('Error: Location is not in the correct format ("lat,lon")')
    exit(1)
if output and TAT.contains_slash(output):
    print('Error: Output file name contains a slash')
    exit(1)

__dir__ = os.path.dirname(os.path.realpath(__file__))
ts = load.timescale()


if not (date or time):
    t = ts.now()
else:
    if date:
        year, month, day = map(int, date.split('-'))
    else:
        now = datetime.utcnow()
        year, month, day = now.year, now.month, now.day

    t = ts.utc(year, month, day)

    if time:
        hour, minute, second = map(int, time.split(':'))
        t += ts.utc(hour, minute, second)




os.makedirs( os.path.join(__dir__,'output'), exist_ok=True)
 
if not output:   
    time_str =  t.utc_strftime('%Y-%m-%d_%H:%M:%S')
    output_name = os.path.join(__dir__,'output','moon_' + time_str)
else:
    output_name = os.path.join(__dir__,'output',output)

if location:
    lat, lon = map(float, location.split(','))
    latlon = (lat,lon)
else:
    latlon = None


lunar_helper = LunarHelper()


""" latlon = (51.5,-0.12)  #London
latlon = (50.8,6.1)  #Aachen
latlon = (-22.9068,-43.1729) #Rio """

moon_info = lunar_helper.get_moon_info(t,latlon)

illumination_degrees = lunar_helper.get_illumination_degree(moon_info['illumination'],moon_info['phase'].degrees)

nasa_approx = lunar_helper.get_nasa_approx(illumination_degrees)

nasa_png = os.path.join(__dir__,'nasa','moon.{:03d}.png'.format(nasa_approx["img_num"]))

if moon_info['position_angle']:
    output_name += "_{:.03f}_{:.03f}".format(*latlon)
   
    TAT.rotate_image(nasa_png,output_name + '.png',moon_info['position_angle'].degrees -90)
    moon_info['latitude'],moon_info['longitude'] = latlon[0], latlon[1]
    moon_info['position_angle'] = round(moon_info['position_angle'].degrees,2)

else:
    print(nasa_png)
    shutil.copy(nasa_png,output_name + '.png')
    del moon_info['position_angle']

moon_info['time'] = t.utc_strftime('%Y-%m-%d %H:%M:%S (UTC)')
moon_info['phase'] = round(moon_info['phase'].degrees,2)
moon_info['illumination'] = round(moon_info['illumination'],2)
moon_info['distance'] = round(moon_info['distance'])

moon_info['json'] = output_name + '.json'
moon_info['image'] = output_name + '.png'

with open(output_name + '.json', 'w') as f:
    json.dump(moon_info, f, indent=4)

print(json.dumps(moon_info, indent=2))
