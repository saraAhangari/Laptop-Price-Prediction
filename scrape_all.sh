#!/bin/bash
set -euxo pipefail
cd ./scraper
python ./link_extractor/main.py --count 4000 -o ../datasets/links.txt
scrapy crawl laptops -a links_file=../datasets/links.txt
python ./jsonl_to_csv.py -i ./data.jsonl -o ../datasets/data.csv
mv ./data.jsonl ../datasets/data.jsonl
