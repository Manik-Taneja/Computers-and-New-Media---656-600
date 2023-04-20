ls output_* | sort -n -t _ -k 2
for f in *.mp4; do echo "file '$f'" >> videos.txt; done
ffmpeg -f concat -safe 0 -i videos.txt -c copy FINALOUTPUT.mp4

