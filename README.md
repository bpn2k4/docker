# Docker

This repo contains:<br>
- [`docker`](./docker): Dockerfile template for some languages like: Nodejs, React Project, Go, Python,... <br>
- [`template`](./templates/): Docker compose file for some services like: mysql, postgresql, elasticsearch, kibana,... <br>
- [`examples`](./examples/): Some docker compose file for multi containers app, or ad-hoc app like: gitlab,... <br>

## 1. Dockerfile for some language
## 2. Docker compose template for some services
## 3. Some ad-hoc container app

For run a `postgresql` container:

```bash
cp /template/postgresql.yaml docker-compose.yaml
mkdir data
sudo chown 1001:1001 data
docker compose up -d
```