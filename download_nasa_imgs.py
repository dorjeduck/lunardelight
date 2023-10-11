from PIL import Image
import requests
import os
import json


def process_image(input_path, output_path, scale_factor, rotation_angle, crop_width, crop_height):
    """
    Process an image: scale, rotate, crop and save as PNG.
    
    Parameters:
        input_path (str): Path to the input .tif file.
        output_path (str): Path to save the processed .png file.
        scale_factor (float): Factor to scale the image.
        rotation_angle (float): Angle to rotate the image.
        crop_width (int): Width of the cropped area.
        crop_height (int): Height of the cropped area.
    """
    # Check if the output image already exists
    if os.path.exists(output_path):
        print(f"Image already exists: {output_path}")
        return
    
    # Open the .tif file
    with Image.open(input_path) as img:
        # Scale the image
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        img_resized = img.resize(new_size, Image.LANCZOS)
        
        # Rotate the image
        img_rotated = img_resized.rotate(rotation_angle)
        
        # Calculate the cropping box
        left = (img_rotated.width - crop_width) // 2
        top = (img_rotated.height - crop_height) // 2
        right = (img_rotated.width + crop_width) // 2
        bottom = (img_rotated.height + crop_height) // 2
        
        # Crop the image
        img_cropped = img_rotated.crop((left, top, right, bottom))
        
        # Save the image in .png format
        img_cropped.save(output_path, 'PNG')
        print(f"Processed and saved: {output_path}")



# Ensure to create a folder to store the downloaded files and avoid clutter
output_folder = 'nasa'
os.makedirs(output_folder, exist_ok=True)


# prepare processing of images

# URL of the JSON file
url = "https://svs.gsfc.nasa.gov/vis/a000000/a005000/a005048/mooninfo_2023.json"

# Path to the subfolder where the file should be saved
folder_path = "json"
file_name = "mooninfo_2023.json"
full_path = os.path.join(folder_path, file_name)

# Check if the subfolder does not exist, if true, create it
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Check if the file does not exist in the subfolder
if not os.path.exists(full_path):
    # Send a HTTP request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (HTTP Status Code 200)
    if response.status_code == 200:
        # Write the content to a file in binary mode
        with open(full_path, "wb") as f:
            f.write(response.content)
        print(f"{file_name} has been downloaded and saved to {full_path}")
    else:
        print(f"Failed to retrieve the file: {url}")
        exit()
else:
    print(f"{file_name} already exists in {full_path}")


json_file = os.path.join('json','mooninfo_2023.json')

with open(json_file, 'r', encoding='utf-8') as file:
    # Load JSON data from file
    data = json.load(file)

max_diameter = max(data, key=lambda x: x['diameter'])['diameter']


# URL pattern for 2023
url_pattern = "https://svs.gsfc.nasa.gov/vis/a000000/a005000/a005048/frames/1920x1080_16x9_30p/plain/moon.{:04d}.tif"

# Loop through the required img file numbers (2622 - 3328)
for i, img_num in enumerate(range(2622, 3329)):
    # Generate the URL
    url = url_pattern.format(img_num)

    local_tif_path = os.path.join(output_folder,f"moon.{img_num:04d}.tif")
    local_png_path = os.path.join(output_folder,f"moon.{i+1:03d}.png")

    if os.path.exists(local_png_path):
        print(f"Already done: {local_png_path}")
        continue
   
    
    # Download the file
    response = requests.get(url)
    
    # Check if request was successful (HTTP Status Code 200)
    if response.status_code == 200:
        # Save the file
        with open(local_tif_path, "wb") as f:
            f.write(response.content)
      
        process_image(local_tif_path,local_png_path,
                  max_diameter/data[img_num]['diameter'],360-data[img_num]['posangle'],1080,1080)
   
        os.remove(local_tif_path)

    else:
        print(f"Failed to download: {url}")
    
    # Pause for 5 second to avoid overwhelming the server
    # time.sleep(5)

