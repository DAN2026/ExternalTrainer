from blinker import signal

set_ini = signal('set-ini')
set_mipbias = signal('set-mipbias')
set_testing_ini = signal('set-testing-ini')

set_fov = signal('set-fov')
set_view_distance = signal('set-view-distance')
set_gamma = signal('set-gamma')

set_display_batch = signal('set-display-batch')

set_environment = signal('set-environment')
set_beer = signal('set-beer')
set_fullbright = signal('set-fullbright')
set_no_trees = signal('set-no-trees')
set_scouting = signal('set-scouting')
set_pretty = signal('set-pretty')
set_no_structures = signal('set-no-structures')

set_damage_numbers = signal('set-damage-numbers')
set_stalker_vision = signal('set-stalker-vision')

get_fov = signal('get-fov')
get_gamma = signal('get-gamma')
get_view_distance = signal('get-view-distance')

on_connection_change = signal('on-connection-change')
request_reconnect = signal('request-reconnect')
request_shutdown = signal('request-shutdown')

request_save_config = signal('request-save-config')
request_load_config = signal('request-load-config')
on_save_success = signal('on-save-success')
on_save_failure = signal('on-save-failure')
on_load_complete = signal('on-load-complete')


# Hotkey stuff

get_hotkeys = signal('get-hotkeys')
request_hotkey_sync = signal('request-hotkey-sync')



request_toggle_no_water = signal('request-toggle-no-water')
request_toggle_fullbright = signal('request-toggle-fullbright')
request_toggle_beer_xz = signal('request-toggle-beer-xz')
request_toggle_environment = signal('request-toggle-environment')
request_normal_ini = signal('request-normal-ini')
request_hard_ini = signal('request-hard-ini')

request_game_lock = signal('request-game-lock')
request_open_close_menu = signal('request-open-close-menu')

on_game_lock_change = signal("on_game_lock_change")