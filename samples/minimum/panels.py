from bottlecap.panel import panel_config


@panel_config(name="sample.test_panel")
def test_panel(context, request):
    return "<div>Hi, I'm a test panel!</div>"

