#!/bin/bash
for file in static/Output/*.mp4;do 
	echo "$(basename "$file")"
done
