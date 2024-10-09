import csv
import sys

def read_labels(csv_file_path):
    labels = {}
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Adjust the file number (as file0001 corresponds to column 0 in the minhash array)
            file_number = int(row['FileNumber']) - 1  # Shift index
            labels[file_number] = row['Category']
    return labels

def read_connected_files(file_path):
    connected_groups = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('['):  # Only consider lines that start with '['
                group = list(map(int, line.strip()[1:-1].split(',')))  # Convert to list of integers
                connected_groups.append(group)
    return connected_groups

def compute_accuracy(connected_groups, labels):
    correct_counter = 0
    wrong_counter = 0

    for group in connected_groups:
        main_node = group[0] 
        main_category = labels.get(main_node, None)

        if main_category is None:
            print(f"Warning: No category found for file {main_node + 1}")
            continue

        # Compare the category of each other file in the group to the main node
        for file_index in group[1:]:
            file_category = labels.get(file_index, None)
            if file_category is None:
                print(f"Warning: No category found for file {file_index + 1}")
                continue

            if file_category == main_category:
                correct_counter += 1
            else:
                wrong_counter += 1

    total = correct_counter + wrong_counter
    accuracy = (correct_counter / total) * 100 if total > 0 else 0
    return accuracy, correct_counter, wrong_counter

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('\nUsage: python accuracy_check.py article_labels.csv found_connected_files.txt\n')
        sys.exit(0)

    csv_file_path = sys.argv[1]
    connected_file_path = sys.argv[2]
    labels = read_labels(csv_file_path)

    connected_groups = read_connected_files(connected_file_path)
    accuracy, correct_counter, wrong_counter = compute_accuracy(connected_groups, labels)

    print(f"Correct classifications: {correct_counter}")
    print(f"Wrong classifications: {wrong_counter}")
    print(f"Accuracy: {accuracy:.2f}%")
