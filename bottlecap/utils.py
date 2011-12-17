
import os

_here = os.path.dirname(__file__)
_microtemplates = os.path.join(_here, 'microtemplates')


def get_microtemplates(names=None):

    templates = {}

    all_filenames = {}
    for _fn in os.listdir(_microtemplates):
        if _fn.endswith('.mustache'):
            name = _fn[:-9]
            fname = os.path.join(_microtemplates, _fn)
            all_filenames[name] = fname

    # XXX Names can be a list of templates that the page needs.
    # For now on, we ignore names and include all the templates we have.
    names = all_filenames.keys()

    for name in names:
        #try:
        fname = all_filenames[name]
        #except KeyError:
        #    raise "No such microtemplate %s" % name
        templates[name] = file(fname).read()

    return templates
    

