# FAF-191_Kitchen

## Build:

```bash
docker image build -t docker-kitchen .
```

## Run:

```bash
docker run -p 5000:5000 --name kitchen -d docker-kitchen
```
