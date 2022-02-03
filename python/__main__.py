import argparse
import sys

import pandas as pd

from .constraint import *
from .grid import *
from .solve import *

def cmd_solve(args):
    df = pd.read_csv(args.csv, header=None)

    # create the grid
    grid = Grid()
    grid.parse_df(df)

    # solve
    grid2 = solve(grid)
    df2 = grid2.df()
    df2.to_csv("solution.csv", header=False, index=False)
    

def cmd_sums(args):
    sum = args.sum
    count = args.count
    choices = list(map(lambda x: int(x), args.choices.split(",")))
    
    print("sum: {}".format(sum))
    print("count: {}".format(count))
    print("choices: {}".format(choices))

    assert count <= len(choices)
    
    print("choice lists:")
    for choice_list in generate_sums(sum, count, choices):
        print("  {}".format(choice_list))


def cmd_validate(args):
    df = pd.read_csv(args.csv, header=None)

    # create the grid
    grid = Grid()
    grid.parse_df(df)

    print("found {} numerical cells".format(len(grid.cells)))
    

def get_parser():
    parser = argparse.ArgumentParser(
        description="Solve cross sums puzzles")
    subparsers = parser.add_subparsers()

    # solve
    p = subparsers.add_parser(
        "solve",
        help="read a CSV file representing a puzzle and output solution")
    p.add_argument(
        "csv",
        help="CSV file containing puzzle description")
    p.add_argument(
        "--output", "-o",
        default=None,
        help="CSV file containing puzzle solution")
    p.set_defaults(func=cmd_solve)

    # sums
    p = subparsers.add_parser(
        "sums",
        help="generate and print sums")
    p.add_argument(
        "sum",
        type=int,
        help="sum of the numbers")
    p.add_argument(
        "count",
        type=int,
        help="required number of addends")
    p.add_argument(
        "choices",
        help="comma-separate list of possible addends")
    p.set_defaults(func=cmd_sums)

    # validate
    p = subparsers.add_parser(
        "validate",
        help="validate a CSV file representing a puzzle")
    p.add_argument(
        "csv",
        help="CSV file containing puzzle description")
    p.set_defaults(func=cmd_validate)

    return parser


def main():
    parser = get_parser()

    # execute the function
    args = parser.parse_args(sys.argv[1:])
    if "func" in args:
        return args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
