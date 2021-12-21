def read_lines(file_path, encoding="ISO-8859-1"):
    with open(file_path, encoding=encoding) as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            yield line


def read_matrix_pairs(filename, is_matrix=True):
    pairs = read_lines(filename)
    if is_matrix:
        dim = int(next(pairs))
        yield dim

    for pair in pairs:
        try:
            i, j = pair.split()
        except ValueError:
            continue

        i = int(i)
        j = int(j)
        yield i, j


def write_new_pairs_to_file(filename, pairs):
    with open(filename, "w+") as w:
        for i, j in pairs:
            w.write(f'{i} {j}\n')


def write_new_index_file(filename, index):
    with open(filename, "w+") as w:
        for i in index:
            w.write(i)