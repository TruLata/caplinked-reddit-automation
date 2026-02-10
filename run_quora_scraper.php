<?php
// Quora Scraper Cron Job Wrapper
$output = shell_exec('cd /home/252452.cloudwaysapps.com/bhdwepebka/public_html/caplinked_quora_scraper && python3 quora_scraper.py 2>&1');
echo "Quora Scraper executed at " . date('Y-m-d H:i:s') . "\n";
echo $output;
file_put_contents('/home/252452.cloudwaysapps.com/bhdwepebka/public_html/logs/quora_scraper.log', date('Y-m-d H:i:s') . " - Execution completed\n", FILE_APPEND);
?>
