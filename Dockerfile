# Dockerfile for PTIT INT4418 Group 6 (Verifier-Guided Repair)
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/.elan/bin:${PATH}"

# 1. Install system utilities and Python
RUN apt-get update && apt-get install -y --no-install-recommends     curl     git     build-essential     python3     python3-pip     python3-venv     ca-certificates     && rm -rf /var/lib/apt/lists/*

# 2. Install Elan and Lean 4
RUN curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain leanprover/lean4:v4.8.0

# 3. Setup workspace
WORKDIR /workspace
COPY requirements.txt /workspace/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /workspace/

CMD ["python3", "-m", "src.baseline_repair"]
