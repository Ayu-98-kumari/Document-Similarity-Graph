import sys
import re
import pickle
import os

# This Script will read all the Text files from the Files Directory, clean it and create a .pkl files of unique shingles in current directory.

def read_clean(file):
    art = open(f'{PATH}/{file}','r').read().lower()

    art = re.sub(r'[©0-9\*\$\\%?\-\'“”",#\.+:.]', " ", art, flags=re.MULTILINE)
    art = re.sub(r"click here|www|com|html|javasript|\t|cp|file|http|https|jpg|png|technewsworld|jpghttps", " ", art)
    art = re.sub(r'^\<.*\>$', ' ', art,  flags=re.MULTILINE)
    art = art.replace('\n',' ')

    art = re.split(r'\W+', art)

    return art[:-1]

def getWordShingles(file, K=3):
    
    shingleList = []
    artWords = read_clean(file)
    for i in range(len(artWords)-2):
        shingleList.append(tuple(artWords[i:i+K]))
    
    return shingleList


def getShingleDict(files):
    shingleDict = {}
    for file in files:
        shingleList = getWordShingles(f'{file}', 3)

        for shingle in shingleList:
            if shingle not in shingleDict: shingleDict[shingle] = 1
            else: shingleDict[shingle] += 1
    return shingleDict

if __name__ == '__main__':


    if len(sys.argv) != 2:
        print('\nUsage Command: python3 createShingles.py path_to_all_text_files')
        sys.exit(0)

    PATH = sys.argv[1]

    files = os.listdir(PATH)
    shingleDict = getShingleDict(files)

    finalDict = {key: value for key, value in shingleDict.items() if value > 1}
    finalDict = {key: i for i, key in enumerate(finalDict.keys())}
    # print(finalDict)
    dictFile = open('shingles.pkl','wb')
    pickle.dump(finalDict, dictFile)
    dictFile.close()


