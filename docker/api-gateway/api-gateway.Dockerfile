FROM nginx:latest

RUN apt-get update \
    && apt-get install -y nginx-module-njs

COPY ./nginx/oauth2.js ./etc/nginx/conf.d/oauth2.js
