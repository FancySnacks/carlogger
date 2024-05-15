#!/bin/bash

echo "carlogger: Running IMPORT test sequence"

parent_dir=$(pwd)
relative_dir="/tests/import_arg_test"

exec_dir="${parent_dir}${relative_dir}"

source "$exec_dir"