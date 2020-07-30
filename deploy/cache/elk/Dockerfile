FROM redis

COPY ./conf/redis.conf /usr/local/etc/redis/redis.conf

RUN chmod -R 777 /var/lib \
        && chmod 777 /usr/local/etc/redis/redis.conf

CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
