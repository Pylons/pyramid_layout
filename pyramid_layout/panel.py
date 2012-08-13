import venusian


class panel_config(object):
    """ A function, class or method decorator which allows a
    developer to create panel registrations.

    For example, this code in a module ``panels.py``::

      from resources import MyResource

      @panel_config(name='my_panel', context=MyResource):
      def my_panel(context, request):
          return 'OK'

    The following arguments are supported as arguments to
    :class:`pyramid_layout.panel.panel_config`: ``context``, ``name``,
    ``renderer``, ``attr``.

    The meanings of these arguments are the same as the arguments passed to
    :meth:`pyramid_layout.config.add_panel`.
    """
    def __init__(self, name='', context=None, renderer=None, attr=None):
        self.name = name
        self.context = context
        self.renderer = renderer
        self.attr = attr

    def __call__(self, wrapped):
        settings = self.__dict__.copy()

        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_panel(panel=ob, **settings)

        info = venusian.attach(wrapped, callback, category='pyramid_layout')

        if info.scope == 'class':
            # if the decorator was attached to a method in a class, or
            # otherwise executed at class scope, we need to set an
            # 'attr' into the settings if one isn't already in there
            if settings['attr'] is None:
                settings['attr'] = wrapped.__name__

        settings['_info'] = info.codeinfo # fbo "action_method"
        return wrapped
