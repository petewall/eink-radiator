#!/bin/bash

DEPLOYMENT_DIR=/opt/eink-radiator

if ! command -v vendir > /dev/null 2>&1; then
    echo Error: vendir not installed >&2
    echo To install, see directions here: https://carvel.dev/vendir/docs/latest/install
    exit 1
fi

if ! command -v ytt > /dev/null 2>&1; then
    echo Error: ytt not installed >&2
    echo To install, see directions here: https://carvel.dev/ytt/docs/latest/install
    exit 1
fi

mkdir -p "${DEPLOYMENT_DIR}"
cd "${DEPLOYMENT_DIR}"

PLATFORM="darwin-amd64"
set -e

echo "Generating bill of materials via vendir..."
ytt \
    --file tools.yaml \
    --data-value platform="${PLATFORM}" \
    --file vendir.template.yml > vendir.yml

echo "Downloading components..."
vendir sync

echo "Generating config.yaml..."
ytt \
    --file tools.yaml \
    --data-value dir="${DEPLOYMENT_DIR}" \
    --file config.template.yaml > config.yaml

if [ ! -f slides.yaml ]; then
    echo "Generating stubbed slides.yaml..."
    echo "apiVersion: v1.eink-radiator.petewall.net" > slides.yaml
    echo "kind: Slides" >> slides.yaml
    echo "slides: []" >> slides.yaml
fi

echo "Deployment complete!"
echo "To start, run:"
echo "${DEPLOYMENT_DIR}/components/main/eink-radiator-${PLATFORM}" --config "${DEPLOYMENT_DIR}/config.yaml"
