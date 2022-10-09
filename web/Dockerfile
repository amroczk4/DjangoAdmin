FROM nginx:1.18
RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY static/ /usr/share/nginx/html/static/
COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/conf.d/ /etc/nginx/conf.d/
EXPOSE 80