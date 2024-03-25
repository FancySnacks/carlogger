#!/bin/bash

echo "carlogger: Running READ test sequence"

parent_dir=$(pwd)
relative_dir="/tests/read_arg_test"

exec_dir="${parent_dir}${relative_dir}"

source "$exec_dir"