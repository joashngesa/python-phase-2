# INBOUND RECEIVING ASN COMPLIANCE PIPELINE

## Pipeline Task

```
discover inbound files
        ↓
read JSON
        ↓
validate file structure
        ↓
convert raw values
        ↓
validate records
        ↓
identify duplicates
        ↓
transform valid records
        ↓
calculate receiving/compliance metrics
        ↓
write outputs
        ↓
capture failures
        ↓
continue safely where appropriate
        ↓
produce run-level metadata
```

## File Contracts

```
TOP LEVEL
    list

EACH ITEM IN LIST
    dict / JSON object
```

## Pipeline Workflow

1. Scan `INPUT_DIR` to get the raw files.
2. Read Json files meeting the contract requirements & extract table.
3. Convert file from `read`
4. create helper function `validation.py` for validation
5. Get `invalid` & `valid`from `converted` module
6. Get `duplicates` from valid file
7. Get `transformed` table from valid
8. Get `supplier_summary` table from `transformed` file
9. Get `warehouse_digest` table from `transformed`
10. Code `write_output` file for the files output

## Supporting modules

1. `.env.config` module that holds paths & environment variables.
2. `config.py` module that holds the pipeline configurations.
3. `log_config.py` module that configures the logging in the pipeline.

## Pipeline metadata modules

1. `result.py` that collects metrics for each file in the pipeline
2. `metrics.py` collects collective metrics for all the files in the pipeline

## Orchestrating modules

1. `process.py`
2. `execute.py`

## Validation contract & business relationships

### optional fields

```
carrier
dock_door
notes
receipt_date
N/B: when receipt_status = "Received"; then receipt_date should have a date_value
```

### allowed receipt status

```
{
    "Received",
    "Partial",
    "Rejected",
}
```

### quantity validation

```
ordered_qty > 0

shipped_qty >= 0

received_qty >= 0

damaged_qty >= 0

damaged_qty <= received_qty

unit_cost > 0
```

## Date validation rules

```
order_date <= ship_date

ship_date <= receipt_date

order_date <= promised_delivery_date
```

## Duplicates contract

`receipt_id` is used to check for duplicates

## Transform module contract

### 1. ordered value

`ordered_qty × unit_cost`

### 2. received value

`received_qty × unit_cost`

### 3. quantity variance

`received_qty - ordered_qty`

interpretation:

* 0  -> exact receipt
* less than 0  -> shortage
* greater than 0 -> over-receipt

### 4. fill rate

```
fill_rate_pct =
received_qty / ordered_qty × 100
```

### 5. damage rate

```
damage_rate_pct =
damaged_qty / received_qty × 100
```

where the damage rate is 0; we will use the value `None` as the value 0 insinuates that their was no damages to recived goods even when the received quantity is 0. When the damaged goods is recorded as 0, then the damage rate pct should represent that their was 0%(no damaged goods) to the goods received.

### 6. delivery variance

```
delivery_variance_days =
receipt_date - promised_delivery_date
```

interpretation:

```
negative → early
0        → on time
positive → late
```

where no receipt exists: we will use the `None` value since 0 is better used to reflect `on time` deliveries.

### 7. Delivery performance

```
Early -> negative
On Time -> 0
Late -> postive
Not Received -> none
we will use the delivery variance to get the values above
```

### Received performance

```
Exact -> 0 quantity variance
Short -> negative quantity variance
Over -> positive quantity variance
Damaged -> positive damaged_qty
Short & Damaged -> (-ve qty_var & +ve dam_qty)
```

We will use `quantity_variance` to determine *exact*, *short*, *over*. Check the `damaged column` to assign *damaged*, combine `damaged column` & `quality_variance` to get *short & damaged*.

### Compliance status

outcomes:

```
Compliant
Quantity Issue
Damage Issue
Delivery Issue
Multiple Issues
```

**a. Compliant:** *On time* `delivery_performance`& *Exact* `Received_performance`.

**b. Quantity_issue:** *Short* & *Over* `Received_performance`.

**c. Damaged_issue:**  *Damaged* `Received_performance`.

**d. Delivery_issue:** *Early* & *Late* `Delivery_performance`.

**e.  Multiple_issues:** *Early* OR *Late* `Delivery_performance` AND *Short* OR *Over* OR *Damaged*  OR *Short & damaged*`Received_performance`.
