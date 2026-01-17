import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import csvmerge  # import ../csvmerge.py
import logging


def test(i1, i2, ref=None, always="", sort_cols_list=[False, True], skip1=[], skip2=[], skip_empty=False):
    error = False
    tmp_output = "out.csv"

    # Test drop options:
    # Convert to lists in order to use zip
    i1_list = [i1]
    i2_list = [i2]
    drop1 = [[]]
    drop2 = [[]]
    # i1 == '3r_3c.csv' <-> '3r_5c.csv' with drop1=last 2 cols
    # i1 == '5r_3c.csv' <-> '5r_5c.csv' with drop1=last 2 cols
    # i2 == '3r_3c.csv' <-> '3r_5c.csv' with drop2=last 2 cols
    # i2 == '5r_3c.csv' <-> '5r_5c.csv' with drop2=last 2 cols
    if (i1[-6:] == '3c.csv'):  # i1 == '3r_3c.csv' or i1 == '5r_3c.csv'
        i1_list.append(f'{i1[:2]}_5c.csv')  # append('3r_5c.csv') or append('5r_5c.csv')
        i2_list.append(i2)
        drop1.append(['header4', 'header5'])
        drop2.append([])
    if (i2[-6:] == '3c.csv'):  # i2 == '3r_3c.csv' or i2 == '5r_3c.csv'
        i1_list.append(i1)
        i2_list.append(f'{i2[:2]}_5c.csv')  # append('3r_5c.csv') or append('5r_5c.csv')
        drop1.append([])
        drop2.append(['header4', 'header5'])
    if (i1[-6:] == '3c.csv' and i2[-6:] == '3c.csv'):
        i1_list.append(f'{i1[:2]}_5c.csv')
        i2_list.append(f'{i2[:2]}_5c.csv')
        drop1.append(['header4', 'header5'])
        drop2.append(['header4', 'header5'])

    for i1_i2_d1_d2 in zip(i1_list, i2_list, drop1, drop2):
        for sort_cols in sort_cols_list:
            for case_insensitive in [False, True]:
                # Run function
                c = csvmerge.CSVMerge(i1_i2_d1_d2[0], i1_i2_d1_d2[1], tmp_output, always, sort_cols, skip1, skip2, i1_i2_d1_d2[2], i1_i2_d1_d2[3], ",", case_insensitive, skip_empty)
                c.run()

                # Check reference file
                if ref:
                    with open(tmp_output) as outputfile:
                        with open(ref) as referencefile:
                            if outputfile.read() != referencefile.read():
                                error = True

                # Remove output file
                os.remove(tmp_output)

                # Raise exception if error
                if error:
                    raise Exception(f"Error! {i1_i2_d1_d2[0]} vs {i1_i2_d1_d2[1]} != {ref}\n- always: {always}\n- sort cols: {sort_cols}\n- skip: {skip1} {skip2}\n- drop: {i1_i2_d1_d2[2]} {i1_i2_d1_d2[3]}\n- skip empty: {skip_empty}\n- case insensitive: {case_insensitive}")


def test_pop(in_list, indices, ref, removed_ref):
    in_list_copy = in_list.copy()
    removed = []
    csvmerge.pop_elements_from_list(in_list, indices, removed)
    if in_list != ref:
        raise Exception(f"Error! {in_list_copy} / {indices} -> list {in_list}, expected {ref}")
    if removed != removed_ref:
        raise Exception(f"Error! {in_list_copy} / {indices} -> removed {removed}, expected {removed_ref}")


def test_longest_shortest(string1, string2, l_ref, s_ref):
    longest, shortest = csvmerge.get_longest_shortest(string1, string2)
    if longest != l_ref:
        raise Exception(f"Error! Longest {longest}, expected {l_ref}")
    if shortest != s_ref:
        raise Exception(f"Error! Longest {shortest}, expected {s_ref}")


def main():
    # Set logger to quiet mode
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Main tests:

    # - Always x 5
    # -- Table dimensions x 4
    # --- Content x 2
    # ---- Skip columns x 4

    # To test the sort option:
    # - By default, all tests are run with False and True since the input files are already sorted
    # - Tests with 5r_5c_unsorted.csv and sort=True should behave as tests with 5r_5c.csv and sort=False

    # To test the drop options:
    # - By default, tests with *_5c.csv and drop=[header4,header5] should behave as tests with *_3c.csv

    # - No always option (same content only, no decision taken)
    # -- Same size
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv")
    # ---- Skip same columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip2_3r_3c_skip2.csv", "", [False, True], ['header2'], ['header2'])
    # -- Different number of rows (check rows tail)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "5r_3c.csv", "5r_3c.csv")
    test("5r_3c.csv", "3r_3c.csv", "5r_3c.csv")
    # -- Different number of columns (check cols tail)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv")
    test("3r_5c.csv", "3r_3c.csv", "3r_5c.csv")
    # ---- Skip same columns
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "", [False, True], ['header2'], ['header2'])
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip2_3r_3c_skip2.csv", "", [False, True], ['header2'], ['header2'])
    # ---- Skip different columns (columns not in common)
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", "", [False, True], [], ['header5'])
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", "", [False, True], [], ['header5', 'header4'])
    # -- Different number of rows and columns (check both tails)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv",          "5r_5c.csv",          "5r_5c.csv")
    test("3r_3c.csv",          "5r_5c_unsorted.csv", "5r_5c.csv", "", [True])
    test("5r_5c.csv",          "3r_3c.csv",          "5r_5c.csv")
    test("5r_5c_unsorted.csv", "3r_3c.csv",          "5r_5c.csv", "", [True])

    # - Always=1
    # -- Same size
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv", "1")
    # ---- Skip same columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip2_3r_3c_skip2.csv", "1", [False, True], ['header2'], ['header2'])
    # ---- Skip different columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip1_3r_3c_skip3.csv", "1", [False, True], ['header1'], ['header3'])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err.csv", "1")
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c.csv",     "1")
    # ---- Skip same columns
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err_skip2_3r_3c_skip2.csv", "1", [False, True], ['header2'], ['header2'])
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c_skip2_3r_3c_err_skip2.csv", "1", [False, True], ['header2'], ['header2'])
    # ---- Skip different columns
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err_skip1_3r_3c_skip3.csv", "1", [False, True], ['header1'], ['header3'])
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c_skip1_3r_3c_err_skip3.csv", "1", [False, True], ['header1'], ['header3'])
    # -- Different number of rows (check rows tail)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "5r_3c.csv", "5r_3c.csv", "1")
    test("5r_3c.csv", "3r_3c.csv", "5r_3c.csv", "1")
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "5r_3c.csv",     "5r_3c_err2.csv", "1")
    test("3r_3c.csv",     "5r_3c_err.csv", "5r_3c_err3.csv", "1")
    test("5r_3c_err.csv", "3r_3c.csv",     "5r_3c_err.csv",  "1")
    test("5r_3c.csv",     "3r_3c_err.csv", "5r_3c.csv",      "1")
    # -- Different number of columns (check cols tail)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", "1")
    test("3r_5c.csv", "3r_3c.csv", "3r_5c.csv", "1")
    # ---- Skip same columns
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "1", [False, True], ['header2'], ['header2'])
    test("3r_5c.csv", "3r_3c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "1", [False, True], ['header2'], ['header2'])
    # ---- Skip different columns (columns in common)
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip1_3r_5c_skip3.csv", "1", [False, True], ['header1'], ['header3'])
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip1_3r_3c_skip3.csv", "1", [False, True], ['header1'], ['header3'])
    # ---- Skip different columns (columns not in common)
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip4_3r_3c_skip3.csv", "1", [False, True], ['header4'], ['header3'])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_5c_err2.csv", "1")
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_5c_err3.csv", "1")
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err.csv",  "1")
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c.csv",      "1")
    # ---- Skip same columns
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_3c_err_skip2_3r_5c_skip2.csv", "1", [False, True], ['header2'], ['header2'])
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_3c_skip2_3r_5c_err_skip2.csv", "1", [False, True], ['header2'], ['header2'])
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip2_3r_3c_skip2.csv", "1", [False, True], ['header2'], ['header2'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip2_3r_3c_err_skip2.csv", "1", [False, True], ['header2'], ['header2'])
    # ---- Skip different columns (columns in common)
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_3c_err_skip1_3r_5c_skip3.csv", "1", [False, True], ['header1'], ['header3'])
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_3c_skip1_3r_5c_err_skip3.csv", "1", [False, True], ['header1'], ['header3'])
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip1_3r_3c_skip3.csv", "1", [False, True], ['header1'], ['header3'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip1_3r_3c_err_skip3.csv", "1", [False, True], ['header1'], ['header3'])
    # ---- Skip different columns (columns not in common)
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip4_3r_3c_skip3.csv", "1", [False, True], ['header4'], ['header3'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip4_3r_3c_err_skip3.csv", "1", [False, True], ['header4'], ['header3'])
    # -- Different number of rows and columns (check both tails)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv",          "5r_5c.csv",          "5r_5c.csv", "1")
    test("3r_3c.csv",          "5r_5c_unsorted.csv", "5r_5c.csv", "1", [True])
    test("5r_5c.csv",          "3r_3c.csv",          "5r_5c.csv", "1")
    test("5r_5c_unsorted.csv", "3r_3c.csv",          "5r_5c.csv", "1", [True])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv",      "5r_5c.csv",          "5r_5c_err2.csv", "1")
    test("3r_3c_err.csv",      "5r_5c_unsorted.csv", "5r_5c_err2.csv", "1", [True])
    test("3r_3c.csv",          "5r_5c_err.csv",      "5r_5c_err3.csv", "1")
    test("5r_5c_err.csv",      "3r_3c.csv",          "5r_5c_err.csv",  "1")
    test("5r_5c.csv",          "3r_3c_err.csv",      "5r_5c.csv",      "1")
    test("5r_5c_unsorted.csv", "3r_3c_err.csv",      "5r_5c.csv",      "1", [True])

    # - Always=2
    # -- Same size
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv", "2")
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c.csv",     "2")
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c_err.csv", "2")
    # -- Different number of rows (check rows tail)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "5r_3c.csv", "5r_3c.csv", "2")
    test("5r_3c.csv", "3r_3c.csv", "5r_3c.csv", "2")
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "5r_3c.csv",     "5r_3c.csv",      "2")
    test("3r_3c.csv",     "5r_3c_err.csv", "5r_3c_err.csv",  "2")
    test("5r_3c_err.csv", "3r_3c.csv",     "5r_3c_err3.csv", "2")
    test("5r_3c.csv",     "3r_3c_err.csv", "5r_3c_err2.csv", "2")
    # -- Different number of columns (check cols tail)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", "2")
    test("3r_5c.csv", "3r_3c.csv", "3r_5c.csv", "2")
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_5c.csv",      "2")
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_5c_err.csv",  "2")
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err3.csv", "2")
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_err2.csv", "2")
    # -- Different number of rows and columns (check both tails)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv",          "5r_5c.csv",          "5r_5c.csv", "2")
    test("3r_3c.csv",          "5r_5c_unsorted.csv", "5r_5c.csv", "2", [True])
    test("5r_5c.csv",          "3r_3c.csv",          "5r_5c.csv", "2")
    test("5r_5c_unsorted.csv", "3r_3c.csv",          "5r_5c.csv", "2", [True])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv",      "5r_5c.csv",          "5r_5c.csv",      "2")
    test("3r_3c_err.csv",      "5r_5c_unsorted.csv", "5r_5c.csv",      "2", [True])
    test("3r_3c.csv",          "5r_5c_err.csv",      "5r_5c_err.csv",  "2")
    test("5r_5c_err.csv",      "3r_3c.csv",          "5r_5c_err3.csv", "2")
    test("5r_5c.csv",          "3r_3c_err.csv",      "5r_5c_err2.csv", "2")
    test("5r_5c_unsorted.csv", "3r_3c_err.csv",      "5r_5c_err2.csv", "2", [True])

    # - Always=l/s (error cells are the longest)
    # -- Same size
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv", "l")
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv", "s")
    # ---- Skip same columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip2_3r_3c_skip2.csv", "l", [False, True], ['header2'], ['header2'])
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip2_3r_3c_skip2.csv", "s", [False, True], ['header2'], ['header2'])
    # ---- Skip different columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip1_3r_3c_skip3.csv", "l", [False, True], ['header1'], ['header3'])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err.csv", "l")
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c.csv",     "s")
    # ---- Skip same columns
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err_skip2_3r_3c_skip2.csv", "l", [False, True], ['header2'], ['header2'])
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c_skip2_3r_3c_err_skip2.csv", "s", [False, True], ['header2'], ['header2'])
    # ---- Skip different columns
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err_skip1_3r_3c_skip3.csv", "l", [False, True], ['header1'], ['header3'])
    # -- Different number of rows (check rows tail)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "5r_3c.csv", "5r_3c.csv", "l")
    test("3r_3c.csv", "5r_3c.csv", "5r_3c.csv", "s")
    test("5r_3c.csv", "3r_3c.csv", "5r_3c.csv", "l")
    test("5r_3c.csv", "3r_3c.csv", "5r_3c.csv", "s")
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "5r_3c.csv",     "5r_3c_err2.csv", "l")
    test("3r_3c.csv",     "5r_3c_err.csv", "5r_3c_err3.csv", "s")
    test("5r_3c_err.csv", "3r_3c.csv",     "5r_3c_err.csv",  "l")
    test("5r_3c.csv",     "3r_3c_err.csv", "5r_3c.csv",      "s")
    # -- Different number of columns (check cols tail)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", "l")
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", "s")
    test("3r_5c.csv", "3r_3c.csv", "3r_5c.csv", "l")
    test("3r_5c.csv", "3r_3c.csv", "3r_5c.csv", "s")
    # ---- Skip same columns
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "l", [False, True], ['header2'], ['header2'])
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "s", [False, True], ['header2'], ['header2'])
    test("3r_5c.csv", "3r_3c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "l", [False, True], ['header2'], ['header2'])
    test("3r_5c.csv", "3r_3c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "s", [False, True], ['header2'], ['header2'])
    # ---- Skip different columns (columns in common)
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip1_3r_5c_skip3.csv", "l", [False, True], ['header1'], ['header3'])
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip1_3r_3c_skip3.csv", "l", [False, True], ['header1'], ['header3'])
    # ---- Skip different columns (columns not in common)
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip4_3r_3c_skip3.csv", "l", [False, True], ['header4'], ['header3'])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_5c_err2.csv", "l")
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_5c_err3.csv", "s")
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err.csv",  "l")
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c.csv",      "s")
    # ---- Skip same columns
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_3c_err_skip2_3r_5c_skip2.csv", "l", [False, True], ['header2'], ['header2'])
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_3c_skip2_3r_5c_err_skip2.csv", "s", [False, True], ['header2'], ['header2'])
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip2_3r_3c_skip2.csv", "l", [False, True], ['header2'], ['header2'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip2_3r_3c_err_skip2.csv", "s", [False, True], ['header2'], ['header2'])
    # ---- Skip different columns (columns in common)
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_3c_err_skip1_3r_5c_skip3.csv", "l", [False, True], ['header1'], ['header3'])
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip1_3r_3c_skip3.csv", "l", [False, True], ['header1'], ['header3'])
    # ---- Skip different columns (columns not in common)
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip4_3r_3c_skip3.csv", "l", [False, True], ['header4'], ['header3'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip4_3r_3c_err_skip3.csv", "s", [False, True], ['header4'], ['header3'])
    # -- Different number of rows and columns (check both tails)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv",          "5r_5c.csv",          "5r_5c.csv", "l")
    test("3r_3c.csv",          "5r_5c_unsorted.csv", "5r_5c.csv", "l", [True])
    test("3r_3c.csv",          "5r_5c.csv",          "5r_5c.csv", "s")
    test("3r_3c.csv",          "5r_5c_unsorted.csv", "5r_5c.csv", "s", [True])
    test("5r_5c.csv",          "3r_3c.csv",          "5r_5c.csv", "l")
    test("5r_5c_unsorted.csv", "3r_3c.csv",          "5r_5c.csv", "l", [True])
    test("3r_3c.csv",          "5r_5c.csv",          "5r_5c.csv", "s")
    test("3r_3c.csv",          "5r_5c_unsorted.csv", "5r_5c.csv", "s", [True])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv",      "5r_5c.csv",          "5r_5c_err2.csv", "l")
    test("3r_3c_err.csv",      "5r_5c_unsorted.csv", "5r_5c_err2.csv", "l", [True])
    test("3r_3c.csv",          "5r_5c_err.csv",      "5r_5c_err3.csv", "s")
    test("5r_5c_err.csv",      "3r_3c.csv",          "5r_5c_err.csv",  "l")
    test("5r_5c.csv",          "3r_3c_err.csv",      "5r_5c.csv",      "s")
    test("5r_5c_unsorted.csv", "3r_3c_err.csv",      "5r_5c.csv",      "s", [True])

    # Empty cells tests
    # - Same size
    test("3r_3c.csv", "3r_3c_empty.csv", "3r_3c.csv",       "1")
    test("3r_3c.csv", "3r_3c_empty.csv", "3r_3c.csv",       "l")
    test("3r_3c.csv", "3r_3c_empty.csv", "3r_3c_empty.csv", "2")
    test("3r_3c.csv", "3r_3c_empty.csv", "3r_3c_empty.csv", "s")
    test("3r_3c.csv", "3r_3c_empty.csv", "3r_3c.csv",       "", [False, True], [], [], True)
    test("3r_3c_empty.csv", "3r_3c.csv", "3r_3c.csv",       "", [False, True], [], [], True)
    # - Different number of rows and columns
    test("3r_3c.csv",          "5r_5c_empty.csv", "3r_3c_5r_5c_empty.csv", "1")
    test("3r_3c.csv",          "5r_5c_empty.csv", "5r_5c_empty.csv",       "2")
    test("5r_5c.csv",          "3r_3c_empty.csv", "5r_5c.csv",             "1")
    test("5r_5c_unsorted.csv", "3r_3c_empty.csv", "5r_5c.csv",             "1", [True])
    test("5r_5c.csv",          "3r_3c_empty.csv", "3r_3c_empty_5r_5c.csv", "2")
    test("5r_5c_unsorted.csv", "3r_3c_empty.csv", "3r_3c_empty_5r_5c.csv", "2", [True])
    test("5r_5c.csv",          "3r_3c_empty.csv", "5r_5c.csv",             "",  [False, True], [], [], True)
    test("5r_5c_unsorted.csv", "3r_3c_empty.csv", "5r_5c.csv",             "",  [True],        [], [], True)

    # Tests for pop_elements_from_list function:
    test_pop(['a', 'b', 'c', 'd', 'e'], [], ['a', 'b', 'c', 'd', 'e'], [])
    test_pop(['a', 'b', 'c', 'd', 'e'], [0], ['b', 'c', 'd', 'e'], ['a'])
    test_pop(['a', 'b', 'c', 'd', 'e'], [1, 3], ['a', 'c', 'e'], ['b', 'd'])
    test_pop(['a', 'b', 'c', 'd', 'e'], [0, 2, 4], ['b', 'd'], ['a', 'c', 'e'])
    test_pop(['a', 'b', 'c', 'd', 'e'], [0, 1, 2, 3, 4], [], ['a', 'b', 'c', 'd', 'e'])
    test_pop(['a'], [0], [], ['a'])
    test_pop(['a'], [], ['a'], [])
    test_pop([], [], [], [])

    # Tests for get_longest_shortest function:
    test_longest_shortest("longestword", "short", "longestword", "short")
    test_longest_shortest("short", "longestword", "longestword", "short")
    test_longest_shortest("a", "", "a", "")
    test_longest_shortest("", "a", "a", "")
    test_longest_shortest("samelen1", "samelen2", "samelen1", "samelen2")
    test_longest_shortest("same", "same", "same", "same")


if __name__ == "__main__":
    main()
