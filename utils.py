import json
import os

from PIL import Image
from datetime import datetime
from skyfield.api import load, load_file,wgs84
from skyfield.trigonometry import position_angle_of
from skyfield.units import Angle
from skyfield import almanac

class LunarHelper:
    def __init__(self):
        self.__dir__ = os.path.dirname(os.path.realpath(__file__))
        
        json_file = os.path.join(self.__dir__ ,'json', 'illumination.json')
     
        # Load data from JSON file
        with open(json_file, 'r') as file:
            self.data = json.load(file)

        self.eph = self.load_ephemeris()

        self.sun, self.moon, self.earth = self.eph['sun'], self.eph['moon'], self.eph['earth']

    def get_moon_info(self, t, latlon=False):

        phase = almanac.moon_phase(self.eph, t)
       
        e = self.earth.at(t)
        m = e.observe(self.moon).apparent()

        illumination = 100.0 * m.fraction_illuminated(self.sun)
        distance = m.distance().km

        if latlon:
            location = self.earth + wgs84.latlon(*latlon)

            l = location.at(t)
            m = l.observe(self.moon).apparent()
            s = l.observe(self.sun).apparent()

            posang = position_angle_of(m.altaz(), s.altaz())
            if posang.degrees > 180:
                posang = Angle(degrees = 360 - posang.degrees) 
        else:
            posang = False  # no rotation

        return {
            'phase': phase,
            'illumination': illumination,
            'distance': distance,
            'position_angle': posang
        }

    def get_nasa_approx(self, illumination_degree):

        closest_item = min(self.data, key=lambda x: abs(
            x['illumination_degree'] - illumination_degree), default=None)

        return closest_item
    
    def get_illumination_degree(self,illumination,phase):
        if phase <= 180:
            return illumination * 1.8
        else:
            return 360 - illumination*1.8
    
    def load_ephemeris(self,ephemeris_name='de421.bsp', folder_name='bsp'):
        
        folder_name = os.path.join(self.__dir__,folder_name)

        # Ensure the folder exists
        os.makedirs(folder_name, exist_ok=True)
        
        # Construct the path
        ephemeris_path = os.path.join(folder_name, ephemeris_name)

        if not os.path.isfile(ephemeris_path):
            # Download the ephemeris if it is not present
            eph = load(ephemeris_name)
            os.rename(ephemeris_name, ephemeris_path)
            return eph
        else:
            return load_file(ephemeris_path)

class TAT:
    @classmethod
    def rotate_image(cls, input_path, output_path, degrees):

        # Open the image file
        with Image.open(input_path) as img:
            # Rotate the image
            rotated_img = img.rotate(
                degrees, resample=Image.BICUBIC, expand=True)

            # Create a new image with the same size as the original
            # and paste the rotated image onto it
            result_img = Image.new("RGBA", img.size)
            x = (result_img.width - rotated_img.width) // 2
            y = (result_img.height - rotated_img.height) // 2
            result_img.paste(rotated_img, (x, y), rotated_img)

            # Save the result image
            result_img.save(output_path, format='PNG')

    @classmethod
    def valid_date(cls,date_string):
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    @classmethod
    def valid_time(cls,time_string):
        try:
            datetime.strptime(time_string, "%H:%M:%S")
            return True
        except ValueError:
            return False
    @classmethod
    def valid_location(cls,location_string):
        try:
            lat, lon = map(float, location_string.split(','))
            return True
        except ValueError:
            return False
        
    @classmethod
    def contains_slash(cls,s):
        return '/' in s or '\\' in s
