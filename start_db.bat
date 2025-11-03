@echo off
duckdb -init "ATTACH 'nba_scraper.db' AS db (READ_ONLY);"