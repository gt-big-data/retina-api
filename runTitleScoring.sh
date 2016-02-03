#!/bin/bash

cd /home/bdc/retina-api/
echo $(date) >> titleScoringRuns.log
python titleScoring.py
