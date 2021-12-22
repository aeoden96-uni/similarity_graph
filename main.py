import numpy as np
from helper_functions import mat_print, get_excluded_words
from read import \
    load_matrix_from_file, \
    find_word_id, \
    new_index_and_mapping


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

            if np.allclose(past, x, atol=1e-05):
                return np.around(x, 4)
            past = x.copy()


def print_results(scores, top_results, index):
    keywords = get_excluded_words()

    results = [(score, index[i]) for i, score in enumerate(scores)]
    results.sort(key=lambda x: -x[0])

    results = [(i, k)
               for i, k in results
               if k not in keywords][:top_results]

    [print(i, k) for i, k in results]


def run_main_example(word_id, debug=True):
    matrix_first, pairs, index = new_index_and_mapping(word_id)
    matrix_second = load_matrix_from_file("examples/e00/B.txt")

    p = calculate(matrix_first, matrix_second)[1]

    if debug:
        print("Root of sum of squares", np.sqrt(np.sum(np.square(p))))

    print_results(p, 10, index)


def run_mini_example(example, debug=False):
    matrix_first = load_matrix_from_file(
        "examples/" + example + "/A.txt")
    if debug:
        mat_print(matrix_first)

    matrix_second = load_matrix_from_file(
        "examples/" + example + "/B.txt")

    print("A:")
    mat_print(matrix_first)
    print("B:")
    mat_print(matrix_second)

    p = calculate(matrix_first, matrix_second)

    print("\nResult:")
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
                new_word = input("Word (0 to exit): ").rstrip()

                if new_word == "0":
                    break

                try:
                    word_id = find_word_id(new_word)
                except ValueError:
                    print("Word not found in dictionary")
                    continue

                print("Word OK")

                run_main_example(word_id)

                print()

        elif example in ["e0" + str(i + 1) for i in range(9)]:
            try:
                run_mini_example(example)
            except FileNotFoundError:
                print(f"No example named {example}.")
        print()


if __name__ == '__main__':
    main()
