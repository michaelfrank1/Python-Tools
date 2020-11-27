""" 
The purpose of this script is to place all infinite docking graphs in one Excel spreadsheet 
The script reads the x-y column in a .csv spreadsheet and then this tool will take the data
and visually display it in a graph, showing the path the robot took for each infinite docking
session. 
"""

#!/bin/bash

import fnmatch
import os
import pandas as pd
import string                   # import string library function
import tkinter as tk
import xlsxwriter
from matplotlib import pyplot as plt
from tkinter import Tk, filedialog, messagebox

root = tk.Tk()

# function creates image files
def plotInfDocking(dir):

    # initialization
    count = fileCount = rowNumber = x = y  = 0
    
    # list of filenames created
    fileNames = os.listdir(dir)
    
    # find and print total number of images found
    numfiles = len(fnmatch.filter(os.listdir(dir), 'run*.csv'))
    print(f"Total number of images found: ", numfiles)

    input("Press Enter key to continue . . .")

    # read each filename
    for fileName in fileNames:
            if fileName.startswith("docking"):
                continue

            # create path
            targetFile = os.path.join(dir, fileName)
                                                
            # splitting the string at the last period using .rsplit
            f_extns = targetFile.rsplit('.', 1)
                       
            # if not a .csv file, go to the next file
            if (f_extns[1] != "csv"):
                continue

            # slice run filename and eliminate extension
            photoFile = f_extns[0]
            begin = photoFile.find("run")
            photo = photoFile[begin:]

            # counting files
            fileCount += 1

            # create .jpg file
            photoFileName = os.path.join(dir, photo + ".jpg")
            
            # open .csv file
            fo = open(targetFile, "r")

            # creating dataframe - reading the values from the xy columns in the worksheet
            df = pd.read_csv(targetFile, sep = ',')

            # plot graph
            plt.plot(df['x'], df['y'])

            # eliminated 'plt.ion' so that figure box does not flash on screen

            # display filename at top of graph
            plt.title(fileName)

            # x label
            plt.xlabel("X axis (centimeters)")

            # y label
            plt.ylabel("Y axis (centimeters)")

            # show graph
            # plt.show()

            # save chart to file
            plt.savefig(photoFileName)

            #close graph
            plt.close()

            # close file
            fo.close

            # scale image
            image_width = 14.0
            image_height = 18.2

            cell_width = 6.4
            cell_height = 2.0

            x_scale = cell_width/image_width
            y_scale = cell_width/image_width

            # insert images (5 per row)
            if(fileCount<=5):
                count += 1
                worksheet.insert_image(x, y, photoFileName, {'x_scale': x_scale, 'y_scale': y_scale})
                # print("image #{} created at location {}.".format(count, y))
                print("image #{} created.".format(count))
                # print(photoFileName)

                # xy location of image on worksheet
                y += 5
                
            if(fileCount==5):
                rowNumber += 1
                print('Row #{} has been completed.'.format(rowNumber))

                # start new row
                x += 10

                # create new image in first column
                if(y > 5):
                    y = 0

                # reset fileCount to zero
                fileCount = 0

                # reset 'y' to zero
                # if(y > 5):
                #     y = 0

if __name__ == '__main__':
    # global variables
    yearN = 0

    # remove Tkinter root window
    root.withdraw()

    # choose where infinite docking run files are located
    answer = messagebox.askokcancel("Choose Folder","Choose docking file folder with run files in it")
    folder = filedialog.askdirectory()

    # replace char in string
    newFolder = folder.replace(".", " ")

    begin = folder.find('202' + str(yearN) + '-')
        
    # if year not found, loop to find it
    while(begin == -1):
        begin = folder.find('202' + str(yearN) + '-')
        yearN += 1

        # when year is not found in filename, then .csv file will not have been found either. Therefor, we exit the script
        if(yearN > 9):
            print("NO .CSV FILES FOUND . . . EXITING")
            os._exit(99)
            
        
    # slice folder from beginning of found value to end of string    
    slicedFolder = folder[begin:]
    
    # .xlsx filename
    graphFile = slicedFolder+".xlsx"

    # create 'C:\Temp' file if it doesn't exist 
    # if not os.path.exists('C:\\Temp'):
    #         os.makedirs('C:\\Temp')

    # check if 'C:\Temp' directory exists
    # print('C:\Temp directory exists? ', os.path.isdir('C:\\Temp'))

    # concatenate network path to file
    xlsxFile = os.path.join(folder,graphFile)
    
    # concatenate local path to file
    # xlsxFileLocal = os.path.join('C:\\Temp\\',graphFile)
    
    # create a new Excel file in network folder
    workbook = xlsxwriter.Workbook(xlsxFile)
    print("Excel file will be created in \"{}\"".format(folder))
    
    # add and name worksheet
    worksheet = workbook.add_worksheet('Docking Graphs')

    # give the tab color
    worksheet.set_tab_color('green')

    # hide screen and printed gridlines
    worksheet.hide_gridlines(2)

    # passing selected folder to function
    plotInfDocking(folder)

    print("Please be patient! Large directories take a while to process.")

    # close files
    workbook.close()

    # open .xlsx file
    fd = open(xlsxFile,'r')
    
    # run Microsoft Excel and display .xlsx file
    os.startfile(xlsxFile)
    
    # close file
    fd.close()
    print("Script has ended")