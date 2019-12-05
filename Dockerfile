FROM researchdeezer/spleeter:3.7

EXPOSE 7000

RUN mkdir -p /app
WORKDIR /app

# paths
ENV SPLEETER_IN='/spleeter/in/'
ENV SPLEETER_OUT='/spleeter/out/'
ENV SPLEETER_MODELS='/spleeter/models/'
ENV KV_STORE='/data/'

RUN mkdir -p '${SPLEETER_IN}'
RUN mkdir -p '${SPLEETER_OUT}'
RUN mkdir -p '${SPLEETER_MODELS}'
RUN mkdir -p '${KV_STORE}'


VOLUME /app
VOLUME /spleeter

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade pip -r /app/requirements.txt

COPY ./src app

COPY ./entry.sh /
RUN chmod +x /entry.sh
ENTRYPOINT ["/entry.sh"]
