FROM python:3.8.20-alpine3.20

RUN apk fix &&  \
    apk --no-cache --update add git git-lfs gpg less openssh patch perl && \
    git lfs install && \
    pip install --no-cache-dir git+https://github.com/openedx/cc2olx@{{ CC2OLX_BRANCH }}#egg=cc2olx

ENTRYPOINT ["cc2olx"]
