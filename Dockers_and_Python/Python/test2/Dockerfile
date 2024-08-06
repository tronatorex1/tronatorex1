# This dockerfile calls the python and a Sqlite3 file with previously loaded data (test1.db)
FROM python:3.8-slim-bullseye
ADD main.py .
ADD test1.db . 
CMD ["python", "./main.py"]