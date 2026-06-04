#!/usr/bin/env python3

# Variables
name = "El J"
age = 20
is_cloud_engineer = True

# String formatting
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Cloud Engineer: {is_cloud_engineer}")

# Lists
servers = ["web1", "web2", "db1", "db2"]
print(f"\nServers: {servers}")
print(f"First server: {servers[0]}")
print(f"Total servers: {len(servers)}")

# Dictionary — like JSON
server_info = {
    "name": "web1",
    "ip": "10.0.0.1",
    "port": 80,
    "status": "running"
}

print(f"\nServer info: {server_info}")
print(f"Server IP: {server_info['ip']}")
print(f"Server status: {server_info['status']}")

# Loop through servers
print("\nAll servers:")
for server in servers:
    print(f"  - {server}")