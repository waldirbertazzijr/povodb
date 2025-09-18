FROM postgres:15-alpine

# Copy initialization scripts
COPY ./init /docker-entrypoint-initdb.d/

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=povodb

# Expose port
EXPOSE 5432

# Volume for persistent data
VOLUME /var/lib/postgresql/data
