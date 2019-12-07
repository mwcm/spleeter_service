FROM researchdeezer/spleeter:3.7

RUN mkdir -p /app

# paths
ENV SPLEETER_IN='/spleeter/in/'
ENV SPLEETER_OUT='/spleeter/out/'
ENV SPLEETER_MODELS='/spleeter/models/'
ENV KV_STORE='/data/'
ENV PORT=6000

RUN mkdir -p ${SPLEETER_IN}
RUN mkdir -p ${SPLEETER_OUT}
RUN mkdir -p ${SPLEETER_MODELS}
RUN mkdir -p ${KV_STORE}

RUN useradd --no-create-home nginx
VOLUME /spleeter/

RUN apt-get update
RUN apt-get install nginx python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools -y

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY ./requirements.txt /app/requirements.txt
COPY nginx.conf /etc/nginx/
COPY flask-site-nginx.conf /etc/nginx/conf.d/

RUN pip3 install --no-cache-dir --upgrade pip -r /app/requirements.txt

COPY ./src/ /service/

WORKDIR /service/

EXPOSE 6000

ENTRYPOINT ["/usr/bin/env"]

CMD [ "uwsgi", "--socket",      "0.0.0.0:6000", \
							 "--buffer-size", "32768", \
							 "--plugins",     "python3", \
							 "--protocol",    "uwsgi", \
							 "--gevent",      "100", \
							 "--processes",   "10", \
							 "--wsgi",        "run:app" ]
