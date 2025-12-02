
FROM python:3.10


WORKDIR /qa_guru_advanced_course


RUN pip install poetry


# COPY ./requirements.txt /code/requirements.txt
COPY pyproject.toml poetry.lock* README.md /qa_guru_advanced_course/


# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN poetry config virtualenvs.create false


RUN poetry install


COPY ./app /qa_guru_advanced_course/app


CMD ["fastapi", "run", "app/main.py", "--port", "80"]