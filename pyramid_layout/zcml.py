from pyramid.config import Configurator

from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.schema import TextLine


class IPanelDirective(Interface):
    context = GlobalObject(
        title=u"The interface or class this panel is for.",
        required=False
        )

    panel = GlobalObject(
        title=u"",
        description=u"The panel function",
        required=False,
        )

    name = TextLine(
        title=u"The name of the panel",
        description=u'',
        required=False,
        )

    attr = TextLine(
        title=u'The callable attribute of the panel object'
              u'(default is __call__)',
        description=u'',
        required=False)

    renderer = TextLine(
        title=u'The renderer asssociated with the panel',
        description=u'',
        required=False)


def panel(config_context, context=None, panel=None, name="", attr=None,
          renderer=None):
    config = Configurator.with_context(config_context)
    config.add_panel(
        context=context, panel=panel, name=name,
        attr=attr, renderer=renderer)


class ILayoutDirective(Interface):
    context = GlobalObject(
        title=u"The interface or class this layout is for.",
        required=False
        )

    layout = GlobalObject(
        title=u"",
        description=u"The layout class",
        required=False,
        )

    name = TextLine(
        title=u"The name of the layout",
        description=u'',
        required=False,
        )

    template = TextLine(
        title=u'The renderer asssociated with the layout',
        description=u'',
        required=True)

    containment = GlobalObject(
        title = u'Dotted name of a containment class or interface',
        required=False)


def layout(config_context, context=None, layout=None, name="", containment=None,
           template=None):
    config = Configurator.with_context(config_context)
    config.add_layout(
        context=context, layout=layout, name=name, containment=containment,
        template=template)
