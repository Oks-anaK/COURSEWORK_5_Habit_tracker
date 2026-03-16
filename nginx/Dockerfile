FROM nginx:alpine

# Копирование конфигурации
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Создание папок для статики и медиа
RUN mkdir -p /var/www/static /var/www/media