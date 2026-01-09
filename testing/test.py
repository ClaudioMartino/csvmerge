import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import csvmerge  # import ../csvmerge.py


def test(i1, i2, ref=None, always="", skip1=[], skip2=[], skip_empty=False):
    error = False
    tmp_output = "out.csv"

    for case_insensitive in [False, True]:
        # Run function
        csvmerge.csvmerge(i1, i2, tmp_output, always, skip1, skip2, ",", case_insensitive, skip_empty)

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
            raise Exception(f"Error! {i1} vs {i2} != {ref} (always: {always}, skip empty: {skip_empty}, case insensitive: {case_insensitive})")


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
    # Main tests:

    # - Always x 5
    # -- Table dimensions x 4
    # --- Content x 2
    # ---- Skip columns x 4

    # - No always option (same content only, no decision taken)
    # -- Same size
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv")
    # ---- Skip same columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip2_3r_3c_skip2.csv", "", ['header2'], ['header2'])
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
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "", ['header2'], ['header2'])
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip2_3r_3c_skip2.csv", "", ['header2'], ['header2'])
    # ---- Skip different columns (columns not in common)
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", "", [], ['header5'])
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", "", [], ['header5', 'header4'])
    # -- Different number of rows and columns (check both tails)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "5r_5c.csv", "5r_5c.csv")
    test("5r_5c.csv", "3r_3c.csv", "5r_5c.csv")

    # - Always=1
    # -- Same size
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv", "1")
    # ---- Skip same columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip2_3r_3c_skip2.csv", "1", ['header2'], ['header2'])
    # ---- Skip different columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip1_3r_3c_skip3.csv", "1", ['header1'], ['header3'])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err.csv", "1")
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c.csv",     "1")
    # ---- Skip same columns
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err_skip2_3r_3c_skip2.csv", "1", ['header2'], ['header2'])
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c_skip2_3r_3c_err_skip2.csv", "1", ['header2'], ['header2'])
    # ---- Skip different columns
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err_skip1_3r_3c_skip3.csv", "1", ['header1'], ['header3'])
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c_skip1_3r_3c_err_skip3.csv", "1", ['header1'], ['header3'])
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
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "1", ['header2'], ['header2'])
    test("3r_5c.csv", "3r_3c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "1", ['header2'], ['header2'])
    # ---- Skip different columns (columns in common)
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip1_3r_5c_skip3.csv", "1", ['header1'], ['header3'])
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip1_3r_3c_skip3.csv", "1", ['header1'], ['header3'])
    # ---- Skip different columns (columns not in common)
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip4_3r_3c_skip3.csv", "1", ['header4'], ['header3'])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_5c_err2.csv", "1")
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_5c_err3.csv", "1")
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err.csv",  "1")
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c.csv",      "1")
    # ---- Skip same columns
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_3c_err_skip2_3r_5c_skip2.csv", "1", ['header2'], ['header2'])
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_3c_skip2_3r_5c_err_skip2.csv", "1", ['header2'], ['header2'])
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip2_3r_3c_skip2.csv", "1", ['header2'], ['header2'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip2_3r_3c_err_skip2.csv", "1", ['header2'], ['header2'])
    # ---- Skip different columns (columns in common)
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_3c_err_skip1_3r_5c_skip3.csv", "1", ['header1'], ['header3'])
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_3c_skip1_3r_5c_err_skip3.csv", "1", ['header1'], ['header3'])
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip1_3r_3c_skip3.csv", "1", ['header1'], ['header3'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip1_3r_3c_err_skip3.csv", "1", ['header1'], ['header3'])
    # ---- Skip different columns (columns not in common)
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip4_3r_3c_skip3.csv", "1", ['header4'], ['header3'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip4_3r_3c_err_skip3.csv", "1", ['header4'], ['header3'])
    # -- Different number of rows and columns (check both tails)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "5r_5c.csv", "5r_5c.csv", "1")
    test("5r_5c.csv", "3r_3c.csv", "5r_5c.csv", "1")
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "5r_5c.csv",     "5r_5c_err2.csv", "1")
    test("3r_3c.csv",     "5r_5c_err.csv", "5r_5c_err3.csv", "1")
    test("5r_5c_err.csv", "3r_3c.csv",     "5r_5c_err.csv",  "1")
    test("5r_5c.csv",     "3r_3c_err.csv", "5r_5c.csv",      "1")

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
    test("3r_3c.csv", "5r_5c.csv", "5r_5c.csv", "2")
    test("5r_5c.csv", "3r_3c.csv", "5r_5c.csv", "2")
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "5r_5c.csv",     "5r_5c.csv",      "2")
    test("3r_3c.csv",     "5r_5c_err.csv", "5r_5c_err.csv",  "2")
    test("5r_5c_err.csv", "3r_3c.csv",     "5r_5c_err3.csv", "2")
    test("5r_5c.csv",     "3r_3c_err.csv", "5r_5c_err2.csv", "2")

    # - Always=l/s (error cells are the longest)
    # -- Same size
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv", "l")
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv", "s")
    # ---- Skip same columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip2_3r_3c_skip2.csv", "l", ['header2'], ['header2'])
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip2_3r_3c_skip2.csv", "s", ['header2'], ['header2'])
    # ---- Skip different columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip1_3r_3c_skip3.csv", "l", ['header1'], ['header3'])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err.csv", "l")
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c.csv",     "s")
    # ---- Skip same columns
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err_skip2_3r_3c_skip2.csv", "l", ['header2'], ['header2'])
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c_skip2_3r_3c_err_skip2.csv", "s", ['header2'], ['header2'])
    # ---- Skip different columns
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err_skip1_3r_3c_skip3.csv", "l", ['header1'], ['header3'])
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
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "l", ['header2'], ['header2'])
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "s", ['header2'], ['header2'])
    test("3r_5c.csv", "3r_3c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "l", ['header2'], ['header2'])
    test("3r_5c.csv", "3r_3c.csv", "3r_3c_skip2_3r_5c_skip2.csv", "s", ['header2'], ['header2'])
    # ---- Skip different columns (columns in common)
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip1_3r_5c_skip3.csv", "l", ['header1'], ['header3'])
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip1_3r_3c_skip3.csv", "l", ['header1'], ['header3'])
    # ---- Skip different columns (columns not in common)
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip4_3r_3c_skip3.csv", "l", ['header4'], ['header3'])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_5c_err2.csv", "l")
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_5c_err3.csv", "s")
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err.csv",  "l")
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c.csv",      "s")
    # ---- Skip same columns
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_3c_err_skip2_3r_5c_skip2.csv", "l", ['header2'], ['header2'])
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_3c_skip2_3r_5c_err_skip2.csv", "s", ['header2'], ['header2'])
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip2_3r_3c_skip2.csv", "l", ['header2'], ['header2'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip2_3r_3c_err_skip2.csv", "s", ['header2'], ['header2'])
    # ---- Skip different columns (columns in common)
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_3c_err_skip1_3r_5c_skip3.csv", "l", ['header1'], ['header3'])
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip1_3r_3c_skip3.csv", "l", ['header1'], ['header3'])
    # ---- Skip different columns (columns not in common)
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip4_3r_3c_skip3.csv", "l", ['header4'], ['header3'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip4_3r_3c_err_skip3.csv", "s", ['header4'], ['header3'])
    # -- Different number of rows and columns (check both tails)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "5r_5c.csv", "5r_5c.csv", "l")
    test("3r_3c.csv", "5r_5c.csv", "5r_5c.csv", "s")
    test("5r_5c.csv", "3r_3c.csv", "5r_5c.csv", "l")
    test("3r_3c.csv", "5r_5c.csv", "5r_5c.csv", "s")
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "5r_5c.csv",     "5r_5c_err2.csv", "l")
    test("3r_3c.csv",     "5r_5c_err.csv", "5r_5c_err3.csv", "s")
    test("5r_5c_err.csv", "3r_3c.csv",     "5r_5c_err.csv",  "l")
    test("5r_5c.csv",     "3r_3c_err.csv", "5r_5c.csv",      "s")

    # Empty cells tests
    # - Same size
    test("3r_3c.csv", "3r_3c_empty.csv", "3r_3c.csv",       "1")
    test("3r_3c.csv", "3r_3c_empty.csv", "3r_3c.csv",       "l")
    test("3r_3c.csv", "3r_3c_empty.csv", "3r_3c_empty.csv", "2")
    test("3r_3c.csv", "3r_3c_empty.csv", "3r_3c_empty.csv", "s")
    test("3r_3c.csv", "3r_3c_empty.csv", "3r_3c.csv",       "", [], [], True)
    test("3r_3c_empty.csv", "3r_3c.csv", "3r_3c.csv",       "", [], [], True)
    # - Different number of rows and columns
    test("3r_3c.csv", "5r_5c_empty.csv", "3r_3c_5r_5c_empty.csv", "1")
    test("3r_3c.csv", "5r_5c_empty.csv", "5r_5c_empty.csv",       "2")
    test("5r_5c.csv", "3r_3c_empty.csv", "5r_5c.csv",             "1")
    test("5r_5c.csv", "3r_3c_empty.csv", "3r_3c_empty_5r_5c.csv", "2")
    test("5r_5c.csv", "3r_3c_empty.csv", "5r_5c.csv",             "", [], [], True)

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
