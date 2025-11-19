# Deployment Guide

## Local Development

### Prerequisites
- Python 3.9+
- PostgreSQL 15+
- Redis 7+

### Setup

1. Clone repository:
```bash
git clone https://github.com/yourusername/carbon-aware-checkout.git
cd carbon-aware-checkout
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
make install
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run tests:
```bash
make test
```

6. Start API:
```bash
make run
```

API will be available at `http://localhost:8000`

## Docker Deployment

### Build and run:
```bash
make docker-build
make docker-up
```

### Stop:
```bash
make docker-down
```

## Production Deployment

### AWS ECS/Fargate

1. Build and push image:
```bash
docker build -t cac:latest .
docker tag cac:latest your-registry/cac:latest
docker push your-registry/cac:latest
```

2. Create ECS task definition with environment variables
3. Deploy service with load balancer

### Kubernetes

See `k8s/` directory for manifests (TODO)

## Environment Variables

Required:
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- `DATABASE_URL`
- `REDIS_URL`

Optional:
- `LOG_LEVEL` (default: INFO)
- `API_HOST` (default: 0.0.0.0)
- `API_PORT` (default: 8000)

## Monitoring

- Health check: `GET /`
- Metrics: `GET /metrics`
- Logs: Check `logs/` directory

## Scaling

- Horizontal: Scale API containers
- Vertical: Increase container resources
- Database: Use read replicas for analytics
- Cache: Redis for frequent lookups
