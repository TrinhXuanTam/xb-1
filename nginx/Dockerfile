FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY $NGINX_CONF_FILE /etc/nginx/conf.d/nginx.conf
