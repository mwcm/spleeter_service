# thanks to https://medium.com/@gabimelo/developing-a-flask-api-in-a-docker-container-with-uwsgi-and-nginx-e089e43ed90e
FROM researchdeezer/spleeter:3.7

RUN mkdir -p /service
RUN mkdir -p /model

RUN useradd --no-create-home nginx

RUN apt-get update
RUN apt-get install -y --no-install-recommends supervisor nginx python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

RUN  mkdir -p /etc/uwsgi/
COPY ./requirements.txt /service/requirements.txt
COPY ./nginx.conf /etc/nginx/
COPY ./flask-site-nginx.conf /etc/nginx/conf.d/
COPY ./uwsgi.ini /etc/uwsgi/
COPY ./supervisord.conf /etc/

RUN pip3 install --no-cache-dir --upgrade pip -r /service/requirements.txt

COPY ./src/ /service/

EXPOSE 6000

WORKDIR /service
ENV MODEL_PATH /model

#RUN rq worker spleeter_tasks -u 'redis://0.0.0.0'
RUN chown -R nginx "/service"
ENTRYPOINT ["/usr/bin/env"]
CMD ["/usr/bin/supervisord"]
