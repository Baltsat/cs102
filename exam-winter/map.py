import typing
import sys

#input
map = open(sys.argv[1], "rt", encoding = "utf_8_sig")
map = [list(l[:-1]) if l[-1] == "\n" else list(l) for l in map.readlines()]

#els   ☒     ☺    .    ☼
  #BFS algorithm
    #see: https://cpp.mazurok.com/tag/bfs/


def solution(m: typing.List[typing.List[str]]) -> typing.List[typing.List[str]]:
    parent: typing.List[typing.List[typing.Tuple[int, int]]] = [[] for i in range(len(m))]

    sam_position: typing.Tuple[int, int] = (-1, -1)
    end_position: typing.Tuple[int, int] = (-1, -1)

    for i in range(len(m)):
        for j in range(len(m[i])):
            parent[i].append((-1, -1))

            if m[i][j] == "☺":
                sam_position = i, j

            if m[i][j] == "☼":
                end_position = i, j

    q: typing.List[typing.Tuple[int, int]] = [sam_position]

    if end_position == (-1, -1) or sam_position == (-1, -1):
        return m

    while len(q) > 0:
        y, x = q.pop(0)

        for move in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_y, new_x = y + move[0], x + move[1]

            if new_y >= len(m) or new_y < 0:
                continue

            if new_x >= len(m[new_y]) or new_x < 0:
                continue

            if (
                m[new_y][new_x] == "☒"
                or parent[new_y][new_x] != (-1, -1)
                or (new_y, new_x) == sam_position
            ):
                continue

            parent[new_y][new_x] = y, x
            q.append((new_y, new_x))

    if parent[end_position[0]][end_position[1]] == (-1, -1):
        return m

    pos: typing.Tuple[int, int] = parent[end_position[0]][end_position[1]]

    while pos != sam_position:
        m[pos[0]][pos[1]] = "☺"
        pos = parent[pos[0]][pos[1]]

    return m

if __name__ == "__main__":
    for x in solution(map):
        print("".join(x))
