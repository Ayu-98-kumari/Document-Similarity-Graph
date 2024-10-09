import pickle
import numpy as np
import time
import sys
import os

sys.path.append("utils")

from cleanText import charfunc

def getBigArray(files, shinglesDict):
    
    HTSIZE = len(shinglesDict)
    bigArray = np.zeros((HTSIZE, len(files)), dtype='uint8')
    
    for i, file in zip(range(len(files)),files):
        col = charfunc(f'{PATH}/{file}', shinglesDict)
        bigArray[:,i] = col
       
    return bigArray
        
if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('\nUsage Command: python createBigArray.py Text_File_Path picklefile_path\n')
        print('1st argument: Path of all the Files eg: "~/Files"\n')
        print('2nd argument: Pickle file path including the file name eg: "~/shingles.pkl"\n')
        sys.exit(0)

    PATH = sys.argv[1]
    picklePath = sys.argv[2]

    with open(picklePath, 'rb') as f:
        shinglesDict = pickle.load(f)

    files = sorted(os.listdir(PATH))
       
    bigArray = getBigArray(files, shinglesDict)
#     print(bigArray)
    np.save('finalBigArray.npy', bigArray)
    print(bigArray)
    print('Numpy Array file has been saved with the name "bigArray.npy" in current directory')
    sys.exit(0)
    
    
    