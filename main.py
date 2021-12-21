import numpy as np
from helper_functions import mat_print
from read import get_words_generator, get_pairs_generator

DICT_TXT = "examples/e00/dico.txt"

INDEX_TXT = "examples/e00/index.txt"


def find_word_id(user_word):
    words = get_words_generator("examples/e00/index.txt", "ISO-8859-1")
    for i, word in enumerate(words):
        if word == user_word.rstrip():
            return i + 1
    return -1


# create_matrix_from_pairs_gen
def load_matrix(dim, pairs_gen):
    matrix = np.zeros((dim, dim))
    for i, j in pairs_gen:
        matrix[i - 1][j - 1] = 1
    return matrix


def load_matrix_from_file(filename, pairs_gen=None):
    if pairs_gen is None:
        pairs_gen = get_pairs_generator(filename)
    dim = next(pairs_gen)
    return load_matrix(dim, pairs_gen)


def create_set_from_word_id(word_id):
    pairs_gen = get_pairs_generator(DICT_TXT, has_dimension=True)
    dim = next(pairs_gen)
    uniq = set()
    for i, j in pairs_gen:
        i = int(i)
        j = int(j)

        if word_id == i:
            uniq.add(j)
        if word_id == j:
            uniq.add(i)

    return uniq


def select_pairs(file_name, word_set):
    pairs_gen = get_pairs_generator(DICT_TXT, has_dimension=True)
    dim = next(pairs_gen)

    pairs = [(i, j) for (i, j) in pairs_gen
             if i in word_set and j in word_set]

    return pairs


def create_new_pairs(mapping, pairs):
    new_pairs = [(mapping.index(i) + 1, mapping.index(j) + 1)
                 for (i, j) in pairs]
    return new_pairs


def create_new_index(mapping):
    words = get_words_generator(INDEX_TXT)
    index = [""] * len(mapping)
    for i, word in enumerate(words):
        if i + 1 in mapping:
            index[mapping.index(i+1)] = word
    return index


def generate_new_index_and_mapping(word_id):
    word_set = create_set_from_word_id(word_id)

    mapping = list(word_set)

    # selected pairs
    selected_pairs = select_pairs(DICT_TXT, word_set)

    new_pairs = create_new_pairs(mapping, selected_pairs)
    new_index = create_new_index(mapping)

    # write_new_pairs_to_file("new" + str(word_id) + ".txt", new_pairs)
    # write_new_index_file("new" + str(word_id) + "words.txt", mapping)

    return len(word_set), new_index, new_pairs


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
    words = get_words_generator("config.txt")
    return [i for i in words]


def run_main_example(word_id, debug=False):
    dim, index, pairs = generate_new_index_and_mapping(word_id)

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
        print(i, k)
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
