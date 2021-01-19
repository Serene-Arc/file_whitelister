# File Whitelister

This is a simple tool that will compare the contents of a directory against a list of files and will output the name of any files that are *not* in that whitelist. It is pretty simple and designed to be easily piped in a shell if required.

The tool can use a Levenshtein distance to find close matches to the whitelist of a type that regex cannot. In short, the Levenshtein distance is the number of transforms needed to transform one string into another i.e. the number of letters added, removed, or changed. Check [here](https://en.wikipedia.org/wiki/Levenshtein_distance) for a detailed explanation.

However, it must be noted that the Levenshtein calculations are very intensive. Thus, with a large folder or a large whitelist, the program will take considerably longer to complete

## Arguments and Options

  - `whitelist` is a text file of filenames to compare against
  - `directory` is the directory of files to search
  - `-l, --levenshtein` is an integer for the Levenshtein distance; if the option without an integer is provided, the default is 1
  - `-v,--verbose` will increase the level of logging output

The following options are mutually exclusive and concern the output:

  - `-s, --stdout` will turn off all logging output and output the filenames to stdout; useful for piping
  - `-o,--output` is a file to log the filenames to; default is `result.txt` in the current directory