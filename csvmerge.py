import csv
import argparse
from itertools import zip_longest


def standard_diff(c1, c2):
    return c1 != c2


def case_insensitive_diff(c1, c2):
    return c1.casefold() != c2.casefold()


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


def pop_elements_from_list(list_, indices, removed=None):
    for offset, i in enumerate(indices):
        element = list_.pop(i - offset)
        if removed is not None:
            removed.append(element)


def get_longest_shortest(string1, string2):
    if len(string1) >= len(string2):
        longest = string1
        shortest = string2
    else:
        longest = string2
        shortest = string1
    return longest, shortest


def csvmerge(
        in1_path, in2_path, out_path, always="", skip1=[], skip2=[],
        delimiter=",", caseinsensitive=False, nocolor=False):
    choices1 = []
    choices2 = []
    asterisks = ""

    # Set the compare function
    if caseinsensitive:
        are_different = case_insensitive_diff
    else:
        are_different = standard_diff

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

        # Count total number of differences and rows
        tot_diff = 0
        pop_elements_from_list(header1, col_to_skip_indices1)
        pop_elements_from_list(header2, col_to_skip_indices2)
        for c1, c2 in zip(header1, header2):
            if are_different(c1, c2):
                tot_diff += 1
        tot_rows = 1
        for row1, row2 in zip(reader1, reader2):
            pop_elements_from_list(row1, col_to_skip_indices1)
            pop_elements_from_list(row2, col_to_skip_indices2)
            for c1, c2 in zip(row1, row2):
                if are_different(c1, c2):
                    tot_diff += 1
            tot_rows += 1

        infile1.seek(0)
        reader1 = csv.reader(infile1, delimiter=delimiter)
        infile2.seek(0)
        reader2 = csv.reader(infile2, delimiter=delimiter)

        diff_cnt = 0
        i_row = 0
        for row1, row2 in zip_longest(reader1, reader2):
            # Remove skipped columns
            row1_skip = []
            if row1:
                pop_elements_from_list(row1, col_to_skip_indices1, row1_skip)
            row2_skip = []
            if row2:
                pop_elements_from_list(row2, col_to_skip_indices2, row2_skip)

            output_row = []
            if row1 is not None and row2 is not None:
                i_col = 0
                for c1, c2 in zip_longest(row1, row2):
                    if c1 is not None and c2 is not None:
                        if are_different(c1, c2):
                            diff_cnt += 1
                            if always:
                                if always == "1":
                                    output_row.append(c1)
                                elif always == "2":
                                    output_row.append(c2)
                                else:
                                    longest, shortest = get_longest_shortest(
                                                            c1, c2)
                                    if always == "l":
                                        output_row.append(longest)
                                    elif always == "s":
                                        output_row.append(shortest)
                                    else:
                                        raise Exception("Invalid 'always'.")
                            else:
                                while True:
                                    print(f"({diff_cnt}/{tot_diff}) Row \
{i_row + 1} of {tot_rows}, Column {i_col + 1} {asterisks}")
                                    print_highlighted_cell(
                                        row1, i_col, "[1]", not nocolor)
                                    print_highlighted_cell(
                                        row2, i_col, "[2]", not nocolor)
                                    if (c1, c2) in choices1:
                                        output_row.append(c1)
                                        print("> 1!")
                                        break
                                    elif (c1, c2) in choices2:
                                        output_row.append(c2)
                                        print("> 2!")
                                        break
                                    else:
                                        user_input = input("> ")
                                        if user_input == "1":
                                            output_row.append(c1)
                                            break
                                        elif user_input == "1+":
                                            output_row.append(c1)
                                            choices1.append((c1, c2))
                                            asterisks += "*"
                                            print(f"{c1} from now on.")
                                            break
                                        elif user_input == "2":
                                            output_row.append(c2)
                                            break
                                        elif user_input == "2+":
                                            output_row.append(c2)
                                            choices2.append((c1, c2))
                                            asterisks += "*"
                                            print(f"{c2} from now on.")
                                            break
                                        elif user_input == "q":
                                            return
                                        else:
                                            print("Invalid input. Type 1 (or \
1+) or 2 (or 2+) to select the file, q to exit.")
                        else:
                            output_row.append(c1)  # == c2 (if case sensitive)
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
        "--always", default="", choices=["1", "2", "l", "s"], help="Adopt \
automatically the same decision for each conflict: '1' to always pick the \
value from file #1, '2' to pick the value from file #2, 'l' to pick the \
longest value, 's' to pick the shortest value.")
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
    parser.add_argument(
        "--caseinsensitive", action="store_true", help="Use case-insensitive \
comparisons. If two values differ only by case, the value from file #1 will \
be selected")
    parser.add_argument(
        "--nocolor", action="store_true", help="Use asterisks to highlight \
the differences instead of ANSI escape sequences colors")

    parser_args = vars(parser.parse_args())

    # Run main function
    csvmerge(
        parser_args["i1"], parser_args["i2"], parser_args["o"],
        parser_args["always"], parser_args["skip1"], parser_args["skip2"],
        parser_args["delimiter"], parser_args["caseinsensitive"],
        parser_args["nocolor"])
