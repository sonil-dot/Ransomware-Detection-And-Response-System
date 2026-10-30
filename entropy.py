
import math
from collections import Counter


def calculate_entropy(file_path):
    with open(file_path, "rb") as file:
        data = file.read()

    if not data:
        return 0.0

    frequencies = Counter(data)
    file_size = len(data)

    entropy = 0.0

    for count in frequencies.values():
        probability = count / file_size
        entropy -= probability * math.log2(probability)

    return entropy


if __name__ == "__main__":
    file_path = "./test_data/gold2.txt"
    result = calculate_entropy(file_path)
    print(f"File entropy: {result:.2f} bits per byte")
