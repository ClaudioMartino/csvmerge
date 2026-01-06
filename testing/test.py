import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import csvmerge  # import ../csvmerge.py


def test(i1, i2, ref=None, always=0, skip1=[], skip2=[]):
    error = False
    tmp_output = "out.csv"

    # Run function
    csvmerge.csvmerge(i1, i2, tmp_output, always, skip1, skip2)

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
        raise Exception(f"Error! {i1} vs {i2} != {ref}")


# TODO files with empty cells

# - Always x 3
# -- Table dimensions x 4
# --- Content x 2
# ---- Skip columns x 4

def main():
    # - No always option (same content only, no decision taken)
    # -- Same size
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv")
    # ---- Skip same columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip2_3r_3c_skip2.csv", 0, ['header2'], ['header2'])
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
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip2_3r_5c_skip2.csv", 0, ['header2'], ['header2'])
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip2_3r_3c_skip2.csv", 0, ['header2'], ['header2'])
    # ---- Skip different columns (columns not in common)
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", 0, [], ['header5'])
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", 0, [], ['header5', 'header4'])
    # -- Different number of rows and columns (check both tails)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "5r_5c.csv", "5r_5c.csv")
    test("5r_5c.csv", "3r_3c.csv", "5r_5c.csv")

    # - Always=1
    # -- Same size
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv", 1)
    # ---- Skip same columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip2_3r_3c_skip2.csv", 1, ['header2'], ['header2'])
    # ---- Skip different columns
    test("3r_3c.csv", "3r_3c.csv", "3r_3c_skip1_3r_3c_skip3.csv", 1, ['header1'], ['header3'])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err.csv", 1)
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c.csv",     1)
    # ---- Skip same columns
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err_skip2_3r_3c_skip2.csv", 1, ['header2'], ['header2'])
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c_skip2_3r_3c_err_skip2.csv", 1, ['header2'], ['header2'])
    # ---- Skip different columns
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err_skip1_3r_3c_skip3.csv", 1, ['header1'], ['header3'])
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c_skip1_3r_3c_err_skip3.csv", 1, ['header1'], ['header3'])
    # -- Different number of rows (check rows tail)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "5r_3c.csv", "5r_3c.csv", 1)
    test("5r_3c.csv", "3r_3c.csv", "5r_3c.csv", 1)
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "5r_3c.csv",     "5r_3c_err2.csv", 1)
    test("3r_3c.csv",     "5r_3c_err.csv", "5r_3c_err3.csv", 1)
    test("5r_3c_err.csv", "3r_3c.csv",     "5r_3c_err.csv",  1)
    test("5r_3c.csv",     "3r_3c_err.csv", "5r_3c.csv",      1)
    # -- Different number of columns (check cols tail)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", 1)
    test("3r_5c.csv", "3r_3c.csv", "3r_5c.csv", 1)
    # ---- Skip same columns
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip2_3r_5c_skip2.csv", 1, ['header2'], ['header2'])
    test("3r_5c.csv", "3r_3c.csv", "3r_3c_skip2_3r_5c_skip2.csv", 1, ['header2'], ['header2'])
    # ---- Skip different columns (columns in common)
    test("3r_3c.csv", "3r_5c.csv", "3r_3c_skip1_3r_5c_skip3.csv", 1, ['header1'], ['header3'])
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip1_3r_3c_skip3.csv", 1, ['header1'], ['header3'])
    # ---- Skip different columns (columns not in common)
    test("3r_5c.csv", "3r_3c.csv", "3r_5c_skip4_3r_3c_skip3.csv", 1, ['header4'], ['header3'])
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_5c_err2.csv", 1)
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_5c_err3.csv", 1)
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err.csv",  1)
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c.csv",      1)
    # ---- Skip same columns
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_3c_err_skip2_3r_5c_skip2.csv", 1, ['header2'], ['header2'])
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_3c_skip2_3r_5c_err_skip2.csv", 1, ['header2'], ['header2'])
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip2_3r_3c_skip2.csv", 1, ['header2'], ['header2'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip2_3r_3c_err_skip2.csv", 1, ['header2'], ['header2'])
    # ---- Skip different columns (columns in common)
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_3c_err_skip1_3r_5c_skip3.csv", 1, ['header1'], ['header3'])
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_3c_skip1_3r_5c_err_skip3.csv", 1, ['header1'], ['header3'])
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip1_3r_3c_skip3.csv", 1, ['header1'], ['header3'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip1_3r_3c_err_skip3.csv", 1, ['header1'], ['header3'])
    # ---- Skip different columns (columns not in common)
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err_skip4_3r_3c_skip3.csv", 1, ['header4'], ['header3'])
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_skip4_3r_3c_err_skip3.csv", 1, ['header4'], ['header3'])

    # -- Different number of rows and columns (check both tails)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "5r_5c.csv", "5r_5c.csv", 1)
    test("5r_5c.csv", "3r_3c.csv", "5r_5c.csv", 1)
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "5r_5c.csv",     "5r_5c_err2.csv", 1)
    test("3r_3c.csv",     "5r_5c_err.csv", "5r_5c_err3.csv", 1)
    test("5r_5c_err.csv", "3r_3c.csv",     "5r_5c_err.csv",  1)
    test("5r_5c.csv",     "3r_3c_err.csv", "5r_5c.csv",      1)

    # - Always=2
    # -- Same size
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv", 2)
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c.csv",     2)
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c_err.csv", 2)
    # -- Different number of rows (check rows tail)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "5r_3c.csv", "5r_3c.csv", 2)
    test("5r_3c.csv", "3r_3c.csv", "5r_3c.csv", 2)
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "5r_3c.csv",     "5r_3c.csv",      2)
    test("3r_3c.csv",     "5r_3c_err.csv", "5r_3c_err.csv",  2)
    test("5r_3c_err.csv", "3r_3c.csv",     "5r_3c_err3.csv", 2)
    test("5r_3c.csv",     "3r_3c_err.csv", "5r_3c_err2.csv", 2)
    # -- Different number of columns (check cols tail)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", 2)
    test("3r_5c.csv", "3r_3c.csv", "3r_5c.csv", 2)
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_5c.csv",      2)
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_5c_err.csv",  2)
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err3.csv", 2)
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_err2.csv", 2)
    # -- Different number of rows and columns (check both tails)
    # --- Same content
    # ---- Don't skip
    test("3r_3c.csv", "5r_5c.csv", "5r_5c.csv", 2)
    test("5r_5c.csv", "3r_3c.csv", "5r_5c.csv", 2)
    # --- Different content
    # ---- Don't skip
    test("3r_3c_err.csv", "5r_5c.csv",     "5r_5c.csv",      2)
    test("3r_3c.csv",     "5r_5c_err.csv", "5r_5c_err.csv",  2)
    test("5r_5c_err.csv", "3r_3c.csv",     "5r_5c_err3.csv", 2)
    test("5r_5c.csv",     "3r_3c_err.csv", "5r_5c_err2.csv", 2)


if __name__ == "__main__":
    main()
