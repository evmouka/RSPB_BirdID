# backend/Dockerfile #production
# FROM python:latest
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# EXPOSE 5000
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

# backend/Dockerfile (development setup)
FROM python:latest
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_ENV=development
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]