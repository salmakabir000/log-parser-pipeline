def main_pipeline():
    from ingest import load_json
    from transform import extract_top_level, combine_data
    from clean import clean_types, deduplicate_by_ref
    import pandas as pd
    import os
    from load import load_to_bigquery


    # Authentication
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\UserL42\\Desktop\\log_parser_project\\service-account-key.json"

    # File path
    file_path = "C:\\Users\\UserL42\\Desktop\\log_parser_project\\crown_interactive_january_logs.json"

    # BigQuery destination
    table_id = "project-8605d464-749e-4e80-a2e.log_parser_pipeline.clean_logs"

    # Load JSON data
    raw_data = load_json(file_path)
    print("Total records loaded:", len(raw_data))


    # Extract top-level fields
    extracted_data = extract_top_level(raw_data)
    print("Records after extraction:", len(extracted_data))
    # print("Sample extracted record:", extracted_data[2])


    # XML parsing and combining with top-level data
    final_data = combine_data(extracted_data)
    print("Records after parsing:", len(final_data))


    # Claning data types
    clean_final_data = [clean_types(record) for record in final_data]
    # print("clean_final_data")
    # print(clean_final_data[2])


    # Remove duplicates
    deduplicated_data = deduplicate_by_ref(clean_final_data)
    print("Records after removing duplicates", len(deduplicated_data))


    # convert data to DataFrame
    df = pd.DataFrame(deduplicated_data)
    # print(df.head())
    print("done converting to DataFrame")

    # Load DataFrame to BigQuery
    load_to_bigquery(df, table_id)
    print("Data loaded to BigQuery successfully")
    
if __name__ == "__main__":
    main_pipeline()