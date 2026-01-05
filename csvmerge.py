import csv
import argparse
from itertools import zip_longest


def print_highlighted_cell(row, i_to_highlight, header):
    print(f"{header} ", end="")
    for i, cell in enumerate(row):
        if not cell:
            cell = "<empty>"
        if i == i_to_highlight:
            print(f"\033[91m{cell}\033[00m,", end="")
        else:
            print(f"{cell},", end="")
    print("")


def csvmerge(inputfile1_path, inputfile2_path, outputfile_path, always=0):
    with open(inputfile1_path, mode="r", encoding="utf-8") as inputfile1, \
         open(inputfile2_path, mode="r", encoding="utf-8") as inputfile2, \
         open(outputfile_path, mode="w", encoding="utf-8") as outputfile:

        reader1 = csv.reader(inputfile1)
        reader2 = csv.reader(inputfile2)
        writer = csv.writer(outputfile)

        # Count total number of rows
        tot_rows = 0
        for row1, row2 in zip(reader1, reader2):
            tot_rows += 1
        inputfile1.seek(0)
        inputfile2.seek(0)
        reader1 = csv.reader(inputfile1)
        reader2 = csv.reader(inputfile2)

        i_row = 0
        for row1, row2 in zip_longest(reader1, reader2):
            output_row = []
            if row1 and row2:
                for (i_col, c1), c2 in zip(enumerate(row1), row2):
                    if c1 != c2:
                        if always:
                            if always == 1:
                                output_row.append(c1)
                            if always == 2:
                                output_row.append(c2)
                        else:
                            while True:
                                print(f"--- Row {i_row + 1} of {tot_rows}, \
Column {i_col + 1} ---")
                                print_highlighted_cell(row1, i_col, "[1]")
                                print_highlighted_cell(row2, i_col, "[2]")
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
                        output_row.append(c1)

                # Handle tail for rows with different number of columns
                if len(row1) > len(row2):
                    print(f"Adding columns {len(row2)+1} to {len(row1)} from \
file 1")
                    output_row.extend(row1[len(row2):])
                if len(row2) > len(row1):
                    print(f"Adding columns {len(row1)+1} to {len(row2)} from \
file 2")
                    output_row.extend(row2[len(row1):])
            else:
                if row1:
                    output_row.extend(row1)
                if row2:
                    output_row.extend(row2)
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
    parser_args = vars(parser.parse_args())

    csvmerge(
        parser_args["i1"], parser_args["i2"], parser_args["o"],
        parser_args["always"])
