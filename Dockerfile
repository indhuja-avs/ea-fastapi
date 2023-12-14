FROM osgeo/gdal:ubuntu-small-latest
RUN apt-get update && apt-get -y install python3-pip --fix-missing
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]