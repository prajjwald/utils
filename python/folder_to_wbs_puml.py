#!/usr/bin/python3

import os
import argparse
import functools

class Ignores:
    def __init__(self):
        # Just ignore all hidden directories for now
        self.ignorePrefixes = [ '.' ]
        # Ignore images, documents, etc
        # very arbitrary, ad-hoc list
        self.ignoreSuffixes = [ '.png', '.svg', '.jpg', '.jpeg',
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
    def __init__(self, path):
        self.fullpath = os.path.abspath(args.path)
        self.ignores = Ignores()

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
    parser.add_argument('-p', "--path", default=".")
    args = parser.parse_args()
    
    dirPrinter = DirPrinter(args.path)
    dirPrinter.print()