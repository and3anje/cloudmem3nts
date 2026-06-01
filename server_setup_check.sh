#!/bin/bash

LOGFILE=/workspaces/cloudmem3nts/server_setup_check.log
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log_message() {
    echo "[$TIMESTAMP] $1" >> $LOGFILE
    echo "[$TIMESTAMP] $1"
}

firewall_config() {
    sudo ufw default deny incoming
    log_message "Incoming traffic denied by default"
    sudo ufw default allow outgoing
    log_message "Outgoing traffic allowed"
    sudo ufw allow 22
    log_message "SSH allowed on port 22"
    sudo ufw allow 80
    log_message "HTTP allowed on port 80"
    sudo ufw allow 443
    log_message "HTTPS allowed on port 443"
    sudo ufw --force enable
    log_message "Firewall enabled"
}

check_internet() {
    if curl -s --max-time 5 https://google.com > /dev/null 2>&1; then
        log_message "OK: Internet is reachable"
    else
        log_message "WARNING: Internet is unreachable"
    fi
}

dns_resolution() {
    if dig google.com A +short > /dev/null 2>&1; then
        log_message "OK: DNS resolution working"
    else
        log_message "WARNING: DNS resolution failed"
    fi
}

check_nginx() {
    if ps aux | grep -q "[n]ginx"; then
        log_message "OK: Nginx is running"
    else
        log_message "WARNING: Nginx is not running — starting it"
        sudo nginx
        log_message "Nginx started"
    fi
}

check_open_ports() {
    log_message "Open TCP ports: $(ss -tlnp | grep LISTEN | awk '{print $4}' | tr '\n' ' ')"
    log_message "Open UDP ports: $(ss -ulnp | grep UNCONN | awk '{print $4}' | tr '\n' ' ')"
}

# Main execution
log_message "=== Server Setup Check Started ==="
firewall_config
check_internet
dns_resolution
check_nginx
check_open_ports
log_message "=== Server Setup Check Complete ==="