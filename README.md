# qbags v.1.0.0
The MIT License (MIT)  
Copyright (c) 2016 Kevin Powell

## Overview  
Qbags uses CSV data and the bagit-python module to create bags from subdirectories in a designated source path. A CSV bag queue should include the subdirectories' names and any metadata you'd like to include in each bag's bag-info.txt file. 

Tested in Mac OSX 10.11.16, Windows 10, and Ubuntu 16.04 LTS.

## Dependencies
- Python 3.0 or higher
- Bagit-python module. See installation instructions at https://github.com/LibraryOfCongress/bagit-python

## Usage

### UNIX/MacOSX/Linux
```
$ cd path/to/qbags  
$ python3 qbags-vX.py
```
### Windows 10
- Right-click qbags-vX.py
- Open With...
- Select "Python Launcher for Windows (Console)"

### Instructions
1. Select a CSV file with bag metadata. Make sure bag names are in Column A. Values in Row 1 will be metadata fields in bag-info.txt.
2. Select a Source Path with subdirectories you'd like to turn into bags. Make sure those subdirectories match the bag names in the first CSV column.
3. Select a Destination Path for the bags you're creating. If you want to create bags in place, use the Source Path again here.     
4. OPTIONAL: Compress each bag by selecting 'Zip Bags.'

## Further Development
- Write bagging date and/or bag path to CSV (or another document), creating a log of completed work.  
- Add compression options. 
- Prompt user to overwrite or rename bag if an identical version exists in destination path.
