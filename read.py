def get_words_generator(file_path, encoding="ISO-8859-1"):
    with open(file_path, encoding=encoding) as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            yield line


def get_pairs_generator(filename, has_dimension=True):
    pairs = get_words_generator(filename)
    if has_dimension:
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