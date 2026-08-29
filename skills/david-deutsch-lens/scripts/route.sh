#!/bin/sh
set -eu

case "$0" in
  /*) lens_route_entry=$0 ;;
  *) lens_route_entry=$PWD/$0 ;;
esac
lens_route_script=${lens_route_entry%/*}/route.py

exec python3 "$lens_route_script" "$@"
