# qbags v.1.0.0
The MIT License (MIT)  
Copyright (c) 2016 Kevin Powell  

## Dependencies
- Python 3.0 or higher
- Bagit-python module. See installation instructions at https://github.com/LibraryOfCongress/bagit-python

## Usage

```
~$ cd path/to/qbags  
~$ python3 qbags-vX.py
```
1. Select a CSV file with bag metadata. Make sure bag names are in the Column A. Values in Row 1 will be metadata fields in bag-info.txt.
2. Select a Source Path with subdirectories you'd like to turn into bags. Make sure those subdirectories match the bag names in the first CSV column.
3. Select a Destination Path for the bags you're creating. If you want to create bags in place, use the Source Path again here.     
4. OPTIONAL: Select a Reports Path with subdirectories that contain additional documentation about any or all of the bags. Directories containing additional documentation must include the bag name (e.g. "Bag001-Reports" for "Bag001"). 
5. OPTIONAL: Compress each bag by selecting 'Zip Bags.'
