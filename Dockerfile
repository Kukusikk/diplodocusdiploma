FROM python:3.7-slim

COPY . /home

RUN chmod +x /home/myscript && \
    apt update && \ 
    apt upgrade -y && \ 
    apt install build-essential gcc g++ libc-dev subversion libpq-dev -y && \
    pip3 install Cython && \
    pip3 install -r /home/requirements.txt && \
    rm -rf /var/lib/apt/lists/*

CMD ["/home/myscript"]

