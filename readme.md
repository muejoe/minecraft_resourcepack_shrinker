Minecraft Resourcepack Shrinker
===============================

Prerequisites
-------------
- Python 3
- pillow

Install pillow with:
pip install pillow


It will create a temporary folder called tmp_unzip to extract the source resource pack. 
It will be cleaned afterwards, but the script needs the right to create it and its content.


How to use
----------

Call the tool with -h to see the options

You can just call the tool with the filename of the resourcepack to shrink 
and you can optional change the source and target resolutions with help of parameters.
Default resolution is shrinking from 128x128 to 64x64.
