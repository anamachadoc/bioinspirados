#!/bin/bash
CONFIG_FILE="config.yaml"
for n_bits in {6..20}
do
  echo "Executando com n_bits = $n_bits"
  sed -i "s/n_bits: [0-9]\+/n_bits: $n_bits/" $CONFIG_FILE
  python3 main.py
done
