from django import template

register = template.Library()

@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def custom_submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    request = context['request']
    no_save_and_another = context['has_add_permission'] and not is_popup and (not save_as or context['add'])
    if 'no_save_and_another' in context:
        no_save_and_another = False
    akses_spesial = request.user.is_superuser or 'Admin Sistem' in request.user.group_names
    if 'akses_spesial' in context:
        akses_spesial = akses_spesial or context['akses_spesial']

    show_save = context['has_change_permission'] or context['has_add_permission']
    if 'no_show_save' in context:
        show_save = False
    ctx = {
        'opts': opts,
        'show_delete_link': not is_popup and context['has_delete_permission'] and change and context.get('show_delete', True),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another':  no_save_and_another,
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': show_save,
        'request': request,
        'akses_spesial': akses_spesial,
        'preserved_filters': context.get('preserved_filters'),
    }
    if context.get('original') is not None:
        ctx['original'] = context['original']
    return ctx