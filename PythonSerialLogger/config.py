Settings = {
    "usb_port": "/dev/ttyUSB0",
    "baud": 115200,
    "socket_port": 12345,
    "arduino_timeout": 8,

    "this also doubles as the folder name": "",
    "log_prefix": "testStand",
    "log_path_relative": "logs_RPi_80",

    "boot_keyword": "==SETUP==",
    "tag_character": "!",
    "legacy_character": "=",
    # srsly why not use !header !setup and then check the rest, saves computing, later optimisation option
    "header_keywords": ("!header_begin", "!header_end"),
    "setup_keywords": ("!setup_begin", "!setup_end"),
    "globals_keywords": ("!globals_begin", "!globals_end"),
    "parse_keywords": ("!parse_begin", "!parse_end"),
    "event_call_keyword": "!eventcall",

    "buffer_lines": 50
}
