"""
Object parsing and related functions
"""
import hashlib
import os
import pathlib
import re
import stat
import sys
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    """
    Hash an object and return the hash (write to a file if write is set)
    """
    header = f"{fmt} {len(data)}\0".encode()
    store = header + data
    obj_hash = hashlib.sha1(store).hexdigest()
    obj = zlib.compress(store)
    if write:
        gitdir = repo_find()
        obj_dir = pathlib.Path(str(gitdir) + "/objects/" + obj_hash[:2])
        if not obj_dir.is_dir():
            os.makedirs(obj_dir)
        obj_name = obj_dir / obj_hash[2:]
        with open(obj_name, "wb") as obj_file:
            obj_file.write(obj)
    return obj_hash


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    """
    Return objects by a prefix
    """
    if not 4 <= len(obj_name) <= 40:
        raise Exception(f"Not a valid object name {obj_name}")
    dir_name = obj_name[:2]
    obj_file = obj_name[2:]
    obj_dir = str(gitdir) + "/objects/" + dir_name
    files_list = os.listdir(obj_dir)
    objs = []
    for obj in files_list:
        if obj[: len(obj_file)] == obj_file:
            objs.append(dir_name + obj)

    if not objs:
        raise Exception(f"Not a valid object name {obj_name}")

    return objs


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    """
    No idea what this should do
    """
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    """
    Return object content
    """
    obj_name = resolve_object(sha, gitdir)[0]
    obj_dir = pathlib.Path(obj_name[:2])
    obj_file_name = pathlib.Path(obj_name[2:])
    path = gitdir / "objects" / obj_dir / obj_file_name
    with open(path, "rb") as obj_file:
        data = zlib.decompress(obj_file.read())
    newline_pos = data.find(b"\x00")
    header = data[:newline_pos]
    space_pos = header.find(b" ")
    obj_type = header[:space_pos].decode("ascii")
    if obj_type == "blob":
        content_len = int(header[space_pos:newline_pos].decode("ascii"))
        content = data[newline_pos + 1 :]
        assert content_len == len(content)
    return (obj_type, content)


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    """
    Read a tree
    """
    # PUT YOUR CODE HERE
    ...


def cat_file(obj_name: str, pretty: bool = True) -> None:
    """
    Print file content by hash
    """
    gitdir = repo_find()
    _, content = read_object(obj_name, gitdir)
    if pretty:
        result = content.decode("ascii")
    else:
        result = str(content)
    print(result)


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    """
    Correlate tree to files
    """
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    """
    Parse a commit
    """
    # PUT YOUR CODE HERE
    ...
