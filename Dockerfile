FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" \
    apt-get install -y \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists

RUN pip3 install pandas scipy pulp ortools

COPY /python /crosssums
ENV PYTHONPATH=/

ENTRYPOINT ["python3","-m", "crosssums"]
