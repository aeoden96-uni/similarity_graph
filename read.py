import numpy as np
from helper_functions import _get_words_generator, _get_pairs_generator

DICT_TXT = "examples/e00/dico.txt"
INDEX_TXT = "examples/e00/index.txt"


def find_word_id(user_word):
    words = list(_get_words_generator(INDEX_TXT))
    return words.index(user_word) + 1


def create_set(word_id):
    # word_id    j     --> add j
    #    i    word_id  --> add i

    pairs_gen = _get_pairs_generator(DICT_TXT, skip_dimension=True)

    uniq = set()

    [uniq.add(i) if word_id == j else uniq.add(j)
     for i, j in pairs_gen
     if word_id in [i, j]]

    return uniq


def create_mapping(index_set):
    return list(index_set)


def select_pairs(index_set):
    pairs_gen = _get_pairs_generator(DICT_TXT, skip_dimension=True)

    pairs = [(i, j) for (i, j) in pairs_gen
             if i in index_set and j in index_set]

    return pairs


def create_new_index(mapping):
    old_index = list(_get_words_generator(INDEX_TXT))
    return [old_index[i - 1] for i in mapping]


def create_new_pairs(mapping, pairs):
    new_pairs = [(mapping.index(i) + 1, mapping.index(j) + 1)
                 for (i, j) in pairs]
    return new_pairs


def new_index_and_mapping(word_id):
    index_set = create_set(word_id)
    mapping = create_mapping(index_set)

    selected_pairs = select_pairs(index_set)

    new_pairs = create_new_pairs(mapping, selected_pairs)
    new_index = create_new_index(mapping)

    return load_matrix(len(index_set), new_pairs), new_pairs, new_index


def load_matrix(dim, pairs_gen):
    matrix = np.zeros((dim, dim))
    for i, j in pairs_gen:
        matrix[i - 1][j - 1] = 1
    return matrix


def load_matrix_from_file(filename):
    pairs_gen = _get_pairs_generator(filename, skip_dimension=False)

    return load_matrix(next(pairs_gen), pairs_gen)
