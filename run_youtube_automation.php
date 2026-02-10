<?php
// YouTube Automation Cron Job Wrapper
$youtube_dir = '/home/252452.cloudwaysapps.com/bhdwepebka/public_html/caplinked_youtube_automation';

echo "YouTube Automation started at " . date('Y-m-d H:i:s') . "\n";

// Run content pipeline
$output1 = shell_exec("cd $youtube_dir && python3 content_pipeline.py 2>&1");
echo "Content Pipeline: " . $output1 . "\n";

// Run Runway generator
$output2 = shell_exec("cd $youtube_dir && python3 runway_generator.py 2>&1");
echo "Runway Generator: " . $output2 . "\n";

// Run YouTube uploader
$output3 = shell_exec("cd $youtube_dir && python3 youtube_uploader.py 2>&1");
echo "YouTube Uploader: " . $output3 . "\n";

file_put_contents('/home/252452.cloudwaysapps.com/bhdwepebka/public_html/logs/youtube_automation.log', date('Y-m-d H:i:s') . " - Execution completed\n", FILE_APPEND);
?>
