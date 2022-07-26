from django.http import HttpResponse
import unicodecsv


def export_csv(request, report_name, fields, queryset, field_order=None, start_date=None, end_date=None):
    if start_date and end_date:
        filename = '%s - %s to %s' % (report_name, start_date, end_date)
    else:
        filename = report_name

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (filename,)
    csv = unicodecsv.writer(response, encoding='utf-8')
    csv.writerow(fields)

    for row in queryset:
        if field_order is None:
            csv.writerow([x for x in row.itervalues()])
        else:
            csv.writerow([row[x] for x in field_order])

    return response
