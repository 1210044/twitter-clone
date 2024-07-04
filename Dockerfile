FROM postgres:latest

ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_DB=twitter

COPY ./db/ /var/lib/postgresql/data/

RUN chown -R postgres:postgres /var/lib/postgresql/data/

EXPOSE 5432

# CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
CMD ["postgres"]
