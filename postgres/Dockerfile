# Use the official PostgreSQL base image from Docker Hub
FROM postgres:latest

# Environment variables for PostgreSQL
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword

# Expose the default PostgreSQL port
EXPOSE 5432

# Custom initialization script (optional)
COPY init.sql /docker-entrypoint-initdb.d/

# You can add additional setup or configuration here

# Start PostgreSQL when the container runs
CMD ["postgres"]
