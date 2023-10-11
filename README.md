
# LunarDelight

## Description
LunarDelight provides tools for creating moon-related images and videos using Python. Explore and visualize the dance of the moon in various phases and perspectives through generated media.

## Installation
Ensure that you have Python 3 installed on your system. Follow the steps below to set up LunarDelight:

1. Clone the repository to your local machine.
   ```sh
   git clone https://github.com/dorjeduck/lunardelight.git
   ```
2. Navigate to the project directory.
   ```sh
   cd path/to/LunarDelight
   ```
3. Install the necessary dependencies.
   ```sh
   pip install -r requirements.txt
   ```
4. Download necessary moon images from NASA. (Note: This will download 883MB of images. If there is a problem during the download, simply re-run the script to continue downloading where it left off.)
   ```sh
   python download_nasa_imgs.py
   ```

## Usage
Generate beautiful moon images using simple command-line instructions.

Generate an image of the current moon phase:
```sh
python moon.py
```

To explore various options and ways to specify the date for generating moon imagery, utilize the help command:

```sh
python moon.py -h
```
to see how to specify the date of the moon generated. When a location is given, the rotation of the moon will at seen ffrom the given location will be taken into account.

When you specify a location, LunarDelight ensures the moon's rotation is accurately depicted as it would appear from the given geographical point. This feature enhances the realism and specificity of the generated imagery, providing a true-to-life celestial snapshot from the chosen locale.

The following example generates an image of the moon a new year 2000 as it could be seen over London (latitude: 51.5072°, longitutde: -0.1276).

```sh
python moon.py --date 2000:01:01 -latlon 51.5,-0.13 
```

## License
LunarDelight is distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements
A heartfelt thank you to the following resources that make this project possible:

- NASA Moon Images: [NASA's official site](https://moon.nasa.gov/)
- Skyfield: [GitHub Repository](https://github.com/skyfielders/python-skyfield)

Stay tuned for more updates and features in LunarDelight!
