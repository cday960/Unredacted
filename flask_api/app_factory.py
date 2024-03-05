from handler import EndpointHandler


class FlaskAppWrapper:
    """
    Initializes a flask app with the given config parameters
    app: Flask app object
    """

    # configs is a variable length dict (keyword args)
    def __init__(self, app, **configs):
        """
        Initializes a Flask app with the given configuration.
        app: Flask app object
        configs: keyword args for Flask configuration
        """
        self.app = app
        self.configs(**configs)

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    # adds endpoint to the Flask app
    def add_endpoint(
        self,
        endpoint=None,
        endpoint_name=None,
        handler=None,
        methods=["GET"],
        *args,
        **kwargs
    ):
        self.app.add_url_rule(
            endpoint,
            endpoint_name,
            EndpointHandler(handler),
            methods=methods,
            *args,
            **kwargs
        )

    def run(self, **kwargs):
        self.app.run(**kwargs)
