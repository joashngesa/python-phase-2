## Tranform module

When calculating `budget_variance`, the pipeline uses `ordered_value - quantity_received`.  Positive `budget_variance` shows the orders that were unfulfilled, negative shows orders that were not fulfilled and 0 shows orders were all sent as requested.

When calculating the `delivery_delay`, the module uses `actual_delivery_date - expected_delivery_date`; all the negative values(early deliveries) will be returned as 0 to avoid negative values in cases where the delivery was made early.

When calculating the `fulfillment_rate`, the  module uses `(received_qty / ordered_qty) * 100`.

When calculating `risk score`, the module considered cases where the `fulfillment_rate` is above 100%(over_shipment), this is accounted for because it is concidered a  risk where the quantity received is more than quantity ordered.

## Summary module

The column `over_budget_order_count` was changed to `unfulfilled_order_count`, the name over budget count insinuates that the budget was more than needed whereas the value of the column shows the orders that were unfulfilled(positive budget variance)

## Output summary

`ERROR`:There is an error in the pipeline, all_files summary is not working as expected, a solution is needed. the file metrics also have wrong files count.

`CORRECTION`:in the valid module, the order of the return was valid, duplicates but in the process module, i previously changed the order when assigning the values valid, duplicates in the function. The order should be the same in the module and the process module.

`IMPROVEMENT OPPORTUNITIES` : The file metrics should include failed stage and duration seconds

## Pipeline structure correction

### Improvement in structure validation

Initially the pipeline was was merely obtaining iterable records, as opposed to using an explicit contract which includes:

1. batch_id
2. depot
3. generated_at
4. records(table that undergoes pipeline process)
