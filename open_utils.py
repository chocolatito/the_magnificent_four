
def content_reader(path, in_lines=False):
    with open(path, 'r') as fh:
        if in_lines:
            return [line for line in fh.readlines()]
        return fh.read()


def content_writer(path, content, mode='w'):
    with open(path, mode) as fh:
        fh.write(content)


# ___________________________
