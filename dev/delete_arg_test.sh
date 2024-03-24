#!/bin/bash

echo "carlogger: Running DELETE test sequence"

parent_dir=$(pwd)
relative_dir="/tests/delete_arg_test"

exec_dir="${parent_dir}${relative_dir}"

source "$exec_dir"