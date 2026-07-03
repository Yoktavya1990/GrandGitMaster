FROM python:3.12-alpine
WORKDIR /app
COPY grandgitmaster/ grandgitmaster/
COPY seeds/ seeds/
COPY ggm .
ENV GGM_DB=/data/ggm.db
VOLUME /data
EXPOSE 8477
CMD ["python", "-m", "grandgitmaster", "serve", "--port", "8477"]
