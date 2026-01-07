import csv
import argparse
from itertools import zip_longest


def print_highlighted_cell(row, i_to_highlight, header, color=True):
    # Print header at the beginning
    print(f"{header} ", end="")

    for i, cell in enumerate(row):
        # Handle empty cells
        if cell == "":
            cell = "<empty>"

        # Highlight the selected cell
        if i == i_to_highlight:
            if color:
                print(f"\033[91m{cell}\033[00m", end="")
            else:
                print(f"**{cell}**", end="")
        else:
            print(f"{cell}", end="")

        # Adding a comma to separate elements
        if i != len(row) - 1:
            print(",", end="")

    # Carriage return at the end
    print("")


def get_indices_cols_to_skip(col_names, header):
    col_to_skip_indices = []
    if col_names:
        for col_to_skip in col_names:
            try:
                col_index = header.index(col_to_skip)
            except ValueError:
                print(f"'{col_to_skip}' doesn't exist in file 1")
                continue
            col_to_skip_indices.append(col_index)
    col_to_skip_indices.sort()
    return col_to_skip_indices


def csvmerge(
        in1_path, in2_path, out_path, always=0, skip1=[], skip2=[],
        delimiter=",", nocolor=False):
    with open(in1_path, mode="r", newline="", encoding="utf-8") as infile1, \
         open(in2_path, mode="r", newline="", encoding="utf-8") as infile2, \
         open(out_path, mode="w", newline="", encoding="utf-8") as outfile:

        reader1 = csv.reader(infile1, delimiter=delimiter)
        reader2 = csv.reader(infile2, delimiter=delimiter)
        writer = csv.writer(outfile, delimiter=delimiter, lineterminator='\n')

        # Look for indices of the columns to skip
        header1 = next(reader1)
        col_to_skip_indices1 = get_indices_cols_to_skip(skip1, header1)
        header2 = next(reader2)
        col_to_skip_indices2 = get_indices_cols_to_skip(skip2, header2)

        # Count total number of rows
        tot_rows = 1
        for row1, row2 in zip(reader1, reader2):
            tot_rows += 1
        infile1.seek(0)
        reader1 = csv.reader(infile1, delimiter=delimiter)
        infile2.seek(0)
        reader2 = csv.reader(infile2, delimiter=delimiter)

        i_row = 0
        for row1, row2 in zip_longest(reader1, reader2):
            # Remove skipped columns
            row1_skip = []
            if row1:
                for offset, i in enumerate(col_to_skip_indices1):
                    row1_skip.append(row1.pop(i - offset))
            row2_skip = []
            if row2:
                for offset, i in enumerate(col_to_skip_indices2):
                    row2_skip.append(row2.pop(i - offset))

            output_row = []
            if row1 is not None and row2 is not None:
                i_col = 0
                for c1, c2 in zip_longest(row1, row2):
                    if c1 is not None and c2 is not None:
                        if c1 != c2:
                            if always:
                                if always == 1:
                                    output_row.append(c1)
                                if always == 2:
                                    output_row.append(c2)
                            else:
                                while True:
                                    print(f"--- Row {i_row + 1} of {tot_rows}\
, Column {i_col + 1} ---")
                                    print_highlighted_cell(
                                        row1, i_col, "[1]", not nocolor)
                                    print_highlighted_cell(
                                        row2, i_col, "[2]", not nocolor)
                                    user_input = input("> ")
                                    if user_input == "1":
                                        output_row.append(c1)
                                        break
                                    elif user_input == "2":
                                        output_row.append(c2)
                                        break
                                    elif user_input == "q":
                                        return
                                    else:
                                        print("Invalid input. Type 1 or 2 to \
select the file, q to exit.")
                        else:
                            output_row.append(c1)  # it's equal to c2
                    else:
                        if c1 is not None:
                            output_row.append(c1)
                        if c2 is not None:
                            output_row.append(c2)
                    i_col += 1
            else:
                if row1 is not None:
                    output_row.extend(row1)
                if row2 is not None:
                    output_row.extend(row2)

            # Add skipped columns on the right
            if row1_skip:
                output_row.extend(row1_skip)
            if row2_skip:
                output_row.extend(row2_skip)

            # Write row in output file
            writer.writerow(output_row)
            i_row += 1


if __name__ == "__main__":
    # Parse user arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i1", metavar="file", help="Input file #1", required=True)
    parser.add_argument(
        "-i2", metavar="file", help="Input file #2", required=True)
    parser.add_argument(
        "-o",  metavar="file", help="Output file", required=True)
    parser.add_argument(
        "--always", type=int, default=0, choices=[1, 2],
        help="File from which always pick")
    parser.add_argument(
        "--skip1", metavar="cn", nargs="+", help="Names of the columns to \
remove from file #1 before the comparison. The columns are added back to the \
output file, to the right")
    parser.add_argument(
        "--skip2", metavar="cn", nargs="+", help="Names of the columns to \
remove from file #2 before the comparison. The columns are added back to the \
output file, to the right")
    parser.add_argument(
        "--delimiter", metavar="char", default=",", help="Character used to \
separate the fields in the files")
    parser.add_argument("--nocolor", action="store_true", help="Use asterisks \
to highlight the differences instead of ANSI escape sequences colors")

    parser_args = vars(parser.parse_args())

    # Run main function
    csvmerge(
        parser_args["i1"], parser_args["i2"], parser_args["o"],
        parser_args["always"], parser_args["skip1"], parser_args["skip2"],
        parser_args["delimiter"], parser_args["nocolor"])
