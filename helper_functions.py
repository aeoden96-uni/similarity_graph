CONFIG_TXT = "config.txt"
ENCODING = "ISO-8859-1"


def mat_print(mat, fmt="g"):
    if mat is None:
        return
    col_maxes = [max([len(("{:" + fmt + "}").format(x)) for x in col])
                 for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:" + str(col_maxes[i]) + fmt + "}").format(y), end="  ")
        print("")


def write_new_pairs_to_file(filename, pairs):
    with open(filename, "w+") as w:
        for i, j in pairs:
            w.write(f'{i} {j}\n')


def write_new_index_file(filename, index):
    with open(filename, "w+") as w:
        for i in index:
            w.write(str(i) + "\n")


def _get_words_generator(file_path):
    with open(file_path, encoding=ENCODING) as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            yield line


def _get_pairs_generator(filename, skip_dimension=False):
    pairs = _get_words_generator(filename)

    dim = int(next(pairs))
    if not skip_dimension:
        yield dim

    for pair in pairs:
        try:
            i, j = pair.split()
        except ValueError:
            continue
        yield int(i), int(j)


def get_excluded_words():
    return list(_get_words_generator(CONFIG_TXT))
