FROM python:3.11.3-bullseye

COPY requirements.txt /app/requirements.txt
COPY utils/extra_requirements.txt /app/utils/extra_requirements.txt
COPY cave_api /app/cave_api
WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app
CMD ["utils/run_django_docker.sh"]
# CMD ["python", "manage.py", "runserver"]
# CMD ["tail", "-f", "/dev/null"]
