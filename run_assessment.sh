#!/bin/bash

#./ssllabs-scan-v3 --hostfile url_list.txt --ignore-mismatch >url_scores.json || ssllabs-scan-v3 --hostfile url_list.txt --ignore-mismatch >url_scores.json

python get_scores.py './url_scores.json' > score_summary.txt
