import numpy as np
import sys

# Experimented with 24, 48, 84, 120, 240. (120 gives the best Accuracy)
nRows = 200 # No. of Rows that I want in minhash array.
filterSize = 1 # The significant number that I found based on the file similarity accuracy.

def getprimes(N):
    mask = [0]*N
    plist = []
    for p in range(3,N,2):
        if mask[p] != 0:
            continue
        plist.append(p)
        for x in range(p,N,2*p):
            mask[x] = 1
    return plist

def getMinhashArray(rows):
	minhash = np.zeros((nRows,bigArray.shape[1]), dtype='uint')
	for i in range(nRows):
		i_minhash = np.zeros(bigArray.shape[1], dtype='uint')
		j=1
		for row in rows[i]: 
			allOnesIndex = np.where(bigArray[row] == 1)[0]
			# print(allOnesIndex)
			for ones in allOnesIndex: 
				if i_minhash[ones] == 0:
					i_minhash[ones] = j
				else:
					continue
			j+=1
			# print(i_minhash)
			# input('?')
			minhash[i] = i_minhash
	return minhash


if __name__ =='__main__':

	if len(sys.argv) != 2:
		print('This Program take the path of bigArray as 1st cmd line argument.')
		print('\nUsage eg: python3 createMinHashArray.py bigArray.npy\n')
		sys.exit(0)

	bigArrayPath = sys.argv[1]
	bigArray = np.load(bigArrayPath)
	# Getting all rows whose sum is from then filterSize.
	bigArray = bigArray[np.sum(bigArray, axis = 1)>filterSize]
	#Getting 120 random primes between 95000 - 100000.
	primes = np.random.choice(getprimes(100000)[-5000:], nRows)
	# Creating HashFunctions

	hashFunction = lambda prime, randomRow, bignRows: lambda x: (prime * x + randomRow) % bignRows
	randomRowList = np.random.randint(0, bigArray.shape[0], nRows)
	hashFuncList = [hashFunction(primes[i], randomRowList[i], bigArray.shape[0]) for i in range(nRows)]
	rows = np.array([[f(x) for f in hashFuncList] for x in range(nRows)])
	minhash = getMinhashArray(rows)

	np.save('minhash.npy', minhash)

	print('Min Hash array has been saved in the current directory with name "minhash.npy"')
	sys.exit(0)
