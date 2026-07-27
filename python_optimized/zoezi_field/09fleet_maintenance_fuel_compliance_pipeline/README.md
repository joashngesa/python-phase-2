# FLEET MAINTENANCE  & FUEL COMPLIANCE PIPELINE

## Business scenario



A national distribution company operates delivery trucks from several transport depots.

Every depot submits a daily JSON batch containing:

* fuel purchases
* odometer readings
* maintenance inspections
* vehicle availability
* reported mechanical defects

The operations team needs the pipeline to identify:

* invalid operational records
* duplicate submissions
* suspicious fuel activity
* vehicles requiring urgent maintenance
* depot-level operating metrics
* files that could not be processed
