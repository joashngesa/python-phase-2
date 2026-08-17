# Challenges & Learnings During Designing

## 8-14-2026

1. When designing the extract module, always check the design of the json files imported, some have metadata dictionaries that contain batch_id, depot etc and some do not. Before designing extract, inspect the json files imported to determine the design of the module.
2. When designing the pipeline, to avoid duplicates logs,  the pipeline focusses on creating the modules without coding the loggings, test the result in the test.py during the designing phase. After completion of all the tables, loggings will be added when creating the orchestration modules such as process.py.
