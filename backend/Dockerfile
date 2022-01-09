FROM python:3.7-slim-buster

ARG UID
ENV UID=${UID:-9999}
ARG GID
ENV GID=${GID:-9999}

# We might be running as a user which already exists in this image. In that situation
# Everything is OK and we should just continue on.
RUN groupadd -g $GID recipebook_docker_group || exit 0
RUN useradd --shell /bin/bash -u $UID -g $GID -o -c "" -m recipebook_docker_user || exit 0

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gnupg2 \
    libpq-dev \
    dos2unix \
    tini \
    postgresql-client \
    && apt-get autoclean \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

USER $UID:$GID

COPY --chown=$UID:$GID ./backend/requirements/base.txt /recipebook/requirements/
# Disable the path warn as we set the correct path in the entrypoint when it is easy
# to know the users $HOME/.local/bin location. Changing path in the docker image does
# not work as we do not know where $HOME when using an ENV command.
RUN pip3 install --no-warn-script-location -r /recipebook/requirements/base.txt

COPY --chown=$UID:$GID ./docs /recipebook/docs
COPY --chown=$UID:$GID ./backend /recipebook/backend

WORKDIR /recipebook/backend

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH $PYTHONPATH:/recipebook/backend/src
ENV DJANGO_SETTINGS_MODULE='recipebook.config.settings.base'

RUN dos2unix /recipebook/backend/docker/docker-entrypoint.sh && \
    chmod a+x /recipebook/backend/docker/docker-entrypoint.sh

ENTRYPOINT ["/usr/bin/tini", "--", "/bin/bash", "/recipebook/backend/docker/docker-entrypoint.sh"]
CMD ["local"]
