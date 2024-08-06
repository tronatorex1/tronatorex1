# This dockerfile calls the python and a data-input file (locally) using the ADD commands
FROM python:3.11.4-slim-bookworm
ADD main1.py .
ADD inputfile.txt .
CMD [ "python", "./main1.py" ]