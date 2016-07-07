from datetime import datetime
from StringIO import StringIO
import csv

from flask import Response


def csv_value(v):
    if v is None:
        return v
    if isinstance(v, datetime):
        return v.isoformat()
    return unicode(v).encode('utf-8')


def csvify(iterable, status=200, headers=None):
    rows = filter(lambda r: r is not None, [r.to_row() for r in iterable])
    keys = set()
    for row in rows:
        keys = keys.union(row.keys())
    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerow([k.encode('utf-8') for k in keys])
    for row in rows:
        writer.writerow([csv_value(row.get(k, '')) for k in keys])
    return Response(buf.getvalue(), headers=headers,
                    status=status, mimetype='text/csv')


def dataset_filename(dataset, format):
    ts = datetime.utcnow().strftime('%Y%m%d')
    return '%s-%s.%s' % (dataset.name, ts, format)
