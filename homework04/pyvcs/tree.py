"""
Operations on Git tree objects
"""
import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    """
    Write a tree as a git object and return its' hash
    """
    tree_entries = []
    for entry in index:
        _, name = os.path.split(entry.name)
        if dirname:
            names = dirname.split(os.sep)
        else:
            names = entry.name.split(os.sep)
        if len(names) != 1:
            prefix = names[0]
            name = f"{os.sep}".join(names[1:])
            mode = "40000"
            tree_entry = f"{mode} {prefix}\0".encode()
            tree_entry += bytes.fromhex(write_tree(gitdir, index, name))
            tree_entries.append(tree_entry)
        else:
            if dirname and entry.name.find(dirname) == -1:
                continue
            with open(entry.name, "rb") as content:
                data = content.read()
            mode = str(oct(entry.mode))[2:]
            tree_entry = f"{mode} {name}\0".encode()
            tree_entry += bytes.fromhex(hash_object(data, "blob", write=True))
            tree_entries.append(tree_entry)

    tree_binary = b"".join(tree_entries)
    return hash_object(tree_binary, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    """
    Commit a tree
    """
    timestamp = int(time.mktime(time.localtime()))
    timezone = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    timezone = int(timezone / 60 / 60 * -1)
    if timezone > 0:
        tz_offset = f"+0{timezone}00"
    elif timezone < 0:
        tz_offset = f"-0{timezone}00"
    else:
        tz_offset = "0000"
    if not author:
        author = ""
    email = os.getenv("GIT_AUTHOR_EMAIL")
    if not email:
        email = ""
    if not parent:
        parent = ""

    author_str = f"{author} <{email}>"

    data = f"tree {tree}\n"
    if parent:
        data += f"parent {parent}\n"
    data += f"author {author} {timestamp} {tz_offset}\ncommitter {author} {timestamp} {tz_offset}\n\n{message}\n"
    return hash_object(data.encode(), "commit", write=True)
