FROM centos:centos7


RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm

RUN yum update -y

RUN yum install -y \
    libcurl-devel \
    libffi-devel \
    python35u \
    python35u-pip \
    systemd-devel \
    --

RUN pip3.5 install tox==2.7.0 \
    virtualenv-tools \
    --

RUN mkdir -p \
    /var/cache/build-rpm \
    /var/cache/pip/download \
    /var/cache/pip/pkg

ENV \
    CACHE_DIR=/var/cache/build-rpm \
    PIP_CACHE_DIR=/var/cache/pip \
    PYCURL_SSL_LIBRARY=nss \
    TOX_WORK_DIR=/tmp
