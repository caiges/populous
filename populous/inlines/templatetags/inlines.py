from django import template
from populous.inlines.markup import xml_to_xhtml

register = template.Library()

def do_inline_markup(parser, token):
    """
    
    {% inline_markup obj.field %}
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % bits[0]
    try:
        obj, field = bits[1].split(".")
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument of the form: obj.field" % bits[0]
    return InlineMarkupNode(obj, field)


class InlineMarkupNode(template.Node):
    def __init__(self, obj, field):
        self.obj = obj
        self.field = field
    
    def render(self, context):
        obj = template.Variable(self.obj).resolve(context)
        field = obj._meta.get_field(self.field)
        data = getattr(obj, self.field)
        return xml_to_xhtml(data, context.get('request'), obj, field)

register.tag('inline_markup', do_inline_markup)