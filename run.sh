#!/bin/bash


python "manage.py" runserver &

sleep 6

xdg-open "http://127.0.0.1:8000/index"
