## Tranform module

When calculating `budget_variance`, the pipeline uses `ordered_value - quantity_received`.  Positive `budget_variance` shows the orders that were unfulfilled, negative shows orders that were not fulfilled and 0 shows orders were all sent as requested.

When calculating the `delivery_delay`, the module uses `actual_delivery_date - expected_delivery_date`; all the negative values(early deliveries) will be returned as 0 to avoid negative values in cases where the delivery was made early.

When calculating the `fulfillment_rate`, the  module uses `(received_qty / ordered_qty) * 100`.

When calculating `risk score`, the module considered cases where the `fulfillment_rate` is above 100%(over_shipment), this is accounted for because it is concidered a  risk where the quantity received is more than quantity ordered.

## Summary module

The column `over_budget_order_count` was changed to `unfulfilled_order_count`, the name over budget count insinuates that the budget was more than needed whereas the value of the column shows the orders that were unfulfilled(positive budget variance)
