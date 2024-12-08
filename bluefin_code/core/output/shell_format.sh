#!/bin/bash

# Catppuccin Mocha Color Palette
readonly ROSEWATER="\033[38;2;245;224;220m"   # #f5e0dc
readonly FLAMINGO="\033[38;2;242;205;205m"    # #f2cdcd
readonly PINK="\033[38;2;245;194;231m"        # #f5c2e7
readonly MAUVE="\033[38;2;203;166;247m"       # #cba6f7
readonly RED="\033[38;2;243;139;168m"         # #f38ba8
readonly MAROON="\033[38;2;235;160;172m"      # #eba6ac
readonly PEACH="\033[38;2;250;179;135m"       # #fab387
readonly YELLOW="\033[38;2;249;226;175m"      # #f9e2af
readonly GREEN="\033[38;2;166;227;161m"       # #a6e3a1
readonly TEAL="\033[38;2;148;226;213m"        # #94e2d5
readonly SKY="\033[38;2;137;220;235m"         # #89dceb
readonly SAPPHIRE="\033[38;2;116;199;236m"    # #74c7ec
readonly BLUE="\033[38;2;137;180;250m"        # #89b4fa
readonly LAVENDER="\033[38;2;180;190;254m"    # #b4befe

# Surface colors
readonly BASE="\033[38;2;30;30;46m"           # #1e1e2e
readonly MANTLE="\033[38;2;24;24;37m"         # #181825
readonly CRUST="\033[38;2;17;17;27m"          # #11111b

# Overlay colors
readonly SURFACE0="\033[38;2;49;50;68m"       # #313244
readonly SURFACE1="\033[38;2;69;71;90m"       # #45475a
readonly SURFACE2="\033[38;2;88;91;112m"      # #585b70

# Text styles
readonly STYLE_BOLD="\033[1m"
readonly STYLE_DIM="\033[2m"
readonly STYLE_ITALIC="\033[3m"
readonly STYLE_UNDERLINE="\033[4m"
readonly STYLE_RESET="\033[0m"

# Status indicators with Catppuccin colors
readonly SYMBOL_SUCCESS="✓"
readonly SYMBOL_ERROR="✗"
readonly SYMBOL_WARNING="!"
readonly SYMBOL_INFO="ℹ"

# Logging functions with Catppuccin colors
log_success() {
    echo -e "${GREEN}${SYMBOL_SUCCESS}${STYLE_RESET} ${LAVENDER}$1${STYLE_RESET}"
}

log_error() {
    echo -e "${RED}${SYMBOL_ERROR}${STYLE_RESET} ${FLAMINGO}$1${STYLE_RESET}" >&2
}

log_warning() {
    echo -e "${PEACH}${SYMBOL_WARNING}${STYLE_RESET} ${YELLOW}$1${STYLE_RESET}"
}

log_info() {
    echo -e "${BLUE}${SYMBOL_INFO}${STYLE_RESET} ${SKY}$1${STYLE_RESET}"
}

# Header formatting with Catppuccin colors
print_header() {
    local text="$1"
    echo -e "\n${MAUVE}${STYLE_BOLD}=== ${text} ===${STYLE_RESET}\n"
}

# Status formatting with Catppuccin colors
format_status() {
    local status="$1"
    case "${status,,}" in
        "success"|"done"|"completed") echo -e "${GREEN}${status}${STYLE_RESET}" ;;
        "error"|"failed"|"failure") echo -e "${RED}${status}${STYLE_RESET}" ;;
        "warning"|"pending") echo -e "${PEACH}${status}${STYLE_RESET}" ;;
        *) echo -e "${LAVENDER}${status}${STYLE_RESET}" ;;
    esac
}

# Progress formatting with Catppuccin colors
format_progress() {
    local current="$1"
    local total="$2"
    local percentage=$((current * 100 / total))
    echo -e "${LAVENDER}${current}${STYLE_RESET}/${BLUE}${total}${STYLE_RESET} (${SAPPHIRE}${percentage}%${STYLE_RESET})"
}

# Time formatting with Catppuccin colors
format_timestamp() {
    date "+[${SKY}%H${STYLE_RESET}:${SAPPHIRE}%M${STYLE_RESET}:${BLUE}%S${STYLE_RESET}]"
}

# Additional formatting functions with Catppuccin colors
format_value() {
    local value="$1"
    echo -e "${LAVENDER}${value}${STYLE_RESET}"
}

format_key() {
    local key="$1"
    echo -e "${MAUVE}${key}${STYLE_RESET}"
}

format_path() {
    local path="$1"
    echo -e "${BLUE}${path}${STYLE_RESET}"
}

format_url() {
    local url="$1"
    echo -e "${SAPPHIRE}${STYLE_UNDERLINE}${url}${STYLE_RESET}"
}

format_diff_added() {
    local text="$1"
    echo -e "${GREEN}+${text}${STYLE_RESET}"
}

format_diff_removed() {
    local text="$1"
    echo -e "${RED}-${text}${STYLE_RESET}"
}

format_diff_modified() {
    local text="$1"
    echo -e "${YELLOW}~${text}${STYLE_RESET}"
}

# Box-drawing characters
readonly BOX_TL="┌"
readonly BOX_TR="┐"
readonly BOX_BL="└"
readonly BOX_BR="┘"
readonly BOX_H="─"
readonly BOX_V="│"
readonly BOX_VR="├"
readonly BOX_VL="┤"
readonly BOX_HU="┴"
readonly BOX_HD="┬"
readonly BOX_C="┼"

# Table formatting with Catppuccin colors
format_table_border() {
    local width="$1"
    local style="${2:-primary}"  # primary, secondary, or accent
    local color
    
    case "$style" in
        "primary") color="$MAUVE" ;;
        "secondary") color="$BLUE" ;;
        "accent") color="$PEACH" ;;
        *) color="$SURFACE2" ;;
    esac
    
    echo -e "${color}${BOX_H}$(printf '%*s' "$width" '' | tr ' ' "$BOX_H")${BOX_H}${STYLE_RESET}"
}

format_table_row() {
    local text="$1"
    local style="${2:-primary}"
    local color
    
    case "$style" in
        "primary") color="$MAUVE" ;;
        "secondary") color="$BLUE" ;;
        "accent") color="$PEACH" ;;
        *) color="$SURFACE2" ;;
    esac
    
    echo -e "${color}${BOX_V}${STYLE_RESET} ${text} ${color}${BOX_V}${STYLE_RESET}"
}

format_table_header() {
    local text="$1"
    local width="$2"
    local style="${3:-primary}"
    local color
    
    case "$style" in
        "primary") color="$MAUVE" ;;
        "secondary") color="$BLUE" ;;
        "accent") color="$PEACH" ;;
        *) color="$SURFACE2" ;;
    esac
    
    # Top border
    echo -e "${color}${BOX_TL}$(printf '%*s' "$width" '' | tr ' ' "$BOX_H")${BOX_TR}${STYLE_RESET}"
    
    # Header text
    echo -e "${color}${BOX_V}${STYLE_RESET}${STYLE_BOLD} ${text}$(printf "%$((width-${#text}-1))s") ${color}${BOX_V}${STYLE_RESET}"
    
    # Bottom border
    echo -e "${color}${BOX_VR}$(printf '%*s' "$width" '' | tr ' ' "$BOX_H")${BOX_VL}${STYLE_RESET}"
}

format_table_footer() {
    local width="$1"
    local style="${2:-primary}"
    local color
    
    case "$style" in
        "primary") color="$MAUVE" ;;
        "secondary") color="$BLUE" ;;
        "accent") color="$PEACH" ;;
        *) color="$SURFACE2" ;;
    esac
    
    echo -e "${color}${BOX_BL}$(printf '%*s' "$width" '' | tr ' ' "$BOX_H")${BOX_BR}${STYLE_RESET}"
}

# Example table usage:
# print_table() {
#     local title="$1"
#     local width="$2"
#     local style="${3:-primary}"
#     
#     format_table_header "$title" "$width" "$style"
#     format_table_row "Row 1 content" "$style"
#     format_table_row "Row 2 content" "$style"
#     format_table_footer "$width" "$style"
# }

# Grid table formatting
format_grid_header() {
    local headers=("$@")
    local style="${headers[-1]}"
    unset 'headers[${#headers[@]}-1]'
    local color
    
    case "$style" in
        "primary") color="$MAUVE" ;;
        "secondary") color="$BLUE" ;;
        "accent") color="$PEACH" ;;
        *) color="$SURFACE2" ;;
    esac
    
    # Calculate column widths
    local -a widths=()
    for header in "${headers[@]}"; do
        widths+=($((${#header} + 4)))  # padding
    done
    
    # Top border
    echo -n -e "${color}${BOX_TL}"
    local first=true
    for width in "${widths[@]}"; do
        if [ "$first" = true ]; then
            first=false
        else
            echo -n -e "${BOX_HD}"
        fi
        printf '%*s' "$width" '' | tr ' ' "$BOX_H"
    done
    echo -e "${BOX_TR}${STYLE_RESET}"
    
    # Headers
    echo -n -e "${color}${BOX_V}${STYLE_RESET}"
    for i in "${!headers[@]}"; do
        printf " ${STYLE_BOLD}%-${widths[i]}s${STYLE_RESET}" "${headers[i]}"
        echo -n -e "${color}${BOX_V}${STYLE_RESET}"
    done
    echo
    
    # Separator
    echo -n -e "${color}${BOX_VR}"
    first=true
    for width in "${widths[@]}"; do
        if [ "$first" = true ]; then
            first=false
        else
            echo -n -e "${BOX_C}"
        fi
        printf '%*s' "$width" '' | tr ' ' "$BOX_H"
    done
    echo -e "${BOX_VL}${STYLE_RESET}"
}

format_grid_row() {
    local color="$SURFACE2"
    local -a cells=("$@")
    local style="${cells[-1]}"
    unset 'cells[${#cells[@]}-1]'
    
    case "$style" in
        "primary") color="$MAUVE" ;;
        "secondary") color="$BLUE" ;;
        "accent") color="$PEACH" ;;
        *) color="$SURFACE2" ;;
    esac
    
    # Calculate column widths
    local -a widths=()
    for cell in "${cells[@]}"; do
        widths+=($((${#cell} + 4)))  # padding
    done
    
    # Row content
    echo -n -e "${color}${BOX_V}${STYLE_RESET}"
    for i in "${!cells[@]}"; do
        printf " %-${widths[i]}s" "${cells[i]}"
        echo -n -e "${color}${BOX_V}${STYLE_RESET}"
    done
    echo
}

format_grid_footer() {
    local -a widths=("$@")
    local style="${widths[-1]}"
    unset 'widths[${#widths[@]}-1]'
    local color
    
    case "$style" in
        "primary") color="$MAUVE" ;;
        "secondary") color="$BLUE" ;;
        "accent") color="$PEACH" ;;
        *) color="$SURFACE2" ;;
    esac
    
    # Bottom border
    echo -n -e "${color}${BOX_BL}"
    local first=true
    for width in "${widths[@]}"; do
        if [ "$first" = true ]; then
            first=false
        else
            echo -n -e "${BOX_HU}"
        fi
        printf '%*s' "$width" '' | tr ' ' "$BOX_H"
    done
    echo -e "${BOX_BR}${STYLE_RESET}"
}

# Example grid table usage:
# print_grid_table() {
#     format_grid_header "Column 1" "Column 2" "Column 3" "primary"
#     format_grid_row "Data 1" "Data 2" "Data 3" "primary"
#     format_grid_row "More Data 1" "More Data 2" "More Data 3" "primary"
#     format_grid_footer "12" "12" "12" "primary"  # Column widths
# } 