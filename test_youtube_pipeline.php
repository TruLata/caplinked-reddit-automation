<?php
// Test script for the full YouTube automation pipeline

echo "<h1>YouTube Automation Pipeline Test</h1>";

$youtube_dir = '/home/252452.cloudwaysapps.com/bhdwepebka/public_html/caplinked_youtube_automation';

// Step 1: Run Content Pipeline
echo "<h2>Step 1: Running Content Pipeline...</h2>";
$output1 = shell_exec("cd $youtube_dir && python3 content_pipeline.py 2>&1");
echo "<pre>" . htmlspecialchars($output1) . "</pre>";

// Step 2: Run Runway Video Generator
echo "<h2>Step 2: Running Runway Video Generator...</h2>";
$output2 = shell_exec("cd $youtube_dir && python3 runway_generator.py 2>&1");
echo "<pre>" . htmlspecialchars($output2) . "</pre>";

echo "<h2>Test Complete</h2>";

?>
