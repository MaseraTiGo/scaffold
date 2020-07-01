FROM python:3.5

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

COPY . /usr/src/app

RUN mkdir -p /var/log/app/ \
   && chmod -R 777 /var/log/app

COPY gunicorn.conf /usr/src/app/
# CMD [ "/usr/local/bin/gunicorn", "wsgi:application", "-c", "/usr/src/app/gunicorn.conf" ]
