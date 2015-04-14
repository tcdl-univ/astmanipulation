def unicode_to_file_data(contents, encoding=None):
    if not isinstance(contents, unicode):
        return contents
    if encoding is None:
        encoding = read_str_coding(contents)
    if encoding is not None:
        return contents.encode(encoding)
    try:
        return contents.encode()
    except UnicodeEncodeError:
        return contents.encode('utf-8')


def read_str_coding(source):
    try:
        first = source.index('\n') + 1
        second = source.index('\n', first) + 1
    except ValueError:
        second = len(source)
    return _find_coding(source[:second])


def _find_coding(text):
    coding = 'coding'
    try:
        start = text.index(coding) + len(coding)
        if text[start] not in '=:':
            return
        start += 1
        while start < len(text) and text[start].isspace():
            start += 1
        end = start
        while end < len(text):
            c = text[end]
            if not c.isalnum() and c not in '-_':
                break
            end += 1
        return text[start:end]
    except ValueError:
        pass