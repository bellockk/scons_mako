import os,sys
from SCons.Script import *
from SCons.Errors import StopError

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def _string(target, source, env):
    return 'Mako(%s, %s)' % (target[0], source[0])


    from mako.template import Template

    try:
        template_object = Template(filename=source[0].abspath)
    except:
        raise StopError(SCons.Warnings.Warning,
                                     "Could not load the mako "
                                     "template %s." % source[0].abspath)

    try:
        rendered = template_object.render(**env['MAKO_DICTIONARY'])
    except:
        raise StopError(SCons.Warnings.Warning,
                                     "Could not render the template %s with "
                                     "the following dictionary.\n%s"
                                     "" % (source[0].abspath,
                                           env['MAKO_DICTIONARY']))

    try:
        file_object = open(target[0].abspath, 'w')
        file_object.write(rendered)
        file_object.close()
    except:
        raise StopError(SCons.Warnings.Warning,
                                     "Could not write the rendered template "
                                     "to %s." % target[0].abspath)

def _action(target, source, env):

    from mako.template import Template
    from mako import exceptions

    try:
        template_object = Template(filename=source[0].abspath)
    except:
        print exceptions.text_error_template().render()
        raise SCons.Errors.StopError(SCons.Warnings.Warning, "Because of the above error, could not load the mako template %s. Because of the previous error." % source[0].abspath)

    try:
        rendered = template_object.render(**env['MAKO_DICTIONARY'])
    except:
        print exceptions.text_error_template().render()
        raise SCons.Errors.StopError(SCons.Warnings.Warning, "Because of the above error, could not render the template %s with the following dictionary.\n%s" % (source[0].abspath, env['MAKO_DICTIONARY']))

    try:
        file_object = open(target[0].abspath, 'w')
        file_object.write(rendered)
        file_object.close()
    except:
        raise SCons.Errors.StopError(SCons.Warnings.Warning, "Could not write the rendered template to %s." % target[0].abspath)

def generate(env):
    """
    Add builders and construction variables for the Mako builder.
    """


    scons_action=SCons.Action.Action(_action, _string)
    env['BUILDERS']['Mako'] =  Builder(
            action = scons_action,
            target_factory = env.fs.File
    )

    env.AppendUnique(
        MAKO_DICTIONARY = {}
    )

def exists(env):
    """
    Make sure this tool exists.
    """
    try:
        sys.path.insert(0, os.path.abspath(
            os.path.join(SCRIPT_PATH, '..', '..', '..', '..', 'Mako')))
        import os
        from mako.template import Template
    except ImportError:
        raise StopError(SCons.Warnings.Warning,
                                     "Could not find mako, please ensure you "
                                     "have it installed on your system.")
    else:
        return True
