## Tranform module

When calculating `budget_variance`, the pipeline uses `planned_cost - actual_cost`. This method is prefered so that positive values may reflect postive budget variance and vice verser.

When calculating the `delivery_delay`, the module uses `actual_delivery_date - expected_delivery_date`; all the negative values(early deliveries) will be returned as 0 to avoid negative values in cases where the delivery was made early.

When calculating the `fulfillment_rate`, the  module uses `(received_qty / ordered_qty) * 100`.

When calculating `risk score`, the module considered cases where the `fulfillment_rate` is above 100%(over_shipment), this is accounted for because it is concidered a slight risk where the quantity received is more than quantity ordered.
