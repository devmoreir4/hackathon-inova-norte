import os

def reset_database():
    db_files = [
        "data/sicoob_dev.db",
        "data/sicoob_dev.db-journal",
        "data/test.db",
        "data/test.db-journal",
    ]
    
    removed_count = 0
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"Removed: {db_file}")
                removed_count += 1
            except PermissionError:
                print(f"Error: Cannot remove {db_file}")
                print("Stop the API first, then run this script")
            except Exception as e:
                print(f"Error removing {db_file}: {e}")
    
    if removed_count > 0:
        print(f"Database reset complete. Removed {removed_count} file(s)")
    else:
        print("No database files were removed")

if __name__ == "__main__":
    reset_database()
