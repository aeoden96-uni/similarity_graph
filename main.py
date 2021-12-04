import numpy as np


def find_word_id(word):
    with open("examples/e00/index.txt",encoding= "ISO-8859-1") as f:
        lines = f.readlines()

        for i,line in enumerate(lines):
            if word.rstrip() == line.rstrip():
                return i+1

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
    past = X.copy()
    if limit < 1: raise ValueError

    for i in range(50):
        i += 1
        left_hand = B.dot(X).dot(A.transpose())
        right_hand = B.transpose().dot(X).dot(A)
        X = left_hand + right_hand
        norm = np.linalg.norm(X, 'fro')
        X = X / norm

        # print(i, np.around(X, 4)[0][0])
        if i % 2 == 0:
            if np.allclose(past, X, rtol=1e-05):
                return np.around(X, 4)
            past = X.copy()



def main():
    example = input("Example (etc 'e01'): ")

    if example == "e00":
        id = find_word_id(input("Word: "))
        #print("ID",id)
        print("Word OK")


        # id = 87802

        dim, index, pairs = load_for_word("examples/" + example + "/dico.txt",
                                          id)

        # print(pairs)

        A = load_matrix(dim, pairs)
        B = load_matrix_from_file("examples/e00/B.txt")

        # print("Korijen sume kvadrata elemenata", np.sqrt(np.sum(np.square(p))))
        p = inter(41, A, B)[1]

        results = []

        keywords = ["the" , "or" ,"a" , "in" , "to" , "of" ,"which",
                    "and","as","with", "for","any","it","by", "is","are","than",
                    "an", "from","into", "be"]

        for i,l in enumerate(p):
            results.append((l, index[i]))

        results.sort(key=lambda x: x[0])

        max = 10
        for i,k in results[::-1]:
            if k.rstrip() in keywords:
                continue
            if max <= 0:
                break
            print(i,k, end="")
            max -=1


    else:


        A = load_matrix_from_file("examples/" + example + "/A.txt")
        # print(A)
        B = load_matrix_from_file("examples/" + example + "/B.txt")

        p = inter(1,A,B)

        print(p)
        # print("Korijen sume kvadrata elemenata", np.sqrt(np.sum(np.square(p))))





if __name__ == '__main__':
    main()
