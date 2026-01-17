import csv
import argparse
from itertools import zip_longest
import logging


def standard_diff(c1, c2):
    return c1 != c2


def case_insensitive_diff(c1, c2):
    return c1.casefold() != c2.casefold()


def print_highlighted_cell(row, i_to_highlight, header, color=True):
    # Use header at the beginning
    message = f"{header} "

    for i, cell in enumerate(row):
        # Handle empty cells
        if cell == "":
            cell = "<empty>"

        # Highlight the selected cell
        if i == i_to_highlight:
            if color:
                message += f"\033[91m{cell}\033[00m"
            else:
                message += f"**{cell}**"
        else:
            message += f"{cell}"

        # Adding a comma to separate elements
        if i != len(row) - 1:
            message += ","

    # Print complete message
    logging.info(message)


def get_indices_from_col_names(col_names, header):
    col_to_skip_indices = []
    if col_names:
        for col_to_skip in col_names:
            try:
                col_index = header.index(col_to_skip)
            except ValueError:
                logging.warning(f"'{col_to_skip}' doesn't exist in file 1")
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


class CSVMerge:
    def __init__(self, in1, in2, out, always="", sort_cols=False, skip1=[],
                 skip2=[], drop1=[], drop2=[], delimiter=",",
                 case_insensitive=False, skip_empty=False, no_color=False):
        self.in1 = in1
        self.in2 = in2
        self.out = out
        self.always = always
        self.sort_cols = sort_cols
        self.skip1 = skip1
        self.skip2 = skip2
        self.drop1 = drop1
        self.drop2 = drop2
        self.delimiter = delimiter
        if case_insensitive:
            self.are_different = case_insensitive_diff
        else:
            self.are_different = standard_diff
        self.skip_empty = skip_empty
        self.no_color = no_color

        self.col_to_skip_indices1 = []
        self.col_to_skip_indices2 = []
        self.col_to_drop_indices1 = []
        self.col_to_drop_indices2 = []
        self.sorted_indices1 = []
        self.sorted_indices2 = []
        self.tot_rows = 0
        self.tot_cols = 0
        self.tot_diff = 0

        with open(self.in1, mode="r", newline="", encoding="utf-8-sig") as \
                infile1, \
             open(self.in2, mode="r", newline="", encoding="utf-8-sig") as \
                infile2:
            reader1 = csv.reader(infile1, delimiter=self.delimiter)
            reader2 = csv.reader(infile2, delimiter=self.delimiter)

            # Look for the indices of the columns to skip and drop
            header1 = next(reader1)
            self.col_to_skip_indices1 = get_indices_from_col_names(
                self.skip1, header1)
            pop_elements_from_list(header1, self.col_to_skip_indices1)
            self.col_to_drop_indices1 = get_indices_from_col_names(
                self.drop1, header1)
            pop_elements_from_list(header1, self.col_to_drop_indices1)

            header2 = next(reader2)
            self.col_to_skip_indices2 = get_indices_from_col_names(
                self.skip2, header2)
            pop_elements_from_list(header2, self.col_to_skip_indices2)
            self.col_to_drop_indices2 = get_indices_from_col_names(
                self.drop2, header2)
            pop_elements_from_list(header2, self.col_to_drop_indices2)

            # Compute total number of columns from headers
            self.tot_cols = max(len(header1), len(header2))

            # Get sorted column indices (after pop)
            if self.sort_cols:
                sorted_col1 = sorted(
                    list(enumerate(header1)), key=lambda x: x[1])
                self.sorted_indices1 = [idx for idx, _ in sorted_col1]
                sorted_col2 = sorted(
                    list(enumerate(header2)), key=lambda x: x[1])
                self.sorted_indices2 = [idx for idx, _ in sorted_col2]

            # Count total number of conflicts and rows
            infile1.seek(0)
            reader1 = csv.reader(infile1, delimiter=self.delimiter)
            infile2.seek(0)
            reader2 = csv.reader(infile2, delimiter=self.delimiter)
            for row1, row2 in zip(reader1, reader2):
                pop_elements_from_list(row1, self.col_to_skip_indices1)
                pop_elements_from_list(row1, self.col_to_drop_indices1)
                pop_elements_from_list(row2, self.col_to_skip_indices2)
                pop_elements_from_list(row2, self.col_to_drop_indices2)
                if self.sort_cols:
                    row1 = [row1[i] for i in self.sorted_indices1]
                    row2 = [row2[i] for i in self.sorted_indices2]

                for c1, c2 in zip(row1, row2):
                    if self.are_different(c1, c2):
                        if (not self.skip_empty) or \
                                (self.skip_empty and c1 != "" and c2 != ""):
                            self.tot_diff += 1
                self.tot_rows += 1

        # Print number of conflicts, rows and columns
        if self.tot_cols != 0 and self.tot_rows != 0:
            logging.debug(f"{self.tot_diff} conflicts for {self.tot_rows} \
rows and {self.tot_cols} columns \
({self.tot_diff/(self.tot_rows*self.tot_cols)*100:.1f}%).")

    def run(self):
        with open(self.in1, mode="r", newline="", encoding="utf-8-sig") as \
                infile1, \
             open(self.in2, mode="r", newline="", encoding="utf-8-sig") as \
                infile2, \
             open(self.out, mode="w", newline="", encoding="utf-8") as outfile:
            reader1 = csv.reader(infile1, delimiter=self.delimiter)
            reader2 = csv.reader(infile2, delimiter=self.delimiter)
            writer = csv.writer(
                outfile, delimiter=self.delimiter, lineterminator='\n')

            choices1 = []
            choices2 = []
            asterisks = ""

            diff_cnt = 0
            i_row = 0
            for row1, row2 in zip_longest(reader1, reader2):
                # Remove skipped columns and sort
                row1_skip = []
                if row1:
                    pop_elements_from_list(
                        row1, self.col_to_skip_indices1, row1_skip)
                    pop_elements_from_list(row1, self.col_to_drop_indices1)
                    if self.sort_cols:
                        row1 = [row1[i] for i in self.sorted_indices1]
                row2_skip = []
                if row2:
                    pop_elements_from_list(
                        row2, self.col_to_skip_indices2, row2_skip)
                    pop_elements_from_list(row2, self.col_to_drop_indices2)
                    if self.sort_cols:
                        row2 = [row2[i] for i in self.sorted_indices2]

                output_row = []
                if row1 is not None and row2 is not None:
                    # Both files have one line
                    i_col = 0
                    for c1, c2 in zip_longest(row1, row2):
                        if c1 is not None and c2 is not None:
                            # Both rows have one cell
                            if self.are_different(c1, c2):
                                # Values are different
                                if (not self.skip_empty) or \
                                        (self.skip_empty and c1 != ""
                                         and c2 != ""):
                                    diff_cnt += 1
                                    if self.always:
                                        # Automatic execution
                                        if self.always == "1":
                                            output_row.append(c1)
                                        elif self.always == "2":
                                            output_row.append(c2)
                                        else:
                                            longest, shortest = \
                                                get_longest_shortest(c1, c2)
                                            if self.always == "l":
                                                output_row.append(longest)
                                            elif self.always == "s":
                                                output_row.append(shortest)
                                            else:
                                                raise Exception(
                                                    "Invalid 'always' option.")
                                    else:
                                        # Interactive execution
                                        while True:
                                            logging.info(
                                                f"({diff_cnt}/{self.tot_diff}\
) Row {i_row + 1} of {self.tot_rows}, column {i_col + 1} {asterisks}")
                                            print_highlighted_cell(
                                                row1, i_col, "[1]",
                                                not self.no_color)
                                            print_highlighted_cell(
                                                row2, i_col, "[2]",
                                                not self.no_color)
                                            if (c1, c2) in choices1:
                                                output_row.append(c1)
                                                logging.info("> 1!")
                                                break
                                            elif (c1, c2) in choices2:
                                                output_row.append(c2)
                                                logging.info("> 2!")
                                                break
                                            else:
                                                user_input = input("> ")
                                                if user_input == "1":
                                                    output_row.append(c1)
                                                    logging.debug(
                                                        f"{c1} selected.")
                                                    break
                                                elif user_input == "1+":
                                                    output_row.append(c1)
                                                    choices1.append((c1, c2))
                                                    asterisks += "*"
                                                    logging.info(
                                                        f"{c1} from now on.")
                                                    break
                                                elif user_input == "2":
                                                    output_row.append(c2)
                                                    logging.debug(
                                                        f"{c2} selected.")
                                                    break
                                                elif user_input == "2+":
                                                    output_row.append(c2)
                                                    choices2.append((c1, c2))
                                                    asterisks += "*"
                                                    logging.info(
                                                        f"{c2} from now on.")
                                                    break
                                                elif user_input == "q":
                                                    return
                                                else:
                                                    logging.info(
                                                        "Invalid input. Type \
1 (or 1+) or 2 (or 2+) to select the file, q to exit.")
                                elif self.skip_empty and c1 != "" and c2 == "":
                                    output_row.append(c1)
                                elif self.skip_empty and c1 == "" and c2 != "":
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
            logging.debug(f"{i_row} rows written in {self.out}.")


if __name__ == "__main__":
    # Parse user arguments
    parser = argparse.ArgumentParser(add_help=False)

    general = parser.add_argument_group("General options")
    general.add_argument(
        "-i1", metavar="FILE", help="Input file #1", required=True)
    general.add_argument(
        "-i2", metavar="FILE", help="Input file #2", required=True)
    general.add_argument(
        "-o",  metavar="FILE", help="Output file", required=True)

    input_arg = parser.add_argument_group("Input files options")
    input_arg.add_argument(
        "--sort", action="store_true", help="Sort alphabetically the columns \
of the input files")
    input_arg.add_argument(
        "--skip1", metavar="CN", nargs="+", help="Names of the columns to \
remove from file #1 before the comparison. The columns are added back to the \
output file, to the right")
    input_arg.add_argument(
        "--skip2", metavar="CN", nargs="+", help="Names of the columns to \
remove from file #2 before the comparison. The columns are added back to the \
output file, to the right")
    input_arg.add_argument(
        "--drop1", metavar="CN", nargs="+", help="Names of the columns to \
remove from file #1 before the comparison. The columns are not added back to \
the output file.")
    input_arg.add_argument(
        "--drop2", metavar="CN", nargs="+", help="Names of the columns to \
remove from file #2 before the comparison. The columns are not added back to \
the output file.")

    merge = parser.add_argument_group("Merge options")
    merge.add_argument(
        "--case-insensitive", action="store_true", help="Use case insensitive \
comparisons. If two values differ only by case, the value from file #1 will \
be selected")
    merge.add_argument("--skip-empty", action="store_true", help="Ignore \
empty values: when only one of the conflicting cells is empty, the value of \
the other cell is automatically selected")
    merge.add_argument(
        "--always", default="", choices=["1", "2", "l", "s"], help="Adopt \
automatically the same decision for each conflict: '1' to always pick the \
value from file #1, '2' to pick the value from file #2, 'l' to pick the \
longest value, 's' to pick the shortest value")

    other_arg = parser.add_argument_group("Other options")
    other_arg.add_argument(
        "-h", "--help", action="help", help="Print this help message and exit")
    other_arg.add_argument(
        "-q", "--quiet", default=logging.DEBUG, action="store_const",
        dest="logging_level", const=logging.INFO,
        help="Activate quiet mode")
    other_arg.add_argument(
        "--no-color", action="store_true", help="Use asterisks to highlight \
the differences instead of the color red (ANSI escape sequences)")
    other_arg.add_argument(
        "--info", action="store_true", help="Print just the information about \
the input files and exit")
    other_arg.add_argument(
        "--delimiter", metavar="CHAR", default=",", help="Character used to \
separate the fields in the input and output files (default: ',')")

    parser_args = vars(parser.parse_args())

    # Configure logger with user defined logging level
    logging.basicConfig(
        level=parser_args["logging_level"], format="%(message)s")

    # Run main function
    c = CSVMerge(
        parser_args["i1"], parser_args["i2"], parser_args["o"],
        parser_args["always"], parser_args["sort"], parser_args["skip1"],
        parser_args["skip2"], parser_args["drop1"], parser_args["drop2"],
        parser_args["delimiter"], parser_args["case_insensitive"],
        parser_args["skip_empty"], parser_args["no_color"])

    if not parser_args["info"]:
        c.run()
