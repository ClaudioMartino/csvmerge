# csvmerge: an interactive merge tool for .csv files

This is an interactive merge tool specifically designed for .csv files and written in Python. It performs a line-by-line comparison and when it detects a conflict it prompts the user to select the source file from which to pick the preferred value.

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)

## Basic usage

```
python3 csvmerge.py -i1 <input-file-1> -i2 <input-file-2> -o <output-file>
```

## Other options

* Use `--always <id>` if you already know what to do in case of conflict and you don't need to interact with the tool:
  * `--always 1` to always pick the value from file n. 1.
  * `--always 2` to always pick the value from file n. 2.
  * `--always l` to always pick the longest value. If the two values have the same length, the value from file n. 1 will be selected.
  * `--always s` to always pick the shortest value. If the two values have the same length, the value from file n. 1 will be selected.
* Use `--skip1 <column-name>` and `--skip2 <column-name>` to remove the specified columns from the comparison. You can specify multiple columns for both files. Removed columns are added back to the output file, on the right, file n. 1 before file n. 2. This option is useful when the two files share some, but not all, columns.
* Use `--delimiter <char>` to specify the character used to separate the values in the .csv files. It defaults to `,`.
* Use `--caseinsensitive` to perform case-insensitive comparisons. If two values differ only by case, the value from file n. 1 will be selected.
* Use `--nocolor` to highlight the differences using asterisks rather than red ANSI formatting.

All these options can be displayed by running the helper with `-h`.

## Contributing

Contributions are most welcome by forking the repository and sending a pull request. Errors and new features proposals can be reported opening an issue as well.
