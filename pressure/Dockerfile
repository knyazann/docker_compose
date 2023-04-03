FROM python
COPY . ./app
WORKDIR /app
RUN pip install -r requipments.txt
EXPOSE 80
CMD ["python","pressure.py"]
