FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root_password
ENV MYSQL_DATABASE=oppositions
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=user

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306