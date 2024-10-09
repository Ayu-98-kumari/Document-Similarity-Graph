# Locality Sensitive Hashing (LSH) for Document Similarity

This project implements an end-to-end pipeline for identifying similar documents using **Locality Sensitive Hashing (LSH) Algorithm**. The pipeline includes:
1. **Shingle creation from text files.**
Shingles are a way to break a document into overlapping sequences of words (or characters), which helps compare the similarity between two documents. A shingle is a subset of contiguous tokens (words or characters) taken from a document. In this project, we use word-level shingles with K=3, meaning each shingle will consist of 3 consecutive words from the documents.

2. **MinHash Creation from the Shingle Dictionary**
MinHash is used to efficiently estimate the similarity between documents based on their shingles by creating compact signatures for each document. In this project, we utilize prime numbers to generate the hash functions for MinHash because prime numbers provide a natural source of randomness and ensure an even distribution of hash values. This approach avoids the computational expense and scalability issues associated with generating truly random numbers, especially when dealing with large datasets. By using prime numbers, we can create robust and distinct hash functions that minimize collisions, allowing the MinHash signatures to accurately reflect the similarities between different documents.

3. **Grouping of similar files using LSH in a graph data structure.**
4. **Accuracy evaluation by comparing predicted similar files to actual categories.**

## Project Files
- **createShingles.py**: Creates shingles from text files and stores them in a pickle file.
- **createBigArray.py**: Creates the big binary array where each column represents a document, and each row represents the presence or absence of a shingle.
- **createMinHashArray.py**: Creates the MinHash array based on the big binary array.
- **lsh_similarity_check.py**: Groups similar files based on MinHash values using LSH.
- **ConnectFiles.py**: Connects groups of similar files across different buckets using a graph-based approach.
- **check_accuracy.py**: Checks the accuracy of the LSH similarity predictions by comparing them to the true categories in a CSV file.

## Requirements
You need Python 3.x and the following libraries:
- `numpy`
- `pandas`
- `matplotlib` if you want to visualize the results.

Install the required libraries using:

```bash
pip install numpy
```
## Data information
Articles are present in ```Files.zip```. We mined these articles from RSS news feeds using Python's beautiful soup library and html parser (we can provide the mining code on demand). We mine a total of 1000 articles (100 articles per category) with at least 600 words in each article. Categories are as follows: ``` 'Crime', 'Education', 'Technology', 'Science', 'Bussiness', 'Food','Gasoline', 'Politics', 'RealState', 'Fashion'```

## Running the Pipeline
First, unzip the data Files.zip in your current directory. 
```bash
# 1. Create shingles
python3 createShingles.py ./Files/

# 2. Create the big array
python3 createBigArray.py ./Files/ ./shingles.pkl

# 3. Create the MinHash array
python3 createMinHashArray.py bigArray.npy

# 4. Find similar files using LSH
python3 lsh_similarity_check.py minhash.npy <rows_per_bucket> found_similar_files.txt

# 5. Connect similar files across buckets
python3 ConnectFiles.py found_similar_files.txt > found_connected_files.txt

# 6. Check accuracy of the predicted similarities
python3 check_accuracy.py article_labels.csv found_connected_files.txt
```


### Detailed Steps:

### 1. **Create Shingles**
First, generate shingles from all text files in the specified directory:

```bash
python3 createShingles.py <path_to_text_files>
```

This will create a `shingles.pkl` file containing the shingle dictionary.

### 2. **Create Big Array**
Create the big binary array from the generated shingle dictionary and text files:

```bash
python3 createBigArray.py <path_to_text_files> <path_to_shingles.pkl>
```

This will create a `bigArray.npy` file, which is a large binary matrix representing the presence of shingles in each file.

### 3. **Create MinHash Array**
Create the MinHash array using the big array:

```bash
python3 createMinHashArray.py bigArray.npy
```

This will create a `minhash.npy` file, which is the MinHash signature for each file.

### 4. **Find Similar Files Using LSH**
Run the LSH algorithm to group similar files based on their MinHash signatures:

```bash
python3 lsh_similarity_check.py minhash.npy <rows_per_band>
```

For example:

```bash
python3 lsh_similarity_check.py minhash.npy 2
```

This will print the groups of files that are similar based on their MinHash values.

### 5. **Connect Files Across Buckets**
After grouping files using LSH, use the graph-based approach to connect files found in different buckets:

```bash
python3 ConnectFiles.py found_similar_files.txt > found_connected_files.txt
```

This will output a list of connected groups of files in `found_connected_files.txt`.

### 6. **Check Accuracy of the Predicted Similarities**
You can now check the accuracy of the LSH predictions by comparing them to actual categories provided in a CSV file (`article_labels.csv`).

The CSV file should have the following columns:
- `Category`: The category of the article.
- `FileNumber`: The file number (e.g., `file0001`, `file0002`).

To check the accuracy:

```bash
python3 check_accuracy.py article_labels.csv found_connected_files.txt
```

This will print the accuracy percentage, as well as the number of correct and incorrect classifications.

---

