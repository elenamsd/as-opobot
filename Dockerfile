FROM mongo:latest

COPY data/init.js /docker-entrypoint-initdb.d/

EXPOSE 27017
