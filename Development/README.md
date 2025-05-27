# Development Setup

This folder contains the scripts, data, and models used during development and training.

## Environment Setup

1. Copy the environment template.
    
    ```bash
    cp src/scraping/.env_template src/scraping/.env
    ```

2. Open the new `.env` file and fill in the required environment variables.

    ```
    GITHUB_TOKEN=
    ```

    Make sure not to commit your filled `.env` file to version control.

## Folder Overview

- `data/`: Contains CSV and JSON data used for model training.
- `models/`: Stores trained model files.
- `src/scraping/`: Scripts for scraping and data extraction.
- `src/training/`: Jupyter notebooks and training scripts.