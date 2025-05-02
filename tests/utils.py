def get_query_params(app_test):
    return app_test.query_params


def set_query_params(app_test, params):
    app_test.query_params.update(params)
