import time
import logging
import schedule
from main import main_pipeline

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def job():
    logging.info("Pipeline started")
    try:
        main_pipeline()
        logging.info("Pipeline completed successfully")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")

# schedule it
schedule.every(5).minutes.do(job)

# run once immediately
job()

# scheduler loop
while True:
    schedule.run_pending()
    time.sleep(1)