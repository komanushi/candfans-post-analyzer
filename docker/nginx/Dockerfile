FROM nginx:1.24-alpine

COPY ./docker/nginx/prod.conf.template /etc/nginx/nginx.conf.template
COPY ./application/staticfiles /usr/share/nginx/html/static

COPY ./docker/nginx/entrypoint.sh /root/nginx.sh

ENTRYPOINT ["/root/nginx.sh"]

CMD ["nginx", "-g", "daemon off;"]
