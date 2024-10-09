import pickle
import numpy as np
import re
import sys
    
def charfunc(filename, shinglesDict):

    if type(list(shinglesDict.keys())[0]) is not tuple:
        print('\nWrong dictionary format')
        print('Dictionary key should be a tuple eg: ("word1","word2","word3")\n')
        sys.exit(0)


    else:
        art = open(filename,'r').read().lower()
        art = re.sub(r'[©0-9\*\$\\%?\-\'“”",#\.\<\>+:.]', " ", art, flags=re.MULTILINE)
        art = re.sub(r"click here|www|com|html|javascript|\t|cp|file|http|https|jpg|png|technewsworld|jpghttps", "", art)
        art = re.sub(r'^\<.*\>$', ' ', art,  flags=re.MULTILINE)
        art = art.replace('\n',' ')

        artWords = re.split(r'\W+', art)

        HTSIZE = len(shinglesDict)
        hTable = np.zeros(HTSIZE, dtype='uint8')

        for i in range(len(artWords) -2):
            shingle = tuple(artWords[i:i+3])
            if shingle in shinglesDict:
                index = shinglesDict[shingle]
                hTable[index] = 1

        return hTable

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('\nUsage Command: python nov29.py filesPath picklefile(fullpath)\n')
        print('1st argument: Path of the File you want to read eg:"~/Files/filexxxx.txt"\n')
        print('2nd argument: Pickle file path including the file name eg: "~/file_name.pkl"\n')
        sys.exit(0)

    filename = sys.argv[1]
    picklePath = sys.argv[2]

    with open(picklePath, 'rb') as f:
        shinglesDict = pickle.load(f)
    
    HTSIZE = len(shinglesDict)

    hTable = charfunc(filename, shinglesDict)
    print(hTable)
    