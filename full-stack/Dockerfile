FROM python:3.11-alpine

# Install Node.js & Nginx
RUN apk add --no-cache nodejs npm nginx bash

WORKDIR /app

# Copy backend
COPY procurement-backend/ /app/backend
WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput

# Copy frontend
COPY template-management-project/ /app/frontend
WORKDIR /app/frontend
RUN npm install
RUN npm run build

COPY nginx.conf /etc/nginx/nginx.conf

# Copy run.sh
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 80 8080 8000

ENTRYPOINT ["/run.sh"]
