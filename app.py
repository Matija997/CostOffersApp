from main_menu_window import create_main_menu
import database as db
import os
import shutil

conn = db.get_connection()

backup_files = sorted(
    [f for f in os.listdir('backups')
     if f.startswith('data_') and f.endswith('.db')],
    key=lambda x: int(x.split('_')[1].split('.')[0]), reverse=True
)

for file in backup_files:
    version = int(file.split('_')[1].split('.')[0])
    new_version = version + 1
    new_name = f"backups/data_{new_version}.db"
    shutil.move(f'backups/{file}', new_name)

new_backup = "backups/data_1.db"
shutil.copy('data.db', new_backup)
conn.close()
create_main_menu()
