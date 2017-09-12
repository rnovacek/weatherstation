#!/bin/sh

exec multitail -s 2 -cT ANSI -l './server.py' -cT ANSI -l 'yarn start'
