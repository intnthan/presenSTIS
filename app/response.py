from flask import jsonify, make_response

def success (data, message):
    return make_response(jsonify({
        'status': 'success',
        'data': data,
        'message': message
    }), 200)
    
def error (data, message):
    return make_response(jsonify({
        'status': 'error',
        'data': data,
        'message': message
    }), 400)