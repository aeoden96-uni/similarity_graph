import numpy as np

from helper_functions import mat_print
from read import read_lines, read_matrix_pairs


def find_word_id(user_word):
    words = read_lines("examples/e00/index.txt", "ISO-8859-1")
    for i, word in enumerate(words):
        if word == user_word.rstrip():
            return i + 1
    return -1

#create_matrix_from_pairs_gen
def load_matrix(dim, pairs_gen):
    matrix = np.zeros((dim, dim))
    for i, j in pairs_gen:
        matrix[i - 1][j - 1] = 1
    return matrix


def load_matrix_from_file(filename, pairs_gen=None):
    if pairs_gen is None:
        pairs_gen = read_matrix_pairs(filename)
    dim = next(pairs_gen)
    # pairs = [i for i in pairs_gen]
    return load_matrix(dim, pairs_gen)


def create_set_from_word_id(file_name, word_id):
    pairs = read_matrix_pairs(file_name,is_matrix=False)
    uniq = set()
    for i, j in pairs:
        # try:
        #     i, j = line.split()
        # except ValueError:
        #     continue
        i = int(i)
        j = int(j)

        if word_id == i:
            uniq.add(j)
        if word_id == j:
            uniq.add(i)

    return uniq


def create_pairs_from_set(file_name, word_set):
    pairs = []
    pairs_gen = read_matrix_pairs(file_name,is_matrix=False)

    for i, j in pairs_gen:

        if i in word_set and j in word_set:
            pairs.append((i, j))
    return pairs


def create_new_pairs(mapping, pairs):
    new_pairs = []
    for i, j in pairs:
        new_pairs.append(
            (mapping.index(i) + 1, mapping.index(j) + 1))
    return new_pairs


def create_mapping(word_set):
    return [i for i in word_set]


def create_new_index(mapping):
    with open("examples/e00/index.txt", encoding="ISO-8859-1") as f:
        lines = f.readlines()
        index = [""] * len(mapping)
        for i, line in enumerate(lines):
            ind = i + 1
            if ind in mapping:
                index[mapping.index(ind)] = line

        return index


def generate_new_index_and_mapping(ime_dat, word_id):

    s = create_set_from_word_id(ime_dat, word_id)
    pairs = create_pairs_from_set(ime_dat, s)

    mapping = create_mapping(s)
    new_pairs = create_new_pairs(mapping, pairs)

    new_index = create_new_index(mapping)

    # write_new_pairs_to_file("new" + str(word_id) + ".txt", new_pairs)
    # write_new_index_file("new" + str(word_id) + "words.txt", mapping)

    return len(s), new_index, new_pairs


def calculate(matrix_a, matrix_b):
    x = np.ones((matrix_b.shape[0], matrix_a.shape[0]))
    past = x.copy()

    for i in range(50):
        i += 1
        left_hand = matrix_b.dot(x).dot(matrix_a.transpose())
        right_hand = matrix_b.transpose().dot(x).dot(matrix_a)
        x = left_hand + right_hand
        norm = np.linalg.norm(x, 'fro')
        x = x / norm


        if i % 2 == 0:
            if np.allclose(past, x, rtol=1e-05):
                return np.around(x, 4)
            past = x.copy()


def get_excluded_words():
    exception_list = []
    with open("config.txt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            exception_list.append(line)
    return exception_list


def run_main_example(word_id, debug=False):
    dim, index, pairs = generate_new_index_and_mapping("examples/e00/dico.txt",
                                                       word_id)

    if debug:
        print("Pairs", pairs)

    matrix_first = load_matrix(dim, pairs)
    matrix_second = load_matrix_from_file("examples/e00/B.txt")

    p = calculate(matrix_first, matrix_second)[1]

    if debug:
        print("Root of sum of squares", np.sqrt(np.sum(np.square(p))))

    results = []
    keywords = get_excluded_words()

    if debug:
        print("keywords", keywords)

    for i, l in enumerate(p):
        results.append((l, index[i]))

    results.sort(key=lambda x: x[0])

    top_results = 10
    for i, k in results[::-1]:
        if k.rstrip() in keywords:
            continue
        if top_results <= 0:
            break
        print(i, k, end="")
        top_results -= 1


def run_mini_example(example, debug=False):
    matrix_first = load_matrix_from_file(
        "examples/" + example + "/A.txt")
    if debug:
        mat_print(matrix_first)

    matrix_second = load_matrix_from_file(
        "examples/" + example + "/B.txt")

    p = calculate(matrix_first, matrix_second)

    mat_print(p)
    if debug and p is not None:
        print("Root of sum of squares", np.sqrt(np.sum(np.square(p))))


def main():
    while True:
        example = input("Example (dict,e01,e02... 0 to exit): ")
        if example == "0":
            return
        if example == "dict":
            while True:
                new_word = input("Word (0 to exit): ")

                if new_word == "0":
                    break

                word_id = find_word_id(new_word)

                if word_id == -1:
                    print("Word not OK...exiting")
                    return
                print("Word OK")

                run_main_example(word_id)

                print()

        else:
            run_mini_example(example)
        print()


if __name__ == '__main__':
    main()
    input("Press to exit")
