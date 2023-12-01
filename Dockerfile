FROM python:alpine3.18

ENV VAULT_ADDR=
ENV VAULT_TOKEN=
ENV VAULT_NAMESPACE=

ENV RUNNING_IN_DOCKER=1

ARG USER=veamm

RUN adduser -D $USER
USER $USER
WORKDIR /home/$USER

COPY --chown=$USER:$USER requirements.txt requirements.txt
COPY --chown=$USER:$USER EnvDefault.py EnvDefault.py
COPY --chown=$USER:$USER vault_entity_alias_mount_mapping.py vault_entity_alias_mount_mapping.py

ENV PATH="/home/$USER/.local/bin:${PATH}"

RUN pip3 install --user -r requirements.txt

CMD ["python3", "vault_entity_alias_mount_mapping.py"]
