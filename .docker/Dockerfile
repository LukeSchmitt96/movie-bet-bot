FROM python:3.10

LABEL maintainer Luke Schmitt luke@lukeschmitt.me

WORKDIR /root/docker_ws

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH "/root/.local/bin:$PATH"

COPY . .

RUN poetry install --with test,dev

CMD ["poetry", "run", "task", "start"]
