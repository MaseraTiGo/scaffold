FROM java:8-jre
MAINTAINER Roy

LABEL Description="使用mycat做mysql数据库的读写分离"
ENV mycat-version Mycat1.6.5
USER root

COPY ./Mycat-server-1.6.5-release-20180122220033-linux.tar.gz /
RUN tar -zxf ./Mycat-server-1.6.5-release-20180122220033-linux.tar.gz
COPY ./conf /mycat/conf
COPY ./sources.list /etc/apt/

ENV MYCAT_HOME=/mycat
ENV PATH=$PATH:$MYCAT_HOME/bin

WORKDIR $MYCAT_HOME/bin

RUN chmod u+x $MYCAT_HOME/conf
EXPOSE 8066 9066
CMD ["./mycat","console"]
