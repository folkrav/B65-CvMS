from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return '<h3>404</h3>', 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return '<h3>500</h3>', 500
