import typing as tp

class DB:
    def __init__(self):
        return

def parse(f):
    KEYWORD = "KEYWORD"
    for line in f:
        if '@' in line and '.' in line:
            # do something
            pass
    return DB()

def output(db, filename: tp.AnyStr = "output.txt") -> None:
    with open(filename, 'w') as f:
        f.write('readme')
    return




if __name__ == "__main__":
    filename = 'text.txt'
    with open(filename, 'r') as f:
        db = parse(f)
    output(db)