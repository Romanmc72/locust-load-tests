#!/usr/bin/env bash

set -euo pipefail

main() {
    docker-compose up --scale worker=4 -d
    open http://localhost:8089
}

main
