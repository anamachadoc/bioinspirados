#!/bin/bash

alpha_values=(1 2.5 5)
beta_values=(1 2.5 5)
Q_values=(100 200 500)
refresh_rate_values=(0.001 0.1)
evaporation_rate_values=(0.005 0.5)

base_config="config_default.yaml"
temp_config="config_temp.yaml"
python_script="main.py"

gerar_config() {
    local alpha=$1
    local beta=$2
    local Q=$3
    local refresh_rate=$4
    local evaporation_rate=$5
    local execution=$6

    cp "$base_config" "$temp_config"

    # Substitui apenas os parâmetros que você quer variar
    sed -i "s/^alpha: .*/alpha: $alpha/" "$temp_config"
    sed -i "s/^beta: .*/beta: $beta/" "$temp_config"
    sed -i "s/^Q: .*/Q: $Q/" "$temp_config"
    sed -i "s/^refresh_rate: .*/refresh_rate: $refresh_rate/" "$temp_config"
    sed -i "s/^evaporation_rate: .*/evaporation_rate: $evaporation_rate/" "$temp_config"
    sed -i "s/^execution: .*/execution: $execution/" "$temp_config"

    output_dir="output/LAU15/a${alpha}_b${beta}_Q${Q}_r${refresh_rate}_e${evaporation_rate}"
    mkdir -p "$output_dir"
    execution_dir="${output_dir}/execution_${execution}"
    mkdir -p "$execution_dir"

    echo "Executando: alpha=$alpha, beta=$beta, Q=$Q, refresh_rate=$refresh_rate, evaporation_rate=$evaporation_rate, execution=$execution"
    python3 "$python_script" "$execution_dir"

    rm "$temp_config"
}

# Combinações
for alpha in "${alpha_values[@]}"; do
    for beta in "${beta_values[@]}"; do
        for Q in "${Q_values[@]}"; do
            for refresh_rate in "${refresh_rate_values[@]}"; do
                for evaporation_rate in "${evaporation_rate_values[@]}"; do
                    for execution_number in {0..9}; do
                        gerar_config "$alpha" "$beta" "$Q" "$refresh_rate" "$evaporation_rate" "$execution_number"
                    done
                done
            done
        done
    done
done
