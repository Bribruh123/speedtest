FROM python:3.11
# Or any preferred Python version.
ADD post_data_source.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "-u", "post_data_source.py"]

# Or enter the name of your unique directory and parameter set.