from odoo import models, fields, api
from odoo.exceptions import UserError
import datetime

class MonthlyReport(models.Model):
    _name = 'monthly.report'
    _description = 'Monthly Report'

    name = fields.Char('Report Name', required=True)
    report_date = fields.Date('Report Date')
    note = fields.Text('Description')
    # Add other fields as needed

    @api.model
    def _default_user_name(self):
        # Return the current user's login name
        return self.env.user.name
    

    def action_print_report(self):
        if not self:
            raise UserError("No records selected for printing.")

        # Collect the IDs of all selected records
        record_ids = self.ids

        # Generate the report for the entire recordset
        return self.env.ref('monthly.action_report_monthly_report').report_action(record_ids)