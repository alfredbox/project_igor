sftp pi@192.168.1.180:project_igor/logs/* logs
python3 -m tools.process_log -d logs
