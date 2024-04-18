#!/bin/bash

echo "carlogger: Running UPDATE test sequence"

parent_dir=$(pwd)
relative_dir="/tests/update_arg_test"

exec_dir="${parent_dir}${relative_dir}"

source "$exec_dir"