#!/bin/bash
cd /home/252452.cloudwaysapps.com/bhdwepebka/public_html/caplinked_youtube_automation
python3 content_pipeline.py
python3 runway_generator.py
python3 youtube_uploader.py
