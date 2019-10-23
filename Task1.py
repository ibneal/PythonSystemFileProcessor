#Created by NEAL BHALODIA
import pandas as pd
import shutil, os
import imghdr
from datetime import datetime
from PIL import Image
import filecmp

#NOTE TO USE THIS PROGRAM YOU MUST EDIT THE
#PATH OF THE REPO FILES,THE COPY PATH, and the data.CSV file
#CHANGE IT TO WHERE YOUR REPO FOLDER IS LOCATED
#AND WHERE YOU WANT TO OUTPUT THE extractedFiles


def get_num_pixels(filepath):
    # function to check number of pixels
    width, height = Image.open(filepath).size
    return width*height


def compare_files(fileone, filetwo):
    #function to check if two files are the same
    filecmp.cmp(fileone, filetwo)


def get_pg(textfile):
    #function to get page numbers
    file = open(textfile, 'r')
    text = file.readline()
    store = text.find('[Pg ')
    unedited = text[store:store+8]
    while unedited[-1:] != ']':
        unedited = unedited[:-1]
    file.close()
    return unedited


df = (pd.read_csv("data.csv"))
rdf = pd.DataFrame(columns=['Repository Path', 'Copy Path', 'Corrected File Path', 'Duplicate Files',
                            'File Size', 'Date of File Creation', 'Line/Pixel Count', 'Page Number'])

holdrepo = [] #holds the respositroy path
for repo in df['repository path']:
    holdrepo.append(repo)
holdcopy = [] #holds the copy path
for copyp in df['copy path']:
    holdcopy.append(copyp)

newpath = "/Users/nealbhalodia/PycharmProjects/PythonSystemFileProcessor/extractedFiles"
for index in range(len(holdcopy)):
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    repo = '/Users/nealbhalodia/PycharmProjects/PythonSystemFileProcessor' + holdrepo[index][1:]
    cpath = '/Users/nealbhalodia/PycharmProjects/PythonSystemFileProcessor' + holdcopy[index][1:]
    output = imghdr.what('/Users/nealbhalodia/PycharmProjects/PythonSystemFileProcessor/repository/0/642/270/400/534/238/443')
    if (imghdr.what(repo)) == 'jpeg': #checks if the file is a jpeg
        newcpath = cpath[:-3] + 'jpg' #if it is then it is copied to the copy path with a .jpg extension
        shutil.copy(repo, newcpath) #copies the file to the copy path
        created = (datetime.fromtimestamp(os.stat(repo).st_ctime)) #storing creation date of file
        rdf.loc[index] = [holdrepo[index], holdcopy[index], holdcopy[index][:-3]+'jpg', '', os.path.getsize(newcpath), created, get_num_pixels(newcpath), '']
        #inserting a entry into the results CSV file
    else:
        newcpath = cpath[:-3] + 'txt' #if it is a .txt file it will copy to the copy path with a .txt extension
        shutil.copy(repo, newcpath) #copies the file to the copy path
        created = (datetime.fromtimestamp(os.stat(repo).st_ctime)) #storing creation date of file
        with open(newcpath) as f: #checking the number of lines in the txt file
            line_count = 0
            for line in f:
                line_count += 1
        rdf.loc[index] = [holdrepo[index], holdcopy[index], holdcopy[index][:-3]+'txt', '', os.path.getsize(newcpath), created, line_count, get_pg(newcpath)]
        #inserting a entry into the results CSV file

#creates the result CSV file from the pandas dataframe
rdf.to_csv('result.csv')
