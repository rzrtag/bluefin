#!/bin/bash

# Set the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Source the shell formatting functions
source "$PROJECT_ROOT/core/output/shell_format.sh"

# Configure logging
LOG_DIR="$PROJECT_ROOT/../bluefin_data/logs/nba"
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

# Function to run bettingpros pipeline
run_bettingpros() {
    print_header "BPRO"
    cd "$PROJECT_ROOT/nba/bettingpros"
    
    if python run_bpro_pipeline.py "$@"; then
        log "✓" "bpro done"
        return 0
    else
        log "!" "bpro failed"
        return 1
    fi
}

# Function to run sabersim pipeline
run_sabersim() {
    print_header "SABER"
    cd "$PROJECT_ROOT/nba/sabersim"
    
    if ./run_pipeline.sh; then
        log "✓" "saber done"
        return 0
    else
        log "!" "saber failed"
        return 1
    fi
}

# Main execution
run_bettingpros "$@"
BETTINGPROS_STATUS=$?

run_sabersim
SABERSIM_STATUS=$?

# Final status check
if [ $BETTINGPROS_STATUS -eq 0 ] && [ $SABERSIM_STATUS -eq 0 ]; then
    log "✓" "all done"
    exit 0
else
    log "!" "pipeline failed"
    exit 1
fi 