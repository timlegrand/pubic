
import os


def list_files(path):
    local_tree = os.walk(path)
    for dirpath, dirnames, filenames in local_tree:
        for dirname in dirnames:
            yield (os.path.join(dirpath, dirname))[len(path) + 1:]
        for filename in filenames:
            yield (os.path.join(dirpath, filename))[len(path) + 1:]
