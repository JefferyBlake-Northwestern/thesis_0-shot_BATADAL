#!/bin/zsh
# monitor.sh — interactive menu of shell scripts from a configured directory.

# Ensure standard commands are findable regardless of how the script is invoked
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

SCRIPT_DIR="${SCRIPT_DIR:-./scripts}"

if [ ! -d "$SCRIPT_DIR" ]; then
    printf "Error: directory '%s' does not exist.\n" "$SCRIPT_DIR" >&2
    exit 1
fi

SCRIPTS=()
for f in "$SCRIPT_DIR"/*.sh(N); do
    SCRIPTS+=("$f")
done

if [ "${#SCRIPTS[@]}" -eq 0 ]; then
    printf "No .sh files found in '%s'.\n" "$SCRIPT_DIR" >&2
    exit 1
fi

BOLD=$'\e[1m'
DIM=$'\e[2m'
INVERT=$'\e[7m'
RESET=$'\e[0m'
CLEAR=$'\e[2J\e[H'
HIDE_CURSOR=$'\e[?25l'
SHOW_CURSOR=$'\e[?25h'

selected=0
n_items="${#SCRIPTS[@]}"
max_idx="$n_items"

render_menu() {
    printf "%s" "$CLEAR"
    printf "%sScript menu — arrows or j/k to move, Enter to run, q to quit%s\n" "$BOLD" "$RESET"
    printf "%sDirectory:%s %s\n" "$DIM" "$RESET" "$SCRIPT_DIR"
    printf "%sFound:%s %d script(s)\n\n" "$DIM" "$RESET" "${#SCRIPTS[@]}"

    local i
    for ((i = 1; i <= ${#SCRIPTS[@]}; i++)); do
        local basename_val="$(basename "${SCRIPTS[$i]}")"
        local idx=$((i - 1))
        if [ "$idx" -eq "$selected" ]; then
            printf "  %s> %s%s\n" "$INVERT" "$basename_val" "$RESET"
        else
            printf "    %s\n" "$basename_val"
        fi
    done

    if [ "$selected" -eq "$n_items" ]; then
        printf "\n  %s> Quit%s\n" "$INVERT" "$RESET"
    else
        printf "\n    Quit\n"
    fi
}

run_script() {
    local path="$1"
    local basename_val="$(/usr/bin/basename "$path")"

    local project_root="$(cd "$SCRIPT_DIR/.." && pwd)"
    local abs_path="$(cd "$(/usr/bin/dirname "$path")" && pwd)/$basename_val"

    printf "%s" "$SHOW_CURSOR"
    /usr/bin/clear
    printf "%s=== running: %s ===%s\n" "$BOLD" "$basename_val" "$RESET"
    printf "%s(cwd: %s)%s\n\n" "$DIM" "$project_root" "$RESET"

    if [ ! -f "$abs_path" ]; then
        printf "Error: script not found: %s\n" "$abs_path" >&2
    else
        (
            cd "$project_root" || exit 1
            /bin/zsh "$abs_path"
        )
    fi
    local rc=$?

    printf "\n%s─── exit code: %d ───%s\n" "$DIM" "$rc" "$RESET"
    printf "%sPress any key to return to menu...%s" "$BOLD" "$RESET"
    read -sk 1
    printf "%s" "$HIDE_CURSOR"
}

# Read a single logical keypress. Returns: UP, DOWN, ENTER, QUIT, or raw byte.
read_key() {
    local buf rest
    read -sk 1 buf
    if [[ "$buf" == $'\e' ]]; then
        read -sk 2 -t 0.05 rest 2>/dev/null
        buf="${buf}${rest}"
    fi
    case "$buf" in
        $'\e[A') echo "UP" ;;
        $'\e[B') echo "DOWN" ;;
        $'\e[C') echo "RIGHT" ;;
        $'\e[D') echo "LEFT" ;;
        $'\e')   echo "QUIT" ;;
        $'\n'|"") echo "ENTER" ;;
        j|J)     echo "DOWN" ;;
        k|K)     echo "UP" ;;
        q|Q)     echo "QUIT" ;;
        *)       echo "$buf" ;;
    esac
}

trap 'printf "%s" "$SHOW_CURSOR"; clear; exit' INT TERM EXIT

printf "%s" "$HIDE_CURSOR"

while true; do
    render_menu
    action="$(read_key)"

    case "$action" in
        UP)
            selected=$((selected - 1))
            if [ "$selected" -lt 0 ]; then
                selected="$max_idx"
            fi
            ;;
        DOWN)
            selected=$((selected + 1))
            if [ "$selected" -gt "$max_idx" ]; then
                selected=0
            fi
            ;;
        ENTER)
            if [ "$selected" -eq "$n_items" ]; then
                break
            fi
            run_script "${SCRIPTS[$((selected + 1))]}"
            ;;
        QUIT)
            break
            ;;
    esac
done

printf "%s" "$SHOW_CURSOR"
clear
