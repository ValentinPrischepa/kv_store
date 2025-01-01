# Persistent Key-Value Store

This repository contains a simple key-value store implemented in Python, designed for persistence using a log file and in-memory hash map. The store supports basic operations such as putting, getting, and deleting entries, and includes log file compaction to reclaim space.

## Features

- **Persistent Storage**: Utilizes a log file to ensure data persistence.
- **In-Memory Index**: Maintains an in-memory hash map for fast lookups.
- **Log File Compaction**: Periodically compacts the log file to remove obsolete entries.
- **RESTful API**: Provides a Flask-based web interface for interacting with the store.

## Benchmark
- Write Throughput: 18667.23634551022 operations/second
- Read Throughput: 85570.44871245598 operations/second

## Project Structure

- `app.py`: The main Flask application.
- `config.py`: Configuration file for paths and other settings.
- `kv_store/`
  - `__init__.py`: Initialization file for the key-value store package.
  - `log_file_manager.py`: Manages log file operations.
  - `hash_map_manager.py`: Manages in-memory hash map operations.
  - `service.py`: Provides high-level operations for the key-value store.
- `tests/`
  - `test_log_file_manager.py`: Unit tests for the log file manager.
  - `test_hash_map_manager.py`: Unit tests for the hash map manager.
  - `test_service.py`: Unit tests for the service layer.
- `.gitignore`: Git ignore file to exclude unnecessary files from version control.
- `requirements.txt`: List of dependencies.
- `utils.py`: Utility functions.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ValentinPrischepa/kv_store.git
    cd kv_store
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```bash
    python app.py
    ```

2. The API will be available at `http://127.0.0.1:5000`.

## Running Tests

To run the tests, use the following command:
```bash
python -m unittest discover -s tests
