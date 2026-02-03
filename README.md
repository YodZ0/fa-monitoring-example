# FastAPI monitoring: Grafana + Prometheus + Loki

## Installation

Clone repository:

```commandline
git clone https://github.com/YodZ0/fa-monitoring-example.git
```

Install dependencies:

```commandline
poetry install
```

## Run / Stop

### Makefile:

#### Run

Run docker compose build:

```commandline
make run-build
```

#### Shutdown

Stop and remove docker containers:

```commandline
make shutdown
```

Stop and remove docker containers with volumes:

```commandline
make demolish
```

### Manual:

#### Run

Run docker compose build:

```commandline
docker compose up --build -d
```

#### Shutdown

Stop and remove docker containers:

```commandline
docker compose down
```

Stop and remove docker containers with volumes:

```commandline
docker compose down -v
```

## FastAPI configuration

This example project use two ways to collect metrics:

1. `prometheus-client` - official Prometheus library that you can use for manual metrics configuration;
2. `prometheus-fastapi-instrumentator` - de-facto industry standard, third-party library for FastAPI+Prometheus
   integration.

So, in this project you can see how to use both of them.

All you need to do is set "use_instrumentator" in `src/main.py`:

```python
from bootstrap import create_app

app = create_app(use_instrumentator=True)  # run app with prometheus-fastapi-instrumentator
```

## Load producer

### Usage

Run synthetic load producer with Makefile:

```commandline
make load
```

or manually:

```commandline
python ./load_producer/loader.py
```

### Configuration

Producer has two load patterns: `Constant` and `Random`:

- `Constant` generate requests with constant delay based on `base_rps` value;
- `Random` generate requests with random (min, max) delay seconds.

Set config params in `load_producer/loader.py`

```python
config = LoadConfig(
    duration_seconds=0.0,           # load duration in seconds, 0.0 = infinity
    pattern=LoadPattern.CONSTANT,   # or LoadPattern.RANDOM
    base_rps=10.0,                  # constant delay 1.0 / 10 = 100ms
    random_min_delay_seconds=0.01,  # min delay 10ms
    random_max_delay_seconds=2.0,   # max delay 2000ms
)
```
