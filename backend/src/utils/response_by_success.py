def response_by_success(success, is_remove=False):
    if success:
        code = 200 if not is_remove else 204
        return {
            'ok': True,
            'message': 'Operation completed successfully'
        }, code
    return {'ok': False, 'message': 'Unsuccessful operation'}, 422
