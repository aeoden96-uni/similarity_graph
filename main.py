import numpy as np


def find_word_id(word):
    with open("examples/e00/index.txt", encoding="ISO-8859-1") as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if word.rstrip() == line.rstrip():
                return i + 1

        raise EOFError


def load_matrix_from_file(filename):
    with open(filename) as f:
        pairs = []
        dim = int(f.readline())
        lines = f.readlines()
        for line in lines:
            i, j = line.split()
            i = int(i)
            j = int(j)
            pairs.append((i, j))
    return load_matrix(dim, pairs)


def load_matrix(dim, pairs):
    matrix = np.zeros((dim, dim))
    for i, j in pairs:
        matrix[i - 1][j - 1] = 1
    return matrix


def create_set_form_lines(lines, word_id):
    uniq = set()
    for line in lines:
        try:
            i, j = line.split()
        except ValueError:
            continue
        i = int(i)
        j = int(j)

        if word_id == i:
            uniq.add(j)
        if word_id == j:
            uniq.add(i)

    return uniq


def create_pairs_from_set(lines, word_set):
    pairs = []

    for line in lines:
        try:
            i, j = line.split()
        except ValueError:
            continue
        i = int(i)
        j = int(j)
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
    mapping = []
    for u in word_set:
        mapping.append(u)
    return mapping


def write_new_pairs_to_file(filename, pairs):
    with open(filename, "w+") as w:
        for i, j in pairs:
            w.write(f'{i} {j}\n')


def create_new_index(mapping):
    with open("examples/e00/index.txt", encoding="ISO-8859-1") as f:
        lines = f.readlines()
        index = [""] * len(mapping)
        for i, line in enumerate(lines):
            ind = i + 1
            if ind in mapping:
                index[mapping.index(ind)] = line

        return index


def write_new_index_file(filename, index):
    with open(filename, "w+") as w:
        for i in index:
            w.write(i)


def load_for_word(ime_dat, word_id):
    with open(ime_dat) as f:
        lines = f.readlines()
        s = create_set_form_lines(lines, word_id)

        pairs = create_pairs_from_set(lines, s)

    mapping = create_mapping(s)
    new_pairs = create_new_pairs(mapping, pairs)

    new_index = create_new_index(mapping)

    # write_new_pairs_to_file("new" + str(word_id) + ".txt", new_pairs)
    # write_new_index_file("new" + str(word_id) + "words.txt", mapping)

    return len(s), new_index, new_pairs


def calculate(limit, matrix_a, matrix_b):
    x = np.ones((matrix_b.shape[0], matrix_a.shape[0]))
    past = x.copy()
    if limit < 1:
        raise ValueError

    for i in range(50):
        i += 1
        left_hand = matrix_b.dot(x).dot(matrix_a.transpose())
        right_hand = matrix_b.transpose().dot(x).dot(matrix_a)
        x = left_hand + right_hand
        norm = np.linalg.norm(x, 'fro')
        x = x / norm

        # print(i, np.around(x, 4)[0][0])
        if i % 2 == 0:
            if np.allclose(past, x, rtol=1e-05):
                return np.around(x, 4)
            past = x.copy()


def main():
    example = input("Example (etc 'e01'): ")

    if example == "e00":
        word_id = find_word_id(input("Word: "))
        print("Word OK")

        dim, index, pairs = load_for_word("examples/" + example + "/dico.txt",
                                          word_id)

        # print(pairs)

        matrix_first = load_matrix(dim, pairs)
        matrix_second = load_matrix_from_file("examples/e00/B.txt")

        # print("Root of sum of squares", np.sqrt(np.sum(np.square(p))))
        p = calculate(41, matrix_first, matrix_second)[1]

        results = []

        keywords = ["the",
                    "or",
                    "a",
                    "in",
                    "to",
                    "of",
                    "which",
                    "and",
                    "as",
                    "with",
                    "for",
                    "any",
                    "it",
                    "by",
                    "is",
                    "are",
                    "than",
                    "an",
                    "from",
                    "into",
                    "be"]

        for i, l in enumerate(p):
            results.append((l, index[i]))

        results.sort(key=lambda x: x[0])

        max_iter = 10
        for i, k in results[::-1]:
            if k.rstrip() in keywords:
                continue
            if max_iter <= 0:
                break
            print(i, k, end="")
            max_iter -= 1

    else:

        matrix_first = load_matrix_from_file(
            "examples/" + example + "/matrix_first.txt")
        # print(matrix_first)
        matrix_second = load_matrix_from_file(
            "examples/" + example + "/matrix_second.txt")

        p = calculate(1, matrix_first, matrix_second)

        print(p)
        # print("Root of sum of squares", np.sqrt(np.sum(np.square(p))))


if __name__ == '__main__':
    main()
