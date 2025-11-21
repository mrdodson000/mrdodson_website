import sys
import pathlib
import md_parser as mdp
import subprocess

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Error: provide post processor with a single filepath.")
        sys.exit(1)

    website_root_path = sys.argv[1]

    mdp.md_parse(website_root_path)
