#!/bin/bash

# for testing.
# python run.py --multirun task.num_observation=1,2,3,4,5,6,7,8,9,10 task.num_simulations=1000,10000,100000 compute_metrics=true hydra/launcher=joblib task=bernoulli_glm,bernoulli_glm_raw,gaussian_linear,gaussian_linear_uniform,gaussian_mixture,slcp,slcp_distractors,two_moons algorithm=npe
# python run.py --multirun task.num_observation=1 task.num_simulations=1000
# compute_metrics=false hydra/launcher=joblib task=bernoulli_glm algorithm=npe
# python run.py --multirun task.num_observation=1,2,3,4,5,6,7,8,9,10 task.num_simulations=1000,10000,100000 compute_metrics=true hydra/launcher=joblib task=two_moons algorithm=nre

# List of tasks
# tasks=("gaussian_linear" "gaussian_linear_uniform" "gaussian_mixture" "slcp"
# "slcp_distractors" "two_moons")
tasks=("bernoulli_glm" "bernoulli_glm_raw")

# List of algorithms
# algorithms=("nle" "nre")
algorithms=("snle" "snre")

# Common settings
num_observation="1,2,3,4,5,6,7,8,9,10"
num_simulations="1000,10000,100000"
compute_metrics="true"
launcher="joblib"

# File to log failures
failed_log="failed_tasks_algorithms.log"
> $failed_log  # Clear previous log

# Iterate over each algorithm and task and run the command
for algorithm in "${algorithms[@]}"; do
    for task in "${tasks[@]}"; do
        echo "Running algorithm: $algorithm, task: $task"
        python run.py --multirun \
            task.num_observation=$num_observation \
            task.num_simulations=$num_simulations \
            compute_metrics=$compute_metrics \
            hydra/launcher=$launcher \
            hydra.launcher.n_jobs=5 \
            task=$task \
            algorithm=$algorithm
        if [ $? -ne 0 ]; then
            echo "Failed: algorithm=$algorithm, task=$task" >> $failed_log
        fi
    done
done

echo "All tasks and algorithms completed."
echo "Check $failed_log for any failures."