# Support bot

This is a customer service bot which includes a user interface agent and agents with several tools.

## Overview

The support bot consists of 7 main agents:

1. **User Interface Agent**: Handles initial user interactions and directs them to the help center agent based on their needs.
2. **Help Center Agent**: Provides detailed help and support using various tools and integrated with a Qdrant VectorDB for documentation retrieval.
3. **Stripe Agent**: Provides detailed support on stripe: search user by email and cancel a subscription
4. **Grafana Agent**: Who gives me information of a Grafana user from an email
5. **Query agent**: Who knows how to prodiore and execute queries on my postgre. I described 2 tables: users and services
6. **Kubectl agent**: That knows how to run create and run kubectl commands on my cluster to retrieve logs from a container for example

## Setup

To start the support bot:

1. Ensure Docker is installed and running on your system.
2. Install the necessary additional libraries:

```shell
make install
```

3. Initialize docker

```shell
docker-compose up -d
```

4. Prepare the vector DB:

```shell
make prep
```

5. Run the main script:

```shell
make run
```

## Tests

1. Run the test script to confirm everything run as expected:

```shell
make test
```
