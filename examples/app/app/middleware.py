from flask import jsonify, make_response


def render_response(fn):
    """Response renderer middleware."""
    def decorator(*args, **kwargs):
        response, code = fn(*args, **kwargs)
        return make_response(jsonify(response), code)
    return decorator
