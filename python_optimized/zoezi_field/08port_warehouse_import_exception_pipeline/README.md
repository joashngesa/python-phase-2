# Pipeline: Port-to-warehouse import exception pipeline.

## Project overview

Entails a supply chain company that imports goods through ports, clears customs, then moves containers to inland warehouses.

Each port sends JSON files with import container events. Some files are clean, some are broken, some have nested records, some have bad dates, some have invalid business values, and some contain duplicate container events.

Your pipeline must scan a folder, extract records from multiple JSON structures, validate and convert fields, handle controlled file failure, separate valid/invalid/duplicate records, transform valid records, summarize business results, and produce a final run summary.

## Pipeline Visual Data Flow

INPUT_DIR + FILE_PATTERN
          │
          ▼
    scan_folder()
          │
          │ returns list[Path]
          ▼
   process_all_files()
          │
          ├──────── file_path 1 ────────┐
          │                             ▼
          │                    process_one_file()
          │                             │
          │                             ▼
          │                        read_file()
          │                             │ raw
          │                             ▼
          │                     extraction modules
          │                             │ extracted rows
          │                             ▼
          │                       convert_data()
          │                             │ converted rows
          │                             ▼
          │                    get_invalid_tbl()
          │                       │          │
          │                    invalid    valid_raw
          │                                  │
          │                                  ▼
          │                       get_duplicates_valid()
          │                          │             │
          │                     duplicates       valid
          │                                        │
          │                                        ▼
          │                                transform_data()
          │                                        │
          │                                        ▼
          │                               summarize_table()
          │                                        │
          │                                        ▼
          │                                  write outputs
          │                                        │
          │                                        ▼
          │                              build_success_score()
          │                                        │
          │                              returns one file result
          │                                        │
          ├──────── file_path 2 ────────────────────┤
          ├──────── file_path 3 ────────────────────┤
          │                                        │
          ▼                                        ▼
            collect all file-result dictionaries
                              │
                              ▼
                     build_run_summary()
                              │
                              ▼
                         execute.py
                              │
                 print and write final report



## Orchestration Levels

The pipeline has three levels of control:

### Level one: `execute.py`

This is the pipleine entry point. It's responsibility is to:

* start the pipeline
* call `process_all_files()`
* receive the final run results
* print the overall execution report

### Level 2:  `process_all_files()`

This controls the entire batch. Its's responsibility is to:

* scan the input folder
* receive the discovered file_paths
* process each file
* collect each file result
* create run levels totals
* handle folder level failures

This function orchestrates the batch

the expectes output of `process_all_files` is **file_results**

### Level 3:  `process_one_file()`

This controls one file. Its's responsibility is to:

* read one file
* extract records and metadata
* convert values
* validate rows
* create function that is used to get invalid & valid rows
* separate duplicates & valid rows
* transform valid rows
* summarize transformed rows
* write file level outputs

This function orchestrates file level work flow

The expected output from `process_one_file` is **file_result**
