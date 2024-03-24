#!/bin/bash

echo "carlogger: Running ADD test sequence"

parent_dir=$(pwd)
relative_dir="/tests/add_arg_test"

exec_dir="${parent_dir}${relative_dir}"

source "$exec_dir"