import datetime
import typing as tp


def month_to_num(month: str) -> str:
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    if month not in months:
        return month
    ret = str(months.index(month) + 1)
    if len(ret) == 1:
        return "0" + ret
    return ret


def clean_line(s: str) -> str:
    if "--" in s:
        return s.split("--")[0]
    return s


flatten = []


def clean_doc(filename: str):
    global flatten
    with open(filename) as f:
        for line in f.readlines():
            for tok in clean_line(line).split():
                flatten.append(month_to_num(tok))


class DataBase:
    items: tp.List[str]
    ident: int

    def __init__(self, id: int, items: tp.List[str]):
        self.ident = id
        self.items = items

    def __str__(self) -> str:
        return f"{self.ident}: {self.items}"


def filtered(s: str) -> str:
    ret = ""
    for i in s:
        if i != "'":
            ret += i
    return ret


def to_list(l: tp.List[DataBase]) -> tp.List[DataBase]:
    m: tp.Dict[int, tp.List[str]] = {}
    for elem in l:
        if elem.ident in m.keys():
            for item in elem.items:
                m[elem.ident].append(item)
        else:
            m.update({elem.ident: elem.items})

    ret = []
    for k in m.keys():
        ret.append(DataBase(k, m[k]))
    return ret


def output(filename):
    global result_str
    with open(filename, "wt") as f:
        f.write(result_str)


if __name__ == "__main__":

    clean_doc("text.txt")

    result = []
    result_d: tp.Dict[str, tp.List[DataBase]] = {}

    last_date: str = ""
    index = 0
    while index < len(flatten):
        tok = flatten[index]

        if tok == "DATES":
            last_date = f"{flatten[index + 1]}.{flatten[index + 2]}.{flatten[index + 3]}"
            result_d.update({last_date: []})
            result.append(last_date)
            index += 6
            continue

        def read_id() -> DataBase:
            global index
            ret = DataBase(id=int(flatten[index][2:]), items=[])
            index += 1

            while flatten[index] != "/":
                if flatten[index][-1] == "*":
                    for j in range(int(flatten[index][:-1])):
                        ret.items.append(f"D{len(ret.items) + 1}")
                    index += 1
                    continue

                ret.items.append(flatten[index])
                index += 1

            index += 1
            return ret

        if tok == "KEYWORD":
            index += 1
            result_d[last_date].append(read_id())
            while flatten[index] != "/":
                result_d[last_date].append(read_id())

        if tok == "END":
            break
        index += 1

    result_str = ""
    for key, value in result_d.items():
        if len(value) != 0:
            print(f"{key}:")
            result_str += f"{key}:\n"
            for i in to_list(value):
                print(f"    ID{i.ident} - {filtered(str(i.items))}")
                result_str += f"    ID{i.ident} - {filtered(str(i.items))}\n"

    output("output.txt")
