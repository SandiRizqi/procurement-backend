#!/bin/sh
# start backend
cd /app/backend
gunicorn config.wsgi:application --bind 0.0.0.0:8000 &

# start frontend
cd /app/frontend
npm run start &

# start nginx
nginx -g 'daemon off;'
