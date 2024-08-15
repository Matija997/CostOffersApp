import main_menu_window
import database as db
import os
import shutil

conn = db.get_connection()
files = os.listdir('backups')
version = len(files)
backup_name = f"backups/data_{version}.0.db"
shutil.copy('data.db', backup_name)
conn.close()
main_menu_window.create_main_menu()
