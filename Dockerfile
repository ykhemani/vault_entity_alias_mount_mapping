FROM python:alpine3.16

ENV VAULT_ADDR=
ENV VAULT_TOKEN=
ENV VAULT_NAMESPACE=

RUN mkdir /app
ADD vault_entity_alias_mount_mapping.py /app
ADD requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["python3", "vault_entity_alias_mount_mapping.py"]
