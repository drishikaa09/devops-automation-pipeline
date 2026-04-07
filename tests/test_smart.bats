#!/usr/bin/env bats

@test "smart.sh creates project directory" {
  run bash smart.sh test_project 2

  [ -d "test_project" ]
}

@test "smart.sh creates correct number of files" {
  run bash smart.sh test_project2 3

  [ -f "test_project2/file1.txt" ]
  [ -f "test_project2/file2.txt" ]
  [ -f "test_project2/file3.txt" ]
}
