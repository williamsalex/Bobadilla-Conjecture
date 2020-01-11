#!/bin/bash
parallel --timeout 5 -j 7 -N0 ../sage ./loader.sage.py ::: {1..4000} 2>/dev/null