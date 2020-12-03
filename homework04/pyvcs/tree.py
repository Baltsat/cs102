import os
import pathlib
import stat
import time
import typing as tp
import sys

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    """
    Write a tree as a git object and return its' hash
    tree_entries = [] done
    пройтись по каждой записи в индексе: done
        если имеем дело с каталогом (lib/books/dune.txt): errrrhhm how the fuck?
            отсекаем первую часть пути (lib) okay bruh
            формируем строку: "mode путь\x00sha" (путь это lib, второй раз, lib/books, попробуйте закоммитить несколько вложенных каталогов и посмотреть tree-obj) tried that. Still don't know what the fuck to do
            прибавляем к tree_entries okay
            вызываем write-tree для оставшегося пути (books/dune.txt) fuck recursion btw
        иначе, имеем дело с именем файла (dune.txt): done
            формируем строку: "mode_в_8_й_системе имя_файла\x00sha" done
            прибавляем к tree_entries done
    данные = объединяем все tree_entries в длинную строку байт done
    вернуть hash_object(данные, "tree", write=True) done too
    """
    tree_entries = []
    for entry in index:
        prefix, name = os.path.split(entry.name)
        if prefix:
            pass # i hate myself and my life
            #tree_hash = write_tree(gitdir, index, name)
        mode = str(oct(entry.mode))[2:]
        tree_entry = f"{mode} {entry.name}\0".encode()
        tree_entry += entry.sha1
        tree_entries.append(tree_entry)

    data = "".encode()
    for tree_entry in tree_entries:
        data += tree_entry
    return hash_object(data, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    # PUT YOUR CODE HERE
    ...
