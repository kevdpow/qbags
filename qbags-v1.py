import os
import sys
import csv
import itertools
import shutil
import time
import bagit
import codecs
from tkinter import Tk, filedialog, IntVar

import tkinter as tk

class getPaths(tk.Tk):
# builds tkinter window which prompts users for paths
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("qbags v1.0.0 - Browse for Paths")

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="Instructions", command=self.helpText)

        self.label1 = tk.Label(self, text="CSV Path").grid(row=1, column=0, sticky=tk.E)
        self.label2 = tk.Label(self, text="Source Path").grid(row=2, column=0, sticky=tk.E)
        self.label3 = tk.Label(self, text="Destination Path").grid(row=3, column=0, sticky=tk.E)
        self.label4 = tk.Label(self, text="Reports Path").grid(row=5, column=0, sticky=tk.E)

        self.e1 = tk.Entry(self, width=50)
        self.e2 = tk.Entry(self, width=50)
        self.e3 = tk.Entry(self, width=50)
        self.e4 = tk.Entry(self, width=50)

        self.zip = IntVar()
        self.e5 = tk.Checkbutton(self, text="Zip Bags", variable=self.zip)

        self.e1Grid = self.e1.grid(row=1, column=1)
        self.e2Grid = self.e2.grid(row=2, column=1)
        self.e3Grid = self.e3.grid(row=3, column=1)

        self.e4Grid = self.e4.grid(row=5, column=1)
        self.e5Grid = self.e5.grid(row=7, column=0, columnspan=3)

        self.browseCSV = tk.Button(self, text='Browse', command=self.getCSV).grid(row=1, column=2, sticky=tk.W)
        self.browseDirectory = tk.Button(self, text='Browse', command=self.getDirectory).grid(row=2, column=2, sticky=tk.W)
        self.browseTarget = tk.Button(self, text='Browse', command=self.getTarget).grid(row=3, column=2, sticky=tk.W)

        self.browseBrunn = tk.Button(self, text='Browse', command=self.getBrunn).grid(row=5, column=2, sticky=tk.W)
        self.submit = tk.Button(self, text='Submit', command=self.submit, width=30).grid(row=8, column=0, columnspan = 3)
    def helpText(self):
        self.top = tk.Toplevel()
        self.top.config(width=1000)
        self.top.title("Instructions")
        #help menu instructions
        self.instructions="""INSTRUCTIONS:

1) Select a CSV file with bag metadata. Make sure bag names are in Column A. Values in row 1 will be metadata fields in bag-info.txt.

2) Select a Source Path with subdirectories you'd like to turn into bags. Make sure those subdirectories match the bag names in the first CSV column. Otherwise they will not be bagged.

3) Select a Destination Path for the bags you're creating. If you want to create bags in place, use the Source Path again here.

4) OPTIONAL: Select a Reports Path with subdirectories that contain additional documentation about any or all of the bags. Directories containing additional documentation must include the bag name (e.g. "Bag001-Reports" for "Bag001").

5) OPTIONAL: Compress each bag by selecting 'Zip Bags.'"""
        self.msg = tk.Message(self.top, text=self.instructions)
        self.msg.pack()
        self.done = tk.Button(self.top, text="Duly Noted", command=self.top.destroy)
        self.done.pack()
    def getCSV(self):
        self.fileName = tk.filedialog.askopenfilename(filetypes = (('Comma Separated Values', '*.csv'), ('All Files', '*.*')), title = "Choose a CSV File")
        self.e1.insert(0, self.fileName)
    def getDirectory(self):
        self.directoryName = tk.filedialog.askdirectory( title = "Choose Source Directory")
        self.e2.insert(0, self.directoryName)
    def getTarget(self):
        self.targetName = tk.filedialog.askdirectory(title = "Choose Destination Directory")
        self.e3.insert(0, self.targetName)
    def getBrunn(self):
        self.brunnName = tk.filedialog.askdirectory(title = "Choose Brunnhilde Directory")
        self.e4.insert(0, self.brunnName)
    def submit(self):
        self.paths = [self.e1.get(), self.e2.get(), self.e3.get()]
        if self.e4.get():
            self.paths.append(self.e4.get())
        self.zip = [self.zip.get()]
        self.destroy()

app = getPaths()
app.mainloop()
Paths = app.paths
compress = app.zip

CSVPath = Paths[0]
BagPath = Paths[1]
TargetPath = Paths[2]
if len(Paths) == 4: #checking for Reports Path
    BrunnPath = Paths[3]
    if BagPath == BrunnPath:
        print("Error: Source Path and Reports Path cannot be identical. Please store reports elsewhere.")
        sys.exit()
    BrunnList = [f for f in os.listdir(BrunnPath) if os.path.isdir(os.path.join(BrunnPath, f))]

#makes list out of subdirectories in BagPath  
DirList = [f for f in os.listdir(BagPath) if os.path.isdir(os.path.join(BagPath, f))]

print("\n" + "-" * 50 + "\n")

def qbags(CSVFile): #compares DirList to CSV, creates bags from matches
    with open(CSVFile) as ifile:
        CSVData = csv.DictReader(ifile)
        data = [row for row in csv.reader(codecs.open(CSVFile, errors='ignore', encoding='utf-8'))]
        key = data[0][0]
        dir_in_csv = []
        for row in CSVData:
            for dir in DirList:
                if dir == row[key]:
                    FullBagPath = BagPath + '/' + dir
                    FullTargetPath = TargetPath + '/' + dir
                    if FullTargetPath != FullBagPath:
                        shutil.copytree(FullBagPath, FullTargetPath)
                    bagit.make_bag(FullTargetPath)
                    bag = bagit.Bag(FullTargetPath)
                    bag.info.update(row)
                    if len(Paths) == 4:
                        for brunn in BrunnList:
                            if dir in brunn:
                                FullBrunnPath = BrunnPath + '/' + brunn
                                reportsDir = FullTargetPath + '/reports'
                                shutil.copytree(FullBrunnPath, reportsDir)
                                if not bag.is_valid(): #if bag is not valid before bag.save(), qbags will exit
                                    print("{} is not a valid bag.".format(dir))
                                    sys.exit()
                                else:
                                    bag.save(manifests=True)
                    if not bag.is_valid(): #if bag is not valid before bag.save(), qbags will exit
                        print("{} is not a valid bag.".format(dir))
                        sys.exit()
                    else:
                        bag.save()
                    if compress[0] == 1: 
                        os.chdir(TargetPath)
                        shutil.make_archive(dir, 'zip', FullTargetPath)
                        shutil.rmtree(FullTargetPath)
                    print("{} successfully bagged.".format(dir))
                    dir_in_csv.append(dir)
                    time.sleep(2)
        difference = set(DirList) - set(dir_in_csv)
        for i in difference:
            print("{} is not in the CSV and was not bagged.".format(i))
        print("\n" + "-" * 50)

qbags(CSVPath)
