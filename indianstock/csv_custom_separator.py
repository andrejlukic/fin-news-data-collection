import csv
import os
from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter

class QuoteAllDialect(csv.excel):
    quoting = csv.QUOTE_ALL

class CsvOptionRespectingItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        if(os.fstat(args[0].fileno()).st_size > 0):
            kwargs['include_headers_line'] = False	
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter
        kwargs.update({'dialect': QuoteAllDialect})
        super(CsvOptionRespectingItemExporter, self).__init__(*args, **kwargs)
