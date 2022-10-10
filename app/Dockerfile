FROM python:3.9.5
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . /code/
RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/sh", "-c", "scripts/entrypoint.sh"]
EXPOSE 8000