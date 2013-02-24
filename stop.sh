#!/bin/bash
ps a | grep "python Zbap.py" | cut -d" " -f 2 | xargs kill -9
