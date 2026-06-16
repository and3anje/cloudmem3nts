#!/usr/bin/env python3
import sqlite3
import datetime

DB_FILE = "servers.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS servers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, ip TEXT NOT NULL, status TEXT NOT NULL, last_checked TEXT NOT NULL)")
    conn.commit()
    conn.close()
    print("Table created or already exists")

def insert_server(name, ip, status):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO servers (name, ip, status, last_checked) VALUES (?, ?, ?, ?)", (name, ip, status, timestamp))
    conn.commit()
    conn.close()
    print(f"Inserted: {name}")

def get_all_servers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servers")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_status(name, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE servers SET status = ?, last_checked = ? WHERE name = ?", (new_status, timestamp, name))
    conn.commit()
    conn.close()
    print(f"Updated {name} to {new_status}")

def get_unhealthy_servers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, ip, status FROM servers WHERE status != 'HEALTHY'")
    rows = cursor.fetchall()
    conn.close()
    return rows

create_table()

insert_server("web-server-01", "10.0.0.1", "HEALTHY")
insert_server("db-server-01", "10.0.0.2", "HEALTHY")
insert_server("api-server-01", "10.0.0.3", "HEALTHY")

print("\n=== All Servers ===")
for row in get_all_servers():
    print(row)

update_status("web-server-01", "DEGRADED")

print("\n=== Unhealthy Servers ===")
for row in get_unhealthy_servers():
    print(row)