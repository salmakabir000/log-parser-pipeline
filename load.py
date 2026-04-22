from google.cloud import bigquery
import logging
import time

logging.basicConfig(level=logging.INFO)

def load_to_bigquery(df, table_id):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            client = bigquery.Client()
            job_config = bigquery.LoadJobConfig(
                write_disposition="WRITE_TRUNCATE",
                autodetect=True
            )

            logging.info(
                f"Upload attempt {attempt+1}"
            )

            job = client.load_table_from_dataframe(
                df,
                table_id,
                job_config=job_config
            )

            job.result()
            logging.info("Upload successful.")
            return True
        
        except Exception as e:
            logging.error(f"Attempt failed: {e}")
            if attempt < max_retries - 1:
                logging.info("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                logging.error("All retries failed.")
                return False