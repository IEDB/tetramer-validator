FROM python:3-slim

# We copy just the requirements.txt first to leverage Docker cache

COPY . /tetramer-validator

WORKDIR /tetramer-validator

RUN 	pip install -r requirements.txt
RUN	pip install -e .

WORKDIR tetramer_validator

ENTRYPOINT [ "tv" ]

CMD [ "webserver", "--host", "0.0.0.0" ]
