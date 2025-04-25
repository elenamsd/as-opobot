FROM mongo:latest

ENV MONGO_INITDB_ROOT_USERNAME=root
ENV MONGO_INITDB_ROOT_PASSWORD=root_password
ENV MONGO_INITDB_DATABASE=opobot

COPY data/init.js /docker-entrypoint-initdb.d/

EXPOSE 27017
