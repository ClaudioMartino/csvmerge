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
        in1, in2, out, always="", sort_cols=False, skip1=[],
        skip2=[], delimiter=",", case_insensitive=False, skip_empty=False,
        info_only=False, nocolor=False):
    choices1 = []
    choices2 = []
    asterisks = ""

    # Set the compare function
    if case_insensitive:
        are_different = case_insensitive_diff
    else:
        are_different = standard_diff

    with open(in1, mode="r", newline="", encoding="utf-8-sig") as infile1, \
         open(in2, mode="r", newline="", encoding="utf-8-sig") as infile2, \
         open(out, mode="w", newline="", encoding="utf-8") as outfile:

        reader1 = csv.reader(infile1, delimiter=delimiter)
        reader2 = csv.reader(infile2, delimiter=delimiter)
        writer = csv.writer(outfile, delimiter=delimiter, lineterminator='\n')

        # Look for the indices of the columns to skip
        header1 = next(reader1)
        col_to_skip_indices1 = get_indices_cols_to_skip(skip1, header1)
        header2 = next(reader2)
        col_to_skip_indices2 = get_indices_cols_to_skip(skip2, header2)

        # Get sorted column indices (after pop)
        if sort_cols:
            pop_elements_from_list(header1, col_to_skip_indices1)
            sorted_col1 = sorted(list(enumerate(header1)), key=lambda x: x[1])
            sorted_indices1 = [idx for idx, _ in sorted_col1]
            pop_elements_from_list(header2, col_to_skip_indices2)
            sorted_col2 = sorted(list(enumerate(header2)), key=lambda x: x[1])
            sorted_indices2 = [idx for idx, _ in sorted_col2]

        # Count conflict and rows
        tot_diff = 0
        tot_rows = 0
        infile1.seek(0)
        reader1 = csv.reader(infile1, delimiter=delimiter)
        infile2.seek(0)
        reader2 = csv.reader(infile2, delimiter=delimiter)
        for row1, row2 in zip(reader1, reader2):
            pop_elements_from_list(row1, col_to_skip_indices1)
            pop_elements_from_list(row2, col_to_skip_indices2)
            if sort_cols:
                row1 = [row1[i] for i in sorted_indices1]
                row2 = [row2[i] for i in sorted_indices2]

            for c1, c2 in zip(row1, row2):
                if are_different(c1, c2):
                    if (not skip_empty) or (
                            skip_empty and c1 != "" and c2 != ""):
                        tot_diff += 1
            tot_rows += 1

        # Print the info and exit when requested
        tot_cols = min(len(header1), len(header2))
        print(f"{tot_diff} conflicts for {tot_rows} rows and {tot_cols} \
columns ({tot_diff/(tot_rows*tot_cols)*100:.1f}%)")
        if info_only:
            return

        # Start merge procedure
        diff_cnt = 0
        i_row = 0
        infile1.seek(0)
        reader1 = csv.reader(infile1, delimiter=delimiter)
        infile2.seek(0)
        reader2 = csv.reader(infile2, delimiter=delimiter)
        for row1, row2 in zip_longest(reader1, reader2):
            # Remove skipped columns and sort
            row1_skip = []
            if row1:
                pop_elements_from_list(row1, col_to_skip_indices1, row1_skip)
                if sort_cols:
                    row1 = [row1[i] for i in sorted_indices1]
            row2_skip = []
            if row2:
                pop_elements_from_list(row2, col_to_skip_indices2, row2_skip)
                if sort_cols:
                    row2 = [row2[i] for i in sorted_indices2]

            output_row = []
            if row1 is not None and row2 is not None:
                # Both files have one line
                i_col = 0
                for c1, c2 in zip_longest(row1, row2):
                    if c1 is not None and c2 is not None:
                        # Both rows have one cell
                        if are_different(c1, c2):
                            # Values are different
                            if (not skip_empty) or \
                               (skip_empty and c1 != "" and c2 != ""):
                                diff_cnt += 1
                                if always:
                                    # Automatic execution
                                    if always == "1":
                                        output_row.append(c1)
                                    elif always == "2":
                                        output_row.append(c2)
                                    else:
                                        longest, shortest = \
                                            get_longest_shortest(c1, c2)
                                        if always == "l":
                                            output_row.append(longest)
                                        elif always == "s":
                                            output_row.append(shortest)
                                        else:
                                            raise Exception(
                                                "Invalid 'always' option.")
                                else:
                                    # Interactive execution
                                    while True:
                                        print(f"({diff_cnt}/{tot_diff}) Row \
{i_row + 1} of {tot_rows}, column {i_col + 1} {asterisks}")
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
                                                print("Invalid input. Type 1 \
(or 1+) or 2 (or 2+) to select the file, q to exit.")
                            elif skip_empty and c1 != "" and c2 == "":
                                output_row.append(c1)
                            elif skip_empty and c1 == "" and c2 != "":
                                output_row.append(c2)
                        else:
                            # Values are equal (case sensitive)
                            output_row.append(c1)
                    else:
                        # Remaining cells
                        if c1 is not None:
                            output_row.append(c1)
                        if c2 is not None:
                            output_row.append(c2)
                    i_col += 1
            else:
                # Remaining rows
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
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-h", "--help", action="help", help="Print this help message and exit")
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
        "--sort", action="store_true", help="Sort alphabetically the columns \
of the input files")
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
    parser.add_argument("--skip-empty", action="store_true", help="Ignore \
empty values. If only one of the conflicting cells is empty, the value of the \
other cell is automatically selected")
    parser.add_argument(
        "--case-insensitive", action="store_true", help="Use case insensitive \
comparisons. If two values differ only by case, the value from file #1 will \
be selected")
    parser.add_argument(
        "--info", action="store_true", help="Print the information about the \
input files and exit")
    parser.add_argument(
        "--no-color", action="store_true", help="Use asterisks to highlight \
the differences instead of ANSI escape sequences colors")

    parser_args = vars(parser.parse_args())

    # Run main function
    csvmerge(
        parser_args["i1"], parser_args["i2"], parser_args["o"],
        parser_args["always"], parser_args["sort"], parser_args["skip1"],
        parser_args["skip2"], parser_args["delimiter"],
        parser_args["case_insensitive"], parser_args["skip_empty"],
        parser_args["info"], parser_args["no_color"])
