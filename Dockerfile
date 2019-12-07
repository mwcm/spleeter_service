# thanks to https://medium.com/@gabimelo/developing-a-flask-api-in-a-docker-container-with-uwsgi-and-nginx-e089e43ed90e
FROM researchdeezer/spleeter:3.7

RUN mkdir -p /app

RUN useradd --no-create-home nginx
VOLUME /spleeter/

RUN apt-get update
RUN apt-get install -y --no-install-recommends supervisor nginx python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

RUN  mkdir -p /etc/uwsgi/
COPY ./requirements.txt /app/requirements.txt
COPY ./nginx.conf /etc/nginx/
COPY ./flask-site-nginx.conf /etc/nginx/conf.d/
COPY ./uwsgi.ini /etc/uwsgi/
COPY ./supervisord.conf /etc/

RUN pip3 install --no-cache-dir --upgrade pip -r /app/requirements.txt

COPY ./src/ /service/


EXPOSE 6000

ENTRYPOINT ["/usr/bin/env"]

WORKDIR /service
RUN  chown -R nginx "/service"
CMD ["/usr/bin/supervisord"]
