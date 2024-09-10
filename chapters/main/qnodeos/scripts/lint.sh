#!/usr/bin/env sh

################################################################################
# Check writing style and other writing inconsistencies.
################################################################################

log () {
    case "$1" in
        INFO)
            echo -n -e '\033[0;32mINFO:  \033[0m'
            ;;
        WARN)
            echo -n -e '\033[0;33mWARN:  \033[0m'
            ;;
        ERROR)
            echo -n -e '\033[0;31mERROR: \033[0m'
            ;;
        *)
            ;;
    esac
    echo "$2"
}

main () {
    error=0

    # Avoid double spaces after period.
    log INFO 'Searching for double spaces after period...'
    rg '\.\s\s' -g '**/*.tex'
    # If mistakes are found (rg returns 0), print message and save error
    if [ $? -eq 0 ]; then
        log ERROR 'Found double spaces after period'
        error=1
    else
        log INFO 'No double spaces after period found'
    fi

    return $error
}

main "$@"
