#!/bin/bash

parent_dir=$(pwd)
test_scripts=("/dev/add_arg_test.sh" "/dev/read_arg_test.sh" "/dev/delete_arg_test.sh")

exec_dir=""

for script in ${test_scripts[@]}
do
  exec_dir="${parent_dir}${script}"
  source "$exec_dir"
done