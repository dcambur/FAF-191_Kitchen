# FAF-191_Kitchen

## Build kitchen container

```bash
docker image build -t kitchen .
```

## Run

### Create Docker network for projects

```bash
docker network create restaurant
```

### Start kitchen container
```bash
docker run -p 81:5000 --name kitchen --rm --net restaurant -d kitchen
```

## Logs

```bash
docker logs -f kitchen
```
