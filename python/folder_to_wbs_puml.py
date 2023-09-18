#!/usr/bin/python3

import os
import argparse

parser = argparse.ArgumentParser(prog="wbs_folder.py",
                                 description="Create a plantuml WBS tree of the current folder")
parser.add_argument('-p', "--path", default=".")
args = parser.parse_args()
fullpath = os.path.abspath(args.path)


def printDir(dirpath, level=2):
    prefix = "*"*(level)
    for child in os.listdir(dirpath):
        print(f"{prefix} {child}")
        fullpath = f"{dirpath}/{child}"
        if os.path.isdir(fullpath):
            printDir(fullpath, level+1)

print("@startwbs\n")
print(f"* {os.path.basename(fullpath)}")
printDir(fullpath)
print("\n@endwbs")