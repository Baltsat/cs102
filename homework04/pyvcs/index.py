"""
Git index operations
"""
import hashlib
# import operator
import os
import pathlib
import string
import struct
import typing as tp
import sys

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    """
    An index entry in readable format
    """

    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        """
        Pack into index format
        """
        # shit code, btw. Less shit than the unpack() function, though
        values = (
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
        )  # ints prepared for straight-forward packing
        bytecast_values = tuple(
            [i.to_bytes(4, "big") for i in values]
        )  # convert to network byte order
        bytecast_str = struct.pack(
            "4s4s4s4s4s4s4s4s4s4s", *bytecast_values
        )  # pack using 10 4bytes objects because FUCK FORMAT STRINGS
        bytecast_str += self.sha1  # simply concatenate
        bytecast_str += self.flags.to_bytes(
            2, "big"
        )  # cast to network order, truncate to 2 and concatenate
        bytecast_str += self.name.encode("ascii")  # simply concatenate the encoded string
        if not len(bytecast_str) % 4 == 0:  # if struct is not aligned to 4 byte-divisible size
            padding_size = 4 - (len(bytecast_str) % 4)  # calculate padded size
            # align size - remaining symbols to align
            for _ in range(0, padding_size):  # pad the shit to fill the void in my fucking soul
                bytecast_str += b"\x00"
        return bytecast_str

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        """
        Unpack into readable format
        """
        # shit code, btw
        last_byte = data[-1]  # start at something
        while last_byte == 0:  # check for NUL padding
            data = data[:-1]  # remove it
            last_byte = data[-1]  # update last_char
        name = ""
        while chr(last_byte) in (
            string.ascii_letters + string.punctuation + string.digits
        ):  # name can't contain non-character bytes, right? fucking shit
            name += chr(last_byte)  # add the letter to the name
            data = data[:-1]  # remove it from the data stream
            last_byte = data[-1]  # update last_char
        name = name[::-1]  # reverses the name (i. e, "txt.rab" converts to "bar.txt")
        flags = int.from_bytes(
            data[-2:], "big"
        )  # get the flags, casting to int from big-endian bytes
        data = data[:-2]  # remove the flags from the byte stream
        sha = data[-20:]  # get the sha (it's in bytes, no converstion required)
        data = data[:-20]  # remove the sha from the data
        unpacked_ints = struct.unpack(
            "4s4s4s4s4s4s4s4s4s4s", data
        )  # we can unpack the big-endian byte snippets with struct now
        bytecast_ints = tuple(
            [int.from_bytes(i, "big") for i in unpacked_ints]
        )  # and cast them to ints
        index_entry = GitIndexEntry(
            bytecast_ints[0],
            bytecast_ints[1],
            bytecast_ints[2],
            bytecast_ints[3],
            bytecast_ints[4],
            bytecast_ints[5],
            bytecast_ints[6],
            bytecast_ints[7],
            bytecast_ints[8],
            bytecast_ints[9],
            sha,
            flags,
            name,
        )  # construct the index entry FINALLY GODFUCKINGDAMNIT
        return index_entry


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    """
    Get index entries in readable format from index
    """
    index_entries = []
    if not (gitdir / "index").is_file():  # no index detected, return an empty list
        return []
    with open(gitdir / "index", "rb") as index_file:
        data = index_file.read()
    data = data[:-20]  # delete the checksum because i said so, goddamnit FUCK
    version = 2  # fuck versions
    version_bytecast = version.to_bytes(4, "big")  # go to bytes
    version_pos = data.find(version_bytecast)  # find the version in byte stream
    data = data[version_pos + 4 :]  # delete the DIRC and version
    entry_count_bytes = data[:4]  # entry count bytes
    entry_count_pos = data.find(entry_count_bytes)  # find the entry count in byte stream
    entry_count = int.from_bytes(entry_count_bytes, "big")  # cast to int
    data = data[entry_count_pos + 4 :]  # delete the entry count from byte stream
    for _ in range(entry_count):  # for each entry
        entry = data[:62]  # 62 bytes are 10 4 byte ints + 20 byte sha + 2 byte flags
        # those are immutable, i hope
        data = data[62:]  # truncate byte stream
        in_extension = False
        while True:  # because FUCK YOU GODDAMNIT FUCK ASS SHIT
            if len(data) == 0:  # no entries left, abort
                break
            byte = chr(data[0])  # get symbol
            if byte == "\x00":  # padding starts, name ends
                break
            if byte == ".":  # hacks
                in_extension = True  # so hacks
            if in_extension and not byte == ".":  # very hacks
                if not byte in string.ascii_letters:  # much hacks
                    break  # fuck i hate myself
            entry += byte.encode("ascii")  # add as name
            data = data[1:]  # truncate byte from byte stream
        while True:
            if len(data) == 0:  # no entries left, abort
                break
            byte = chr(data[0])
            if byte != "\x00":  # not padding
                break
            entry += byte.encode("ascii")  # add padding
            data = data[1:]  # truncate byte from byte stream

        entry_unpacked = GitIndexEntry.unpack(entry)
        index_entries.append(entry_unpacked)

    return index_entries


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    """
    Write entries to index
    """
    with open(gitdir / "index", "wb") as index_file:
        version = 2  # FUCK VERSIONS
        version_bytecast = version.to_bytes(4, "big")
        entries_len_bytecast = len(entries).to_bytes(4, "big")
        index_content = "DIRC".encode()
        index_content += version_bytecast
        index_content += entries_len_bytecast
        for entry in entries:
            index_content += entry.pack()
        # fuck extensions
        index_sha = hashlib.sha1(index_content).digest()  # in binary because FUCK YOU ASSHOLE
        index_content += index_sha
        index_file.write(index_content)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    """
    Get indexed files' details
    """
    index_entries = read_index(gitdir)
    if details:
        for entry in index_entries:
            mode = str(oct(entry.mode))[
                2:
            ]  # get mode in decimal, convert to octal, convert to string, strip prefix ("0o")
            sha = entry.sha1.hex()
            name = entry.name
            flags = entry.flags
            stage = (entry.flags >> 12) & 3 # Dementiy bit-field magic
            print(f"{mode} {sha} {stage}\t{name}")  
    else:
        for entry in index_entries:
            name = entry.name
            print(f"{name}")


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    """
    Update index by adding new files
    """
    index_entries: tp.List[GitIndexEntry] = []
    absolute_paths = [i.absolute() for i in paths]  # get absolute paths
    absolute_paths.sort()  # sort by them
    relative_paths = [
        i.relative_to(os.getcwd()) for i in absolute_paths
    ]  # revert back to relative paths
    relative_paths.reverse()  # reverse the list because FUCK IF I KNOW
    for path in relative_paths:  # finally
        with open(path, "rb") as f_name:
            data = f_name.read()  # read some shit
        obj_hash = bytes.fromhex(hash_object(data, "blob", True))  # write the object you motherfucker
        os_stats = os.stat(path, follow_symlinks=False)  # fuck links
        # fuck this object, really
        name_len = len(str(path))
        if name_len > 0xFFF:  # fucking bit fields
            name_len = 0xFFF
        flags = name_len + 0b0001
        # 1 bit assume-valid (will be 1 for now),
        # 2 bit 0 because we use version 2,
        # 13 bits name_len (or 0xFFF)
        # reversed because little_endian or some shit
        index_entry = GitIndexEntry(
            int(os_stats.st_ctime),
            0,
            int(os_stats.st_mtime),
            0,
            os_stats.st_dev,
            os_stats.st_ino,
            os_stats.st_mode,
            os_stats.st_uid,
            os_stats.st_gid,
            os_stats.st_size,
            obj_hash,
            flags,
            str(path),
        )
        # THIS FUCKING SUCKS ASS
        if index_entry not in index_entries:  # skip existing entries
            index_entries.insert(0, index_entry)

    if write:
        write_index(gitdir, index_entries)
