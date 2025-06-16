# script for shrinking all images inside of a resource pack

# Important:
# - use python 3, I don't know if it will work withh python 2
# - ensure that pillow is installed. You can do it with pip:
#     pip install pillow

import os
import shutil
import zipfile
import argparse
from PIL import Image

parser = argparse.ArgumentParser(description=
    "This program reduces the resolution of square textures of a Minecraft Java resource pack \
     to make it playable on smaller hardware. The default is 128x128 to 64x64 pixels. \
     (c) 2025 muejoe / https://github.com/muejoe" )
parser.add_argument("--source_px", type=int, default=128, help="Source resolution in pixel")
parser.add_argument("--target_px", type=int, default=64, help="Target resolution in pixel")
parser.add_argument("source_file", type=str, help="Source filename")

args = parser.parse_args()

print("Resource pack:", args.source_file)
print("Source resolution (px):", args.source_px)
print("Target resolution (px):", args.target_px)

input_file = args.source_file
output_file = 'result.zip'
tmp_dir = 'tmp_unzip'
source_res = args.source_px
target_res = args.target_px

print("Extracting resource pack ...")
with zipfile.ZipFile(input_file, 'r') as zip_ref:
    zip_ref.extractall(tmp_dir)

print("Now scanning for fitting images ...")
converted_count = 0
skipped_count = 0
for root, dirs, files in os.walk(tmp_dir):
    for file in files:
        if file.lower().endswith('.png'):
            path = os.path.join(root, file)
            with Image.open(path) as img:
                width, height = img.size
                if (width, height) == (source_res, source_res): 
                    img = img.resize((target_res, target_res), Image.LANCZOS)
                    img.save(path)
                    converted_count +=1
                    if converted_count % 200 == 0:
                        print("Converted {}, skipped {} ...".format(converted_count, skipped_count))
                else:
                    skipped_count += 1
            
print("Converted {}, skipped {} ...".format(converted_count, skipped_count))

print("Finally creating new resource pack ...")
with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(tmp_dir):
        for file in files:
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, tmp_dir)
            zipf.write(abs_path, rel_path)

print("Removing temporary files ...")
shutil.rmtree(tmp_dir)
print("Finished! New archive:", output_file)