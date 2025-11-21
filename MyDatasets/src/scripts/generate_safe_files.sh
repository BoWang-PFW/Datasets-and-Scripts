#!/bin/sh
set -u

COUNT=${1:-30}

i=1
while [ "$i" -le "$COUNT" ]; do
  name=$(printf "safe_%02d.c" "$i")
  : > "$name"
  i=$((i + 1))
done
