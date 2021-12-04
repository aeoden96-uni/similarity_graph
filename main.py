import numpy as np
import pandas as pd


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
            matrix[i-1][j-1] = 1
    return matrix



def create_set_form_lines(lines, id):
    uniq = set()
    for line in lines:
        try:
            i, j = line.split()
        except:
            continue
        i = int(i)
        j = int(j)

        if id == i :
            uniq.add(j)
        if  id == j:
            uniq.add(i)

    print("set", len(uniq))
    return uniq


def create_pairs_from_set(lines, S):
    pairs = []

    for line in lines:
        try:
            i, j = line.split()
        except:
            continue
        i = int(i)
        j = int(j)
        if i in S and j in S:
            pairs.append((i, j))
    return pairs


def create_new_pairs(mapping, pairs):
    new_pairs = []
    for i, j in pairs:
        new_pairs.append(
            (mapping.index(i) + 1, mapping.index(j) + 1))
    return new_pairs


def create_mapping(S):
    mapping = []
    for u in S:
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


def load_for_word(ime_dat, rijec_id):
    with open(ime_dat) as f:
        lines = f.readlines()
        s = create_set_form_lines(lines, rijec_id)

        pairs = create_pairs_from_set(lines, s)

    mapping = create_mapping(s)
    new_pairs = create_new_pairs(mapping, pairs)

    new_index = create_new_index(mapping)

    # write_new_pairs_to_file("novi" + str(rijec_id) + ".txt", new_pairs)
    # write_new_index_file("novi" + str(rijec_id) + "rijeci.txt", mapping)

    return len(s), new_index, new_pairs


def inter(limit, A, B):
    X = np.ones((B.shape[0], A.shape[0]))
    if (limit < 1): raise ValueError
    # X = np.ones((5, 3))
    for i in range(limit):
        i = B.dot(X).dot(A.transpose())
        j = B.transpose().dot(X).dot(A)
        X = i + j
        norm = np.linalg.norm(X, 'fro')
        X = X / norm

    return np.around(X, 4)


def main():
    example = input("Koji primjer:(npr e01) ")

    if example == "e00":
        # id = int(input("Id rijeci: "))
        id = 87802

        dim, index, pairs = load_for_word("examples/" + example + "/dico.txt",
                                          id)

        print(pairs)

        A = load_matrix(dim, pairs)
        B = load_matrix_from_file("B.txt")

        # print("Korijen sume kvadrata elemenata", np.sqrt(np.sum(np.square(p))))
        p = inter(40, A, B)[1]

        results = []

        keywords = ["the" , "or" ,"a" , "in" , "to" , "of" ,"which",
                    "and","as","with", "for","any","it"]

        for i,l in enumerate(p):
            results.append((l, index[i]))

        results.sort(key=lambda x: x[0])

        for i,k in results[::-1]:
            if k.rstrip() in keywords:
                continue
            print(i,k)


    else:
        itt = int(input("Broj iteracija: "))

        A = load_matrix_from_file("examples/" + example + "/A.txt")
        # print(A)
        B = load_matrix_from_file("examples/" + example + "/B.txt")

        p = inter(itt,A,B)

        print(p)
        print("Korijen sume kvadrata elemenata", np.sqrt(np.sum(np.square(p))))





if __name__ == '__main__':
    main()
