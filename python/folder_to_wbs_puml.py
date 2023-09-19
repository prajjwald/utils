#!/usr/bin/python3

import os
import argparse
import functools

class Ignores:
    def __init__(self, ignorePrefixes: str, ignoreSuffixes: str):
        # Just ignore all hidden directories for now
        self.ignorePrefixes = ignorePrefixes.split(",") if ignorePrefixes \
            else [ '.', 'docker', 'images', 'sounds', 'docs', 'LICENSE', 'Makefile' ]
        # Ignore images, documents, etc
        # very arbitrary, ad-hoc list
        self.ignoreSuffixes = ignoreSuffixes.split(",") if ignoreSuffixes \
            else [ '.png', '.svg', '.jpg', '.jpeg',
                         '.md', '.txt', '.doc', 'xls', '.ppt', '.odt' ]

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
    def __init__(self, path, maxlevel : int,
                 ignorePrefixes: str, ignoreSuffixes: str,
                 textonly: bool):
        self.maxlevel = maxlevel
        self.fullpath = os.path.abspath(path)
        self.ignores = Ignores(ignorePrefixes, ignoreSuffixes)
        self.textonly = textonly
        self.emojis = {"dir": "<:palm_tree:>", "leaf": "<:four_leaf_clover:>"}

    def printElement(self, element, stars, isDirectory):
        print("*"*stars, end=" ")
        if not self.textonly:
            emoji = self.emojis["dir"] if isDirectory else self.emojis["leaf"]
            print(emoji, end=" ")
        print(element)

    def print(self):
        print("@startwbs\n")
        self.printElement(os.path.basename(self.fullpath), 1, True)
        self.printDir(self.fullpath)
        print("\n@endwbs")

    def printDir(self, dirpath, level=1):
        if self.maxlevel and (level > self.maxlevel):
            return
        for child in os.listdir(dirpath):
            if self.ignores.ignore(child):
                continue

            fullpath = f"{dirpath}/{child}"
            if os.path.isdir(fullpath):
                self.printElement(child, level+1, True)
                self.printDir(fullpath, level+1)
            else:
                self.printElement(child, level+1, False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="wbs_folder.py",
                                 description="Create a plantuml WBS tree of the current folder")
    parser.add_argument('-d', "--directory", default=".")
    # Ignore paths
    parser.add_argument('-p', "--ignoreprefix", default=None)
    parser.add_argument('-s', "--ignoresuffix", default=None)
    parser.add_argument('-l', "--maxlevel", default=0, type=int)
    parser.add_argument('-t', "--textonly", action='store_true')
    args = parser.parse_args()
    
    dirPrinter = DirPrinter(args.directory,
                            args.maxlevel,
                            args.ignoreprefix,
                            args.ignoresuffix,
                            args.textonly)
    dirPrinter.print()