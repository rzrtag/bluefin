#!/bin/bash

# Set the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
cd "$PROJECT_ROOT"

# Source the shell formatting functions
source "$PROJECT_ROOT/bluefin_code/core/output/shell_format.sh"

# Configure logging
LOG_DIR="$PROJECT_ROOT/bluefin_data/logs/nba/ssim"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/pipeline_$(date +%Y-%m-%d).log"

# Function to log messages
log() {
    local level=$1
    local message=$2
    local timestamp=$(format_timestamp)
    
    # Log to file
    echo "$timestamp $level: $message" >> "$LOG_FILE"
    
    # Print to console with color based on level
    case "$level" in
        "✓") log_success "$message" ;;
        "!") log_error "$message" ;;
        "?") log_warning "$message" ;;
        *) log_info "$message" ;;
    esac
}

# Function to run fetch step
run_fetch() {
    print_header "Fetching SaberSim Data"
    
    if python bluefin_code/nba/ssim/fetch.py "$@"; then
        log "✓" "fetch done"
        return 0
    else
        log "!" "fetch failed"
        return 1
    fi
}

# Function to run process step
run_process() {
    print_header "Processing SaberSim Data"
    
    if python bluefin_code/nba/ssim/process.py "$@"; then
        log "✓" "process done"
        return 0
    else
        log "!" "process failed"
        return 1
    fi
}

# Main execution
print_header "SaberSim Pipeline: $(date +%Y-%m-%d)"

# Run fetch step
run_fetch "$@"
FETCH_STATUS=$?

# Run process step if fetch succeeded
if [ $FETCH_STATUS -eq 0 ]; then
    run_process "$@"
    PROCESS_STATUS=$?
else
    log "!" "skipping process step due to fetch failure"
    PROCESS_STATUS=1
fi

# Final status check
if [ $FETCH_STATUS -eq 0 ] && [ $PROCESS_STATUS -eq 0 ]; then
    log "✓" "pipeline completed successfully"
    exit 0
else
    log "!" "pipeline failed"
    exit 1
fi 