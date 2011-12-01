#! /bin/bash

D=`pwd`
cd /home/jbrandt/joelbrandt.org/howsiandoing/

LOG="/home/jbrandt/joelbrandt.org/howsiandoing/log.txt"
TWEETLOG="/home/jbrandt/joelbrandt.org/howsiandoing/tweetlog.txt"
IMAGE_DIR="/home/jbrandt/joelbrandt.org/howsiandoing/i"
DISS="http://www.cs.utexas.edu/~iwehrman/dissertation/dissertation.pdf"
PDF=`mktemp`
curl -s -o $PDF $DISS
WORDS=`pdftotext $PDF - | wc -w`
DATE=`date +%s`
echo "$DATE $WORDS" >> $LOG
rm $PDF

curl -s -o "$IMAGE_DIR/$DATE.png" --data "`python draw_chart.py`" "http://chart.googleapis.com/chart?"
ln -sf "$IMAGE_DIR/$DATE.png" "$IMAGE_DIR/current.png"

sleep 10

echo "-- Checking tweet at $DATE right now by executing python tweet_if_necessary.py $DATE --" >> $TWEETLOG
echo "-- The current time is `date` --" >> $TWEETLOG
python tweet_if_necessary.py $DATE >> $TWEETLOG 2>&1

cd $D
