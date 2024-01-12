from odoo import models, fields

class MonthlyReport(models.Model):
    _name = 'monthly.report'
    _description = 'Monthly Report'

    name = fields.Char('Report Name', required=True)
    report_date = fields.Date('Report Date')
    note = fields.Text('Description')
    # Add other fields as needed
