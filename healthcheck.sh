#!/bin/bash

LOGFILE=~/cloudjourney/health.log
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log_message() {
    echo "[$TIMESTAMP] $1" >> $LOGFILE
    echo "[$TIMESTAMP] $1"
}

check_disk() {
    USAGE=$(df -h / | tail -1 | awk '{print $5}' | tr -d '%')
    if [ $USAGE -gt 70 ]; then
        log_message "WARNING: Disk usage is ${USAGE}%"
    else
        log_message "OK: Disk usage is ${USAGE}%"
    fi
}

check_memory() {
    AVAILABLE=$(cat /proc/meminfo | grep MemAvailable | awk '{print $2}')
    if [ $AVAILABLE -lt 500000 ]; then
        log_message "WARNING: Low memory - ${AVAILABLE}kB available"
    else
        log_message "OK: Memory available - ${AVAILABLE}kB"
    fi
}

check_nginx() {
    if ps aux | grep -q "[n]ginx"; then
        log_message "OK: Nginx is running"
    else
        log_message "WARNING: Nginx is NOT running"
    fi
}

check_internet() {
    if ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1; then
        log_message "OK: Internet is reachable"
    else
        log_message "WARNING: Internet is unreachable"
    fi
}

check_ssh() {
    if ps aux | grep -q "[s]shd"; then
        log_message "OK: SSH is running"
    else
        log_message "WARNING: SSH is NOT running"
    fi
}

check_users() {
    USERS=$(who | wc -l)
    if [ $USERS -gt 3 ]; then
        log_message "WARNING: $USERS users logged in"
    else
        log_message "OK: $USERS users logged in"
    fi
}

# Main execution
log_message " Health Check Started "
check_disk
check_memory
check_nginx
check_internet
check_ssh
check_users
log_message " Health Check Complete "