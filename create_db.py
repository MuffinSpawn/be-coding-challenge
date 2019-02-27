import sys
import argparse

from family_tree.database import create

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', required=False,
        help='Path to the database')
    args = vars(ap.parse_args())
    create(args['file'])

if __name__ == '__main__':
    main()