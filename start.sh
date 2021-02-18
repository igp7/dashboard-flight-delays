#!/bin/sh

gunicorn --bind "$HOST":"$PORT" "$ENTRYPOINT";
