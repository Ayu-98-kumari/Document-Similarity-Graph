import numpy as np
import sys
from collections import defaultdict

def hash_bands_nonzero(minhash_array, bands, rows_per_band):
    hash_buckets = defaultdict(list)

    for file_idx in range(minhash_array.shape[1]):
        for band in range(bands):
            start_row = band * rows_per_band
            end_row = (band + 1) * rows_per_band
            band_values = minhash_array[start_row:end_row, file_idx]

            # Only consider the band if all values are non-zero
            if np.all(band_values != 0):
                band_hash = hash(tuple(band_values))
                hash_buckets[band_hash].append(file_idx)

    return hash_buckets

def group_similar_files_nonzero(hash_buckets):
    """ Find all groups of similar files from hash buckets """
    similar_groups = []
    for file_indices in hash_buckets.values():
        if len(file_indices) > 1:  # Only consider groups with more than one file
            similar_groups.append(file_indices)
    return similar_groups

def hash_bands_and_group(minhash_array, rows_per_band):
    bands = minhash_array.shape[0] // rows_per_band  # Number of bands

    hash_buckets = defaultdict(list)

    # Iterate over each band
    for file_idx in range(minhash_array.shape[1]):
        for band in range(bands):
            start_row = band * rows_per_band
            end_row = (band + 1) * rows_per_band
            band_values = minhash_array[start_row:end_row, file_idx]

            # Only hash the band if all values in the band are non-zero
            if np.all(band_values != 0):
                band_hash = hash(tuple(band_values))  # Hash the tuple of non-zero values
                hash_buckets[(band, band_hash)].append(file_idx)  # Group by band and hash

    similar_groups = group_similar_files_nonzero(hash_buckets)

    return similar_groups

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('\nUsage: python similarity_lsh.py minhash_file.npy rows_per_band\n')
        sys.exit(0)

    minhash_file = sys.argv[1]
    rows_per_band = int(sys.argv[2])

    minhash_array = np.load(minhash_file)

    # Hash the bands and group columns with similar non-zero values
    similar_groups = hash_bands_and_group(minhash_array, rows_per_band)

    # Output lists of column indices that are similar
    print("Groups of similar files (by column index):")
    for group in similar_groups:
        print(group)
