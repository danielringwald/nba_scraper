import os
import shutil
import datetime


def backup_db(db_path="nba_scraper.db", backup_dir="db_backups"):
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"nba_scraper_{timestamp}.db")
    shutil.copy2(db_path, backup_path)
    print(f"Backup created: {backup_path}")


if __name__ == "__main__":
    backup_db()
