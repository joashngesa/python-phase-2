# Challenges & learning during designing

## convert.py module challenge

In cases where the values is blank or missing, instead of the error_reasons column reading that the value is missing or blank- despite coding this in the module,  ir records the second  the scond option coded, for example:


```python
ordered_qty = buy.get("ordered_qty")
        if ordered_qty is None or str(ordered_qty).strip() == "":
            buy["ordered_qty"] = None
            add_error(buy, "ordered_qty is missing or blank")
            conversion_error_count += 1

        else:
            try:
                buy["ordered_qty"] = int(ordered_qty)

            except (ValueError, TypeError):
                buy["ordered_qty"] = None
                add_error(buy, "ordered_qty should be integer")
                conversion_error_count += 1
```

## validate.py module challenge

Find out weather their is need to check for boolean values in integer value columns. For example i used:

```Python
elif not isinstance(received_qty, int):
```

instead of using:

```Python
elif not isinstance(ordered_qty, int) or isinstance(ordered_qty, bool):
```
