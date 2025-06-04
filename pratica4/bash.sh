#!/bin/bash

# (população * gerações)
total=10000

n_pop_values=(100 200 500)
prob_mutation_values=(0.01 0.05 0.1)
prob_crossing_values=(0.6 0.8 1)
select_values=('tournament' 'roulette')

base_config="config_default.yaml"
temp_config="config_temp.yaml"
python_script="main.py"  

gerar_config() {
    local prob_mutation=$1
    local prob_crossing=$2
    local n_pop=$3
    local n_gen=$4
    local execution=$5
    local select_by=$6

    cp "$base_config" "$temp_config"

    sed -i "s/prob_mutation: .*/prob_mutation: $prob_mutation/" "$temp_config"
    sed -i "s/prob_crossing: .*/prob_crossing: $prob_crossing/" "$temp_config"
    sed -i "s/n_pop: .*/n_pop: $n_pop/" "$temp_config"
    sed -i "s/n_gen: .*/n_gen: $n_gen/" "$temp_config"
    sed -i "s/execution: .*/execution: $execution/" "$temp_config"
    sed -i "s/select_by: .*/select_by: $select_by/" "$temp_config"
     
    output_dir="output/LAU15/${select_by}/${prob_mutation}_${prob_crossing}_${n_pop}_${n_gen}"
    mkdir -p "$output_dir"
    execution_dir="${output_dir}/execution_${execution}"
    mkdir -p "$execution_dir"

    echo "Run with config: mutation=$prob_mutation, crossing=$prob_crossing, pop=$n_pop, gen=$n_gen"
    python3 "$python_script" "$execution_dir"

    rm "$temp_config"
}

execution_counter=0

# Combinações
for select_mode in "${select_values[@]}"; do
    for prob_mutation in "${prob_mutation_values[@]}"; do
        for prob_crossing in "${prob_crossing_values[@]}"; do
            for n_pop in "${n_pop_values[@]}"; do
                n_gen=$((total / n_pop))
                for execution_number in {0..9}; do
                    gerar_config "$prob_mutation" "$prob_crossing" "$n_pop" "$n_gen" "$execution_number" "$select_mode"
                    execution_counter=$((execution_counter + 1))
                done
            done
        done
    done
done
