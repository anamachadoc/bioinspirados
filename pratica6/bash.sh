#!/bin/bash

w_values=(1.0)
c1_values=(2.0)
c2_values=(0.5 1.0 2.0)
topology_values=("global" "ring" "focal")

base_config="config_default.yaml"
temp_config="config_temp.yaml"
python_script="main.py"

gerar_config() {
    local w=$1
    local c1=$2
    local c2=$3
    local topology=$4
    local execution=$5

    cp "$base_config" "$temp_config"

    sed -i "s/^w: .*/w: $w/" "$temp_config"
    sed -i "s/^c1: .*/c1: $c1/" "$temp_config"
    sed -i "s/^c2: .*/c2: $c2/" "$temp_config"
    sed -i "s/^topology: .*/topology: $topology/" "$temp_config"

    output_dir="output/${topology}_w${w}_c1${c1}_c2${c2}"
    mkdir -p "$output_dir"
    execution_dir="${output_dir}/execution_${execution}"
    mkdir -p "$execution_dir"

    echo "Executando: w=$w, c1=$c1, c2=$c2, topology=$topology, execution=$execution"
    python3 "$python_script" "$execution_dir"

    rm "$temp_config"
}

# Combinações
for w in "${w_values[@]}"; do
    for c1 in "${c1_values[@]}"; do
        for c2 in "${c2_values[@]}"; do
            for topology in "${topology_values[@]}"; do
                for execution_number in {0..9}; do
                    gerar_config "$w" "$c1" "$c2" "$topology" "$execution_number"
                done
            done
        done
    done
done
