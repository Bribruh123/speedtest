FROM python:3.11
# Or any preferred Python version.
ADD netgear_speeds.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "-u", "netgear_speeds.py"]

# Or enter the name of your unique directory and parameter set.