#!/bin/bash

# Source shell formatting
source "$(dirname "$0")/../../core/output/shell_format.sh"

# Set paths
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OLD_DIR="$PROJECT_ROOT/sabersim"
NEW_DIR="$PROJECT_ROOT/ssim"
DATA_ROOT="$PROJECT_ROOT/../bluefin_data/nba"
OLD_DATA_DIR="$DATA_ROOT/sabersim"
NEW_DATA_DIR="$DATA_ROOT/ssim"

# Function to migrate tests
migrate_tests() {
    print_header "Migrating Tests"
    
    # Create new tests directory if it doesn't exist
    mkdir -p "$NEW_DIR/tests"
    
    if [ -d "$OLD_DIR/tests" ]; then
        # Copy test files
        cp "$OLD_DIR/tests/test_validate.py" "$NEW_DIR/tests/" 2>/dev/null || true
        cp "$OLD_DIR/tests/test_process.py" "$NEW_DIR/tests/" 2>/dev/null || true
        cp "$OLD_DIR/tests/__init__.py" "$NEW_DIR/tests/" 2>/dev/null || true
        
        log_success "Migrated test files"
    else
        log_warning "No tests directory found at $OLD_DIR/tests"
    fi
}

# Function to migrate data
migrate_data() {
    print_header "Migrating Data"
    
    # Create new data directories if they don't exist
    mkdir -p "$NEW_DATA_DIR/raw"
    mkdir -p "$NEW_DATA_DIR/processed"
    
    if [ -d "$OLD_DATA_DIR" ]; then
        log_info "Moving data from $OLD_DATA_DIR to $NEW_DATA_DIR"
        
        # Move raw data
        if [ -d "$OLD_DATA_DIR/raw" ]; then
            for month_dir in "$OLD_DATA_DIR/raw"/*; do
                if [ -d "$month_dir" ]; then
                    month=$(basename "$month_dir")
                    mkdir -p "$NEW_DATA_DIR/raw/$month"
                    mv "$month_dir"/* "$NEW_DATA_DIR/raw/$month/" 2>/dev/null || true
                    log_success "Migrated raw data for $month"
                fi
            done
        fi
        
        # Move processed data
        if [ -d "$OLD_DATA_DIR/processed" ]; then
            for month_dir in "$OLD_DATA_DIR/processed"/*; do
                if [ -d "$month_dir" ]; then
                    month=$(basename "$month_dir")
                    mkdir -p "$NEW_DATA_DIR/processed/$month"
                    mv "$month_dir"/* "$NEW_DATA_DIR/processed/$month/" 2>/dev/null || true
                    log_success "Migrated processed data for $month"
                fi
            done
        fi
    else
        log_warning "No old data directory found at $OLD_DATA_DIR"
    fi
}

# Function to cleanup old files
cleanup_old_files() {
    print_header "Cleaning Up Old Files"
    
    # List of files to remove
    old_files=(
        "$OLD_DIR/fetch.py"
        "$OLD_DIR/process.py"
        "$OLD_DIR/run_pipeline.sh"
        "$OLD_DIR/update_config.py"
        "$OLD_DIR/update_daily.sh"
        "$OLD_DIR/metrics.py"
        "$OLD_DIR/validate.py"
        "$OLD_DIR/batch_process.py"
        "$OLD_DIR/config.yaml"
        "$OLD_DIR/COLUMNS.md"
        "$OLD_DIR/CONFIG.md"
        "$OLD_DIR/COLUMN_ABBREV.md"
        "$OLD_DIR/__init__.py"
    )
    
    # Remove each file
    for file in "${old_files[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            log_success "Removed $file"
        fi
    done
    
    # Remove empty directories
    if [ -d "$OLD_DIR" ]; then
        # Remove __pycache__ first
        find "$OLD_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        
        # Remove tests directory if empty
        if [ -d "$OLD_DIR/tests" ]; then
            rmdir "$OLD_DIR/tests" 2>/dev/null && \
                log_success "Removed empty tests directory" || \
                log_warning "Could not remove tests directory (might not be empty)"
        fi
        
        # Try to remove old directory
        rmdir "$OLD_DIR" 2>/dev/null && \
            log_success "Removed empty directory $OLD_DIR" || \
            log_warning "Could not remove $OLD_DIR (might not be empty)"
    fi
    
    # Clean up old data directory if empty
    if [ -d "$OLD_DATA_DIR" ]; then
        find "$OLD_DATA_DIR" -type d -empty -delete 2>/dev/null
        log_success "Cleaned up empty directories in $OLD_DATA_DIR"
    fi
}

# Function to verify new structure
verify_structure() {
    print_header "Verifying New Structure"
    
    # List of required files
    required_files=(
        "$NEW_DIR/fetch.py"
        "$NEW_DIR/process.py"
        "$NEW_DIR/run_ssim_pipeline.sh"
        "$NEW_DIR/README.md"
        "$NEW_DIR/config/config.yaml"
        "$NEW_DIR/config/columns.yaml"
        "$NEW_DIR/config/mappings.yaml"
        "$NEW_DIR/tests/__init__.py"
        "$NEW_DIR/tests/test_process.py"
        "$NEW_DIR/tests/test_validate.py"
    )
    
    # Check each required file
    local all_good=true
    format_grid_header "File" "Status" "primary"
    
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            format_grid_row "$(basename "$file")" "$(format_status "success")" "primary"
        else
            format_grid_row "$(basename "$file")" "$(format_status "error")" "primary"
            all_good=false
        fi
    done
    
    format_grid_footer "20" "8" "primary"
    
    if [ "$all_good" = true ]; then
        log_success "All required files present"
        return 0
    else
        log_error "Some required files are missing"
        return 1
    fi
}

# Main execution
print_header "SaberSim Cleanup and Migration"

# Parse arguments
case "$1" in
    "--help"|"-h")
        print_header "Usage"
        format_table_header "Command Options" 50 "primary"
        format_table_row "$0              # Run all steps" "primary"
        format_table_row "$0 --migrate    # Only migrate data" "primary"
        format_table_row "$0 --tests      # Only migrate tests" "primary"
        format_table_row "$0 --cleanup    # Only cleanup old files" "primary"
        format_table_row "$0 --verify     # Only verify structure" "primary"
        format_table_footer 50 "primary"
        exit 0
        ;;
    "--migrate")
        migrate_data
        ;;
    "--tests")
        migrate_tests
        ;;
    "--cleanup")
        cleanup_old_files
        ;;
    "--verify")
        verify_structure
        ;;
    *)
        # Run all steps
        migrate_data
        migrate_tests
        cleanup_old_files
        verify_structure
        ;;
esac

# Final status
if [ $? -eq 0 ]; then
    log_success "Cleanup completed successfully"
    exit 0
else
    log_error "Cleanup completed with errors"
    exit 1
fi 