# Regional Procurement Delivery Compliance Pipeline

## Case Scenario

You work for a Canadian industrial supply company operating procurement depots across Western Canada.

Every day, regional procurement systems export JSON files containing purchase-order delivery records.

The business wants a pipeline that determines:

* which records are usable,
* which records are invalid,
* whether duplicated transactions exist,
* whether suppliers are delivering late,
* whether purchase orders exceed their approved budgets,
* which suppliers represent operational risk,
* and whether  **the pipeline itself is operating reliably** .

## Pipeline Workflow

1. **Scan** the `INPUT_DIR` to retrieve the input files
2. **Read** the *json* files retrieved from scanned files.
3. **Extract** the *json files, batch_id, depot*
4. **Add**  *source_file, processed_at*  metadata to the extracted list of dictionaries(table).
5. **Convert** numerics & date columns from the **extracted** table.
6. Create **invalid** & **valid_raw** from the **converted** table.
7. Create **valid** & **duplicates** from **valid_raw** table.
8. Create **transformed** files from **valid table.**
9. Create the **summary** table from the **transformed** table.
10. Create **write_output** module for the pipeline files output.

## Supporting modules

1. `.env.config` file that holds the input & output paths.
2. `config.py` module that holds the environment & pipeline variables used to run the pipeline.
3. `log_config` module that configures the logging of the pipeline.
4. `utility.py` module that designs the `run_id`

## Summarizing modules

1. `result.py` module that summarizes the metrics of each file in the pipeline
2. `metrics.py` module that summarizes the metrics of all the files in the pipeline

## Orchestration modules

1. `process.py` modules that holds `process_one_file` function that processes one file at a time and the `process_all_files` function that processes all files from the scan module. It addresses all folder errors.
2. `execute.py` modules
