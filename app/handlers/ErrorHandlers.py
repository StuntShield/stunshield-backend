from flask import jsonify


class ErrorHandlers:
    def common(e):
        # note that we set the 404 status explicitly
        return (
            jsonify(
                {'code': e.code, 'name': e.name, 'description': e.description},
            ),
            500,
        )

    def page_not_found(e):
        # note that we set the 404 status explicitly
        return (
            jsonify(
                {'code': e.code, 'name': e.name, 'description': e.description},
            ),
            404,
        )

    def internal_server_error(e):
        # note that we set the 404 status explicitly
        return (
            jsonify(
                {'code': e.code, 'name': e.name, 'description': e.description},
            ),
            500,
        )

    def method_not_allowed(e):
        # note that we set the 404 status explicitly
        return (
            jsonify(
                {'code': e.code, 'name': e.name, 'description': e.description},
            ),
            500,
        )