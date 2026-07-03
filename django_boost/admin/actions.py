from __future__ import annotations

from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import model_ngettext
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _, gettext_lazy


def hard_delete_selected(modeladmin, request, queryset):

    opts = modeladmin.model._meta
    app_label = opts.app_label

    # Populate deletable_objects, a data structure of all related objects that
    # will also be deleted.
    deletable_objects, model_count, perms_needed, protected = modeladmin.get_deleted_objects(queryset, request)

    # The user has already confirmed the deletion.
    # Do the deletion and return None to display the change list view again.
    if request.POST.get('post') and not protected:
        if perms_needed:
            raise PermissionDenied
        n = queryset.count()
        if n:
            # log_deletions() replaced the per-object log_deletion() in Django
            # 5.1 (log_deletion() is deprecated); prefer it when available,
            # falling back on Django 4.2/5.0.
            if hasattr(modeladmin, 'log_deletions'):
                modeladmin.log_deletions(request, queryset)
            else:
                for obj in queryset:
                    modeladmin.log_deletion(request, obj, str(obj))
            modeladmin.hard_delete_queryset(request, queryset)
            modeladmin.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(modeladmin.opts, n)
            }, messages.SUCCESS)
        # Return None to display the change list page again.
        return None

    objects_name = model_ngettext(queryset)

    if perms_needed or protected:
        title = _("Cannot delete %(name)s") % {"name": objects_name}
    else:
        title = _("Are you sure?")

    context = {
        **modeladmin.admin_site.each_context(request),
        'title': title,
        'objects_name': str(objects_name),
        'deletable_objects': [deletable_objects],
        'model_count': dict(model_count).items(),
        'queryset': queryset,
        'perms_lacking': perms_needed,
        'protected': protected,
        'opts': opts,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        'media': modeladmin.media,
        'action_name': 'hard_delete_selected',
    }

    request.current_app = modeladmin.admin_site.name

    # Display the confirmation page
    return TemplateResponse(request, modeladmin.delete_selected_confirmation_template or [
        "boost/admin/%s/%s/hard_delete_selected_confirmation.html" % (app_label, opts.model_name),
        "boost/admin/%s/hard_delete_selected_confirmation.html" % app_label,
        "boost/admin/hard_delete_selected_confirmation.html"
    ], context)


hard_delete_selected.allowed_permissions = ('delete',)
hard_delete_selected.short_description = gettext_lazy("Hard delete selected %(verbose_name_plural)s")
