FROM python:3.5-onbuild

RUN mkdir -p /var/log/app/ \
	&& chmod -R 777 /var/log/app

COPY gunicorn.conf /usr/src/app/
# CMD [ "/usr/local/bin/gunicorn", "wsgi:application", "-c", "/usr/src/app/gunicorn.conf" ]
