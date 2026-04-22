# Log Parser Pipeline (JSON → BigQuery)

## Overview

This project implements an end-to-end data engineering pipeline that processes raw JSON log data containing embedded SOAP XML responses, transforms it into a structured format, performs data cleaning and deduplication, and loads the final dataset into Google BigQuery for analytical use.

The pipeline is designed to be modular, re-runnable, and scalable, following standard data engineering separation of concerns: ingestion, transformation, cleaning, and loading.


## Architecture

The pipeline follows a multi-stage flow:
Raw JSON Logs
↓
Ingestion (load_json)
↓
Transformation (extract + XML parsing)
↓
Cleaning (type casting + deduplication)
↓
Structured Dataset (Pandas DataFrame)
↓
BigQuery Load
↓
Scheduled Execution (automation layer)


## Features
- Extracts structured fields from nested JSON logs
- Parses embedded SOAP XML responses using `ElementTree`- Handles missing and malformed data gracefully
- Performs type normalization (timestamps, floats, integers, booleans)
- Deduplicates records based on unique reference (`ref`)- Loads clean data into Google BigQuery
- Supports automated execution via scheduler (cron-like behavior)

## Tech Stack
- Python 3.10+
- Pandas
- Google BigQuery Python Client
- XML parsing (`xml.etree.ElementTree`)
- JSON processing
- Schedule (for automation)

## Project Structure
log-parser-pipeline/
│
├── ingest.py              # Loads raw JSON data
├── transform.py           # Extracts fields + parses XML
├── clean.py              # Data type cleaning + deduplication
├── main.py               # Pipeline orchestration
├── scheduler.py          # Automated execution (optional)
├── requirements.txt
└── README.md

## Data Transformation Details

### Top-Level Fields Extracted:
- id
- action
- success
- gateway
- ref
- service
- time
- created

  ### XML Fields Extracted:
  - amount
  - confirmationTime
  - customerAddress
  - customerMeterNumber
  - debtAmount
  - initiationTime
  - status
  - units
  - unitsType
  - value
  - vat

  ## Data Quality Handling
  - Missing values are preserved as `None` and handled downstream
  - Numeric fields are explicitly cast to float/int
  - Timestamp fields are normalized to ISO datetime format
  - Duplicate records are resolved using `ref`, keeping the latest `created` record

  ## BigQuery Loading Strategy
  - Uses `google-cloud-bigquery` Python client
  - Loads data from Pandas DataFrame
  - Uses `WRITE_TRUNCATE` mode for idempotent pipeline runs
  - Designed for re-runnability without data duplication

  ## Key Design Principles
  - **Modularity**: Each pipeline stage is isolated into separate modules
  - **Re-runnability**: Pipeline can be executed multiple times safely
  - **Observability**: Logging included for pipeline execution tracking
  - **Scalability**: Structured for future extension into Airflow / Cloud Scheduler

  ## Future Improvements
  - Replace scheduler with Apache Airflow or Cloud Composer
