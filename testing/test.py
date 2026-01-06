import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import csvmerge  # import ../csvmerge.py


def test(i1, i2, ref=None, always=0):
    # Run function
    tmp_output = "out.csv"
    csvmerge.csvmerge(i1, i2, tmp_output, always)

    # Check reference file
    if ref:
        error = False
        with open(tmp_output) as outputfile:
            with open(ref) as referencefile:
                if outputfile.read() != referencefile.read():
                    error = True
        os.remove(tmp_output)
        if error:
            raise Exception(f"Error! {i1} vs {i2} != {ref}")


# TODO files with empty cells
def main():
    # - No always option (same content only, no decision taken)
    # -- Same size
    # --- Same content
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv")
    # -- Different number of rows (check rows tail)
    # --- Same content
    test("3r_3c.csv", "5r_3c.csv", "5r_3c.csv")
    test("5r_3c.csv", "3r_3c.csv", "5r_3c.csv")
    # -- Different number of columns (check cols tail)
    # --- Same content
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv")
    test("3r_5c.csv", "3r_3c.csv", "3r_5c.csv")
    # -- Different number of rows and columns (check both tails)
    # --- Same content
    test("3r_3c.csv", "5r_5c.csv", "5r_5c.csv")
    test("5r_5c.csv", "3r_3c.csv", "5r_5c.csv")

    # - Always=1
    # -- Same size
    # --- Same content
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv", 1)
    # --- Different content
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c_err.csv", 1)
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c.csv",     1)
    # -- Different number of rows (check rows tail)
    # --- Same content
    test("3r_3c.csv", "5r_3c.csv", "5r_3c.csv", 1)
    test("5r_3c.csv", "3r_3c.csv", "5r_3c.csv", 1)
    # --- Different content
    test("3r_3c_err.csv", "5r_3c.csv",     "5r_3c_err2.csv", 1)
    test("3r_3c.csv",     "5r_3c_err.csv", "5r_3c_err3.csv", 1)
    test("5r_3c_err.csv", "3r_3c.csv",     "5r_3c_err.csv",  1)
    test("5r_3c.csv",     "3r_3c_err.csv", "5r_3c.csv",      1)
    # -- Different number of columns (check cols tail)
    # --- Same content
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", 1)
    test("3r_5c.csv", "3r_3c.csv", "3r_5c.csv", 1)
    # --- Different content
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_5c_err2.csv", 1)
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_5c_err3.csv", 1)
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err.csv",  1)
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c.csv",      1)
    # -- Different number of rows and columns (check both tails)
    # --- Same content
    test("3r_3c.csv", "5r_5c.csv", "5r_5c.csv", 1)
    test("5r_5c.csv", "3r_3c.csv", "5r_5c.csv", 1)
    # --- Different content
    test("3r_3c_err.csv", "5r_5c.csv",     "5r_5c_err2.csv", 1)
    test("3r_3c.csv",     "5r_5c_err.csv", "5r_5c_err3.csv", 1)
    test("5r_5c_err.csv", "3r_3c.csv",     "5r_5c_err.csv",  1)
    test("5r_5c.csv",     "3r_3c_err.csv", "5r_5c.csv",      1)

    # - Always=2
    # -- Same size
    # --- Same content
    test("3r_3c.csv", "3r_3c.csv", "3r_3c.csv", 2)
    # --- Different content
    test("3r_3c_err.csv", "3r_3c.csv",     "3r_3c.csv",     2)
    test("3r_3c.csv",     "3r_3c_err.csv", "3r_3c_err.csv", 2)
    # -- Different number of rows (check rows tail)
    # --- Same content
    test("3r_3c.csv", "5r_3c.csv", "5r_3c.csv", 2)
    test("5r_3c.csv", "3r_3c.csv", "5r_3c.csv", 2)
    # --- Different content
    test("3r_3c_err.csv", "5r_3c.csv",     "5r_3c.csv",      2)
    test("3r_3c.csv",     "5r_3c_err.csv", "5r_3c_err.csv",  2)
    test("5r_3c_err.csv", "3r_3c.csv",     "5r_3c_err3.csv", 2)
    test("5r_3c.csv",     "3r_3c_err.csv", "5r_3c_err2.csv", 2)
    # -- Different number of columns (check cols tail)
    # --- Same content
    test("3r_3c.csv", "3r_5c.csv", "3r_5c.csv", 2)
    test("3r_5c.csv", "3r_3c.csv", "3r_5c.csv", 2)
    # --- Different content
    test("3r_3c_err.csv", "3r_5c.csv",     "3r_5c.csv",      2)
    test("3r_3c.csv",     "3r_5c_err.csv", "3r_5c_err.csv",  2)
    test("3r_5c_err.csv", "3r_3c.csv",     "3r_5c_err3.csv", 2)
    test("3r_5c.csv",     "3r_3c_err.csv", "3r_5c_err2.csv", 2)
    # -- Different number of rows and columns (check both tails)
    # --- Same content
    test("3r_3c.csv", "5r_5c.csv", "5r_5c.csv", 2)
    test("5r_5c.csv", "3r_3c.csv", "5r_5c.csv", 2)
    # --- Different content
    test("3r_3c_err.csv", "5r_5c.csv",     "5r_5c.csv",      2)
    test("3r_3c.csv",     "5r_5c_err.csv", "5r_5c_err.csv",  2)
    test("5r_5c_err.csv", "3r_3c.csv",     "5r_5c_err3.csv", 2)
    test("5r_5c.csv",     "3r_3c_err.csv", "5r_5c_err2.csv", 2)


if __name__ == "__main__":
    main()
