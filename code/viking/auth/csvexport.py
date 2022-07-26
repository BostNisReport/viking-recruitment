from django.core.exceptions import PermissionDenied
from django.http import StreamingHttpResponse
from django.utils import timezone
from django.utils.text import capfirst, force_text
from django.contrib.admin.util import label_for_field, lookup_field
from functools import update_wrapper
import csv


class Echo(object):
    def write(self, value):
        return value


class CSVExportMixin(object):
    csvexport_fields = ('__all__',)
    export_queryset = None

    def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^csvexport/$',
                wrap(self.csvexport_view),
                name='%s_%s_csvexport' % info),
        ]
        urlpatterns += super(CSVExportMixin, self).get_urls()
        return urlpatterns

    def get_export_queryset(self, request):
        if self.export_queryset is not None:
            return self.export_queryset.all()
        else:
            return self.queryset(request)

    def csvexport_data(self, request):
        writer = csv.writer(Echo())
        csvexport_fields = []

        for field_name in self.csvexport_fields:
            if field_name == '__all__':
                csvexport_fields.extend([x.name for x in self.model._meta.fields])
            else:
                csvexport_fields.append(field_name)

        # CSV header
        yield writer.writerow([capfirst(force_text(label_for_field(
            x, self.model, model_admin=self))) for x in csvexport_fields])

        # CSV data
        for result in self.get_export_queryset(request).iterator():
            csv_row = []

            for field_name in csvexport_fields:
                f, attr, value = lookup_field(field_name, result, self)
                csv_row.append(unicode(value).encode('utf-8'))

            yield writer.writerow(csv_row)

    def csvexport_view(self, request):
        if not self.has_add_permission(request):
            raise PermissionDenied

        response = StreamingHttpResponse(self.csvexport_data(request), content_type='text/csv')
        file_name = capfirst(unicode(self.model._meta.verbose_name_plural))
        file_date = timezone.now().strftime('%Y-%m-%d %H%M')
        response['Content-Disposition'] = 'attachment; filename="%s %s.csv"' % (
            file_name, file_date)

        return response
