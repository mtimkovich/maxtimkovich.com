#!/bin/bash

find src -name requirements.txt -exec cat {} \; | sort -f | uniq > requirements.txt
