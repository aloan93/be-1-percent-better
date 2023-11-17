FROM python:3.10-slim

RUN adduser --uid 1000 --gecos '' --gid 0 --disabled-password onepercent && \
    mkdir -m 775 /opt/onepercent && \
    apt update && apt install -y default-libmysqlclient-dev pkg-config build-essential netcat-openbsd

COPY --chown=1000:0 requirements.txt /opt/onepercent/
RUN pip3 install -r /opt/onepercent/requirements.txt && \
    apt remove -y build-essential && \
    apt autoremove -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/onepercent

COPY --chown=1000:0 . ./
RUN chmod 774 /opt/onepercent/start.sh

USER 1000

CMD ["./start.sh"]
