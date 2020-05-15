#!/bin/bash
declare -a urls=("https://qaqadesign.staples.com/services/printing/services/printing/"
    "https://qadesign.staples.com/services/printing/whats-new"
    "https://qadesign.staples.com/services/printing/photo-gifts/personalized-calendars"
    "https://qadesign.staples.com/services/printing/legacy/Themes?q=1Vs6CjtwxY_VteZzh2jc1dkRmT82QfiZ5yw3oRZWjYdH6cz_FTg4bjMz9,yB,qccP"
"https://qadesign.staples.com/services/printing/Cart")
for target in "${urls[@]}"
do
    curl -kv "$target"
done
curl https://qadesign.staples.com/services/printing/business-cards/ | grep -o '<a .*href=.*>' | sed -e 's/<a /\n<a /g' | sed -e 's/<a .*href=['"'"'"]//' -e 's/["'"'"'].*$//' -e '/^$/ d' | grep -o '^/.*'>urls.txt
input="./urls.txt"
while IFS= read -r line
do
    echo "https://qadesign.staples.com$line"
    curl -kv "https://qadesign.staples.com$line"
done < "$input"
