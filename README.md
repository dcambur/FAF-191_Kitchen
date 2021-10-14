# FAF-191_Kitchen

## Build

```bash
docker image build -t kitchen .
```

## Run

```bash
docker run -p 81:5000 --name kitchen -d kitchen
```

## Logs

```bash
docker logs -f kitchen
```
