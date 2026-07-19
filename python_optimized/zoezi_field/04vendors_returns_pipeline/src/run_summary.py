def output_metadata(
    metadata,
    extracted_record_count,
    valids_record_count,
    invalids_record_count,
    transformed_record_count,
    vendors_record_count,
    reasons_record_count,
):

    return [
        {
            "source": metadata.get("source"),
            "status": metadata.get("status"),
            "generated_at": metadata.get("generated_at"),
            "record_count": metadata.get("record_count"),
            "batch_id": metadata.get("batch_id"),
            "extracted_record_count": extracted_record_count,
            "valids_record_count": valids_record_count,
            "invalids_record_count": invalids_record_count,
            "transformed_record_count": transformed_record_count,
            "vendors_record_count": vendors_record_count,
            "reasons_record_count": reasons_record_count,
        }
    ]
