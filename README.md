# Como rodar

```bash
docker-compose up
```

# Fazendo requisições na API

```bash
docker-compose rm --stop --force wrk
docker-compose up -d wrk
```

# Acessando as páginas

- app: http://localhost:5000
- métricas da app: http://localhost:5000/metrics
- prometheus: http://localhost:9090/
- grafana:  http://localhost:3000/
- email: http://localhost:8025/
