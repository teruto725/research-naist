
import sqlite3 as sql

if __name__ == "__main__":
  with sql.connect("crawl_db.sqlite3") as conn:
    conn.execute("DROP TABLE DIFF")
  