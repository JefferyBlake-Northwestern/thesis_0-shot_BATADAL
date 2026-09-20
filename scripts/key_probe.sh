#!/bin/bash
# key-probe.sh — press a key, see what bytes it produces
printf "Press a key (Ctrl+C to exit): "
while true; do
    IFS= read -rsn1 c
    printf "byte: hex=%02x  dec=%d  " "'$c" "'$c"
    if [ -n "$c" ] && printf '%s' "$c" | grep -q '[[:print:]]'; then
        printf "char='%s'\n" "$c"
    else
        printf "(non-printable)\n"
    fi
done
