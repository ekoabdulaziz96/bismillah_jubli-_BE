from app import create_app, shell_plus_command

# ----------------------------- init app
app = create_app()
app.cli.add_command(shell_plus_command)

# ----------------------------- route index
@app.route('/', methods=['GET'])
def index():
    print('print_log_core_notif')
    app.logger.debug('app_logger_debug_core_notif')
    app.logger.info('app_logger_info_core_notif')
    return 'core-notif', 200


# -------------------------------------------
# see folder ./urls for more route app endpoint
