# Pipeline: Regional cold chain incident batch pipeline

## Project overview

 The theme of the project is cold chain supply chain monitoring.

The company moves temperature-sensitive products across warehouses: vaccines, fresh produce, frozen seafood, insulin, and specialty foods.

Each regional warehouse sends a daily JSON file containing shipment temperature incident reports.

Your job is to build a batch pipeline that scans a raw folder, processes multiple JSON files, survives broken files, validates records, transforms valid records, writes outputs, and creates a run summary.

## Business scenario

The pipeline receivfes json files in the folder. Each file contains shipment temperature events. Each valid record represents one shipment incident. The pipeline answers:

* which files are processed
* which files failed
* which shipments are valid
* which shipments are invalid
* which incidents are high risk
* which region/product category had the most temperature exposure

## Pipeline workflow

## Validation rules

A record is invalid if:

* Any required field is missing.
* Any required field is blank
* Any conversion error exists
* `Product category` is not allowed
* `Delivery_status` is not allowed
* `Carrier` is not allowed
* `required_temp_min_c` is greater than `required_temp_max_c`
* `exposure_minutes` is less than or equal to aero
* `incident_date` is not YYYY-MM-DD
* `incident_date` is after generated date
* if `actual_temp_c` is **within the required temperature range**, the record is valid
