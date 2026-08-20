for truthiness

# Challenges & Learnings During Designing

## 8-14-2026

1. When designing the extract module, always check the design of the json files imported, some have metadata dictionaries that contain batch_id, depot etc and some do not. Before designing extract, inspect the json files imported to determine the design of the module.
2. When designing the pipeline, to avoid duplicates logs,  the pipeline focusses on creating the modules without coding the loggings, test the result in the test.py during the designing phase. After completion of all the tables, loggings will be added when creating the orchestration modules such as process.py.

## 8-15-2026

When designing if statements together with elif statements; always remember python checks conditions from top to bottom

Establish and understand the difference between `value is not` and `value is none or value == "`, and the best scenarios to use one or the other. The main difference is that `if not value` checks for truthiness(evaluating whether a value is consiodered 'falsy' in python), whereas `if value is none or value == "` checks explicitly for missing or blank data types.

## 8-18-2026

The pipeline run but has some output summary issues

the main issues that caused this was not using ( ) after calling `perf_counter()`. This causing a compunding effect.

Using `logging` instead of `logger` when calling logs in modules\

8-19-2026

Rectified the errors in the output files.
