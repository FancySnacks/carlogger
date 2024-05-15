#!/bin/bash

echo "carlogger: Running EXPORT test sequence"

parent_dir=$(pwd)
relative_dir="/tests/export_arg_test"

exec_dir="${parent_dir}${relative_dir}"

source "$exec_dir"