#!/usr/bin/env python3
import os
import requests
import json
from datetime import datetime

# ── PART 1: Simulating Azure SDK Pattern ──

def get_azure_token():
    """
    In real Azure this would use:
    from azure.identity import DefaultAzureCredential
    credential = DefaultAzureCredential()
    token = credential.get_token("https://management.azure.com/.default")
    
    For now we simulate the pattern
    """
    # These would come from Azure App Registration
    tenant_id = os.environ.get('AZURE_TENANT_ID', 'demo-tenant')
    client_id = os.environ.get('AZURE_CLIENT_ID', 'demo-client')
    client_secret = os.environ.get('AZURE_CLIENT_SECRET', 'demo-secret')
    
    print("=== Azure Authentication ===")
    print(f"Tenant ID: {tenant_id}")
    print(f"Client ID: {client_id}")
    print(f"Secret: {'*' * len(client_secret)}")
    
    return {"tenant": tenant_id, "client": client_id}

# ── PART 2: Real Azure Public API Call ──

def get_azure_status():
    """
    Azure Status API - no auth needed
    Shows current status of all Azure services globally
    """
    try:
        url = "https://azure.status.microsoft/api/v2/status.json"
        
        print("\n=== Azure Service Status ===")
        response = requests.get(url, timeout=15)
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Navigate the response
            status = data['status']['description']
            updated = data['updatedTime']
            
            print(f"Overall status: {status}")
            print(f"Last updated: {updated}")
            
            # Show affected services if any
            if 'services' in data:
                print(f"Total services monitored: {len(data['services'])}")
                
    except requests.exceptions.Timeout:
        print("Azure status API timed out")
    except Exception as e:
        print(f"Error: {e}")

# ── PART 3: Simulating VM Management ──

def list_virtual_machines(subscription_id):
    """
    Real code would be:
    from azure.mgmt.compute import ComputeManagementClient
    client = ComputeManagementClient(credential, subscription_id)
    vms = client.virtual_machines.list_all()
    """
    # Simulated VM data — same structure Azure returns
    vms = [
        {
            "name": "web-server-01",
            "location": "eastafrica",
            "properties": {
                "hardwareProfile": {"vmSize": "Standard_B2s"},
                "storageProfile": {"osDisk": {"osType": "Linux"}},
                "provisioningState": "Succeeded"
            }
        },
        {
            "name": "db-server-01",
            "location": "eastafrica",
            "properties": {
                "hardwareProfile": {"vmSize": "Standard_B4ms"},
                "storageProfile": {"osDisk": {"osType": "Linux"}},
                "provisioningState": "Succeeded"
            }
        },
        {
            "name": "dev-server-01",
            "location": "eastafrica",
            "properties": {
                "hardwareProfile": {"vmSize": "Standard_B1s"},
                "storageProfile": {"osDisk": {"osType": "Linux"}},
                "provisioningState": "Failed"
            }
        }
    ]
    
    print(f"\n=== Virtual Machines in subscription {subscription_id} ===")
    print(f"Total VMs: {len(vms)}\n")
    
    for vm in vms:
        name = vm['name']
        location = vm['location']
        size = vm['properties']['hardwareProfile']['vmSize']
        os_type = vm['properties']['storageProfile']['osDisk']['osType']
        state = vm['properties']['provisioningState']
        
        status_icon = "✓" if state == "Succeeded" else "✗"
        print(f"{status_icon} {name}")
        print(f"   Location: {location}")
        print(f"   Size: {size}")
        print(f"   OS: {os_type}")
        print(f"   State: {state}\n")

# ── PART 4: Save Results to JSON ──

def save_report(data, filename):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report = {
        "generated_at": timestamp,
        "data": data
    }
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to {filename}")

# Main execution
credentials = get_azure_token()
get_azure_status()
list_virtual_machines("demo-subscription-123")
save_report(credentials, "azure_report.json")