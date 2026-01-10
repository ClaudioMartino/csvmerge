# csvmerge: an interactive merge tool for .csv files

This is an interactive merge tool specifically designed for .csv files and written in Python. It performs a line-by-line comparison and when it detects a conflict it prompts the user to select the source file from which to pick the preferred value.

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)

## Basic usage

Run the script as:

```
python3 csvmerge.py -i1 <input-file-1> -i2 <input-file-2> -o <output-file>
```

In case of conflict the user is prompted to select the source file: they need to press `1` for file n. 1 or `2` for file n. 2, and confirm the choice with `<Enter>`.

If the user realizes that a specific conflict is going to recur consistently, they can automate their decision by entering `1+` or `2+`. This adds the choice to a list of automatic responses, preventing future prompts for that conflict. A series of asterisks on the screen indicates the total number of automatic choices that have been saved.

## Other options

* Use `--always <id>` if you already know what to do in case of conflict and you don't need to interact with the tool:
  * `--always 1` to always pick the value from file n. 1.
  * `--always 2` to always pick the value from file n. 2.
  * `--always l` to always pick the longest value. If the two values have the same length, the value from file n. 1 will be selected.
  * `--always s` to always pick the shortest value. If the two values have the same length, the value from file n. 1 will be selected.
* Use `--skip1 <column-name>` and `--skip2 <column-name>` to remove the specified columns from the comparison. You can specify multiple columns for both files. Removed columns are added back to the output file, on the right, file n. 1 before file n. 2. This option is useful when the two files share some, but not all, columns.
* Use `--delimiter <char>` to specify the character used to separate the values in the .csv files. It defaults to `,`.
* Use `--skip-empty` to ignore empty values. If only one of the conflicting cells is empty, the value of the other cell will be automatically selected.
* Use `--case-insensitive` to perform case-insensitive comparisons. If two values differ only by case, the value from file n. 1 will be selected.
* Use `--info` to display the information about the input files and exit.
* Use `--no-color` to highlight the differences using asterisks rather than red ANSI formatting.

All these options can be displayed by running the helper with `-h`.

## Contributing

Contributions are most welcome by forking the repository and sending a pull request. Errors and new features proposals can be reported opening an issue as well.
