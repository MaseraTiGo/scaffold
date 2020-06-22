FROM mysql:5.7
MAINTAINER Roy

ENV APT_HOME=/etc/apt
COPY ./sources.list $APT_HOME/

ADD ./conf/ /etc/mysql/

EXPOSE 3306
CMD ["mysqld"]
