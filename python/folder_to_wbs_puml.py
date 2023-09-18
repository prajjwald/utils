#!/usr/bin/python3

import os
import argparse
import functools

class Ignores:
    def __init__(self, ignorePrefixes: str, ignoreSuffixes: str):
        # Just ignore all hidden directories for now
        self.ignorePrefixes = ignorePrefixes.split(",") if ignorePrefixes \
            else [ '.', 'docker', 'images', 'sounds', 'docs', 'LICENSE' ]
        # Ignore images, documents, etc
        # very arbitrary, ad-hoc list
        self.ignoreSuffixes = ignoreSuffixes.split(",") if ignoreSuffixes \
            else [ '.png', '.svg', '.jpg', '.jpeg',
                         '.md', '.txt', '.doc' ]

        # Add first element false for functools.reduce
        self.ignorePrefixes = [ False ] + self.ignorePrefixes
        self.ignoreSuffixes = [ False ] + self.ignoreSuffixes
        

    def ignore(self, node: str):
        ignorePrefixMatch = functools.reduce(
            lambda x,y: x or node.startswith(y),
                                       self.ignorePrefixes)
        ignoreSuffixMatch = functools.reduce(
            lambda x,y: x or node.endswith(y),
                                       self.ignoreSuffixes)
        return ignorePrefixMatch or ignoreSuffixMatch

class DirPrinter:
    def __init__(self, path, ignorePrefixes: str, ignoreSuffixes: str):
        self.fullpath = os.path.abspath(path)
        self.ignores = Ignores(ignorePrefixes, ignoreSuffixes)

    def print(self):
        print("@startwbs\n")
        print(f"* {os.path.basename(self.fullpath)}")
        self.printDir(self.fullpath)
        print("\n@endwbs")

    def printDir(self, dirpath, level=2):
        prefix = "*"*(level)
        for child in os.listdir(dirpath):
            if self.ignores.ignore(child):
                continue
            print(f"{prefix} {child}")
            fullpath = f"{dirpath}/{child}"
            if os.path.isdir(fullpath):
                self.printDir(fullpath, level+1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="wbs_folder.py",
                                 description="Create a plantuml WBS tree of the current folder")
    parser.add_argument('-d', "--directory", default=".")
    # Ignore paths
    parser.add_argument('-p', "--ignoreprefix", default=None)
    parser.add_argument('-s', "--ignoresuffix", default=None)
    args = parser.parse_args()
    
    dirPrinter = DirPrinter(args.directory,
                            args.ignoreprefix,
                            args.ignoresuffix)
    dirPrinter.print()