# Challenges experienced in development

## Convert module challenge

in the convert.py module,  the error_reasons column, i am unable to load the first error causing the error in data conversion, egs when a value is empty, instead of recording the value is empty it records that the conversion failed, it is still true but it does nopt reveal the root cause of the problem

## All_files_summary

the all_files_summary file has an error, debugging needed.

## Duration variable

*TypeError: unsupported operand type for -: 'builtin_function_or_method' and 'float'*   error in the log file.

## Run summary file

THe file was not written in the selected output. The pipeline metrics did not work as expected.

## Solution

When using the perf_counter method, i excluded (), the correction is to include it.

Make sire that the module order of table returns are used the same way they are used in the process module.
