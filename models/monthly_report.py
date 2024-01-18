from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime
from odoo.tools.translate import _


class MonthlyReport(models.Model):
    _name = 'monthly.report'
    _description = 'Monthly Report'
    _order = 'monthly_start_date desc'

    customer_id = fields.Many2one(
        'res.partner', 
        string='Customer', 
        domain=[('is_client', '=', True)], 
        required=True,
    )

    customer_nickname = fields.Char(
        string='Nickname', 
        related='customer_id.nickname',
        readonly=True,
        store=True,  # Set to True if you need to store it in the database, otherwise you can omit this or set it to False
        help="Displays the nickname of the selected customer."
    )
    company_id = fields.Many2one('res.company', string='Company', 
        default=lambda self: self.env.company)

    # Get the current user's login name as the default value for user_name
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, readonly=True)
    # Free text input field with the current user's name as the default value
    user_name = fields.Char(
        string='User Name', 
        default=lambda self: self._default_user_name()
    )
    location = fields.Char(string='Location')
    monthly_start_date = fields.Date(string='Monthly Start Date', required=True, default=fields.Date.context_today)
    monthly_end_date = fields.Date(string='Monthly End Date', required=True)
    monthly_start_time = fields.Float(string='Start time')
    monthly_end_time = fields.Float(string='End time')
    time_difference = fields.Float(string='Time Difference', compute='_compute_time_difference', store=True)


    # monthly_end = fields.Datetime(string='Monthly End Date', required=True, default=fields.Date.context_today) 
    drive_c_free_size = fields.Float(string='Drive C Free')
    drive_c_free_type = fields.Selection([('MB', 'MB'),('GB', 'GB'), ('TB', 'TB')], string='C Type')
    drive_c_total_size = fields.Float(string='Drive C Total')
    drive_c_total_type = fields.Selection([('MB', 'MB'),('GB', 'GB'), ('TB', 'TB')], string='C Type')
    drive_d_free_size = fields.Float(string='Drive D Free')
    drive_d_free_type = fields.Selection([('MB', 'MB'),('GB', 'GB'), ('TB', 'TB')], string='D Type')
    drive_d_total_size = fields.Float(string='Drive D Total')
    drive_d_total_type = fields.Selection([('MB', 'MB'),('GB', 'GB'), ('TB', 'TB')], string='D Type')
    drive_special_name = fields.Char(string='Drive S Name', size=1)
    drive_special_free_size = fields.Float(string='Drive S Free')
    drive_special_total_size = fields.Float(string='Drive S Total')
    drive_special_free_type = fields.Selection([('MB', 'MB'),('GB', 'GB'), ('TB', 'TB')], string='S Type')    
    drive_special_total_type = fields.Selection([('MB', 'MB'),('GB', 'GB'), ('TB', 'TB')], string='S Type')

    server_backup = fields.Selection([('OK', 'OK'), ('NG', 'NG'), ('NO', 'NO'), ('UNKNOWN', 'UNKNOWN')], string='Backup Type')
    outside_backup = fields.Selection([('OK', 'OK'), ('NG', 'NG'), ('NO', 'NO'), ('UNKNOWN', 'UNKNOWN')], string='Outside Backup Type')
    data_size = fields.Float(string='Data Size')
    data_type = fields.Selection([('KB', 'KB'), ('MB', 'MB'), ('GB', 'GB'), ('TB', 'TB')], string='Data Unit')
    basic_size = fields.Float(string='Basic Size')
    basic_type = fields.Selection([('KB', 'KB'), ('MB', 'MB'), ('GB', 'GB'), ('TB', 'TB')], string='Basic Unit')
    evolio_size = fields.Float(string='EVOLIO Size')
    evolio_type = fields.Selection([('KB', 'KB'), ('MB', 'MB'), ('GB', 'GB'), ('TB', 'TB')], string='Evolio Unit')    
    oracle_log = fields.Char(string='Oracle Log')
    
    doctor_data_free = fields.Float(string='Doctor Data Free', required=True)
    doctor_data_total = fields.Float(string='Doctor Data Total', required=True)
    doctor_data_type = fields.Selection([('KB', 'KB'),('MB', 'MB'), ('GB', 'GB')], string='Unit')
    doctor_basic_free = fields.Float(string='Doctor Basic Free', required=True)
    doctor_basic_total = fields.Float(string='Doctor Basic Total', required=True)
    doctor_basic_type = fields.Selection([('KB', 'KB'),('MB', 'MB'), ('GB', 'GB')], string='Unit')


    charge = fields.Boolean(string='Charge')
    complete = fields.Boolean(string='Complete')    
    
    work_result = fields.Text(string='Work Result')
    remark = fields.Text(string='Remark')

    truncated_customer_id = fields.Char(compute='_compute_truncated_fields')
    truncated_location = fields.Char(compute='_compute_truncated_fields')

    @api.depends('customer_id', 'location')
    def _compute_truncated_fields(self):
        max_length = 23
        for record in self:
            # Truncate customer_id
            if record.customer_id and len(record.customer_id.name) > max_length:
                record.truncated_customer_id = record.customer_id.name[:max_length] + '...'
            else:
                record.truncated_customer_id = record.customer_id.name if record.customer_id else ''

            # Truncate location
            if record.location and len(record.location) > max_length:
                record.truncated_location = record.location[:max_length] + '...'
            else:
                record.truncated_location = record.location

    @api.onchange('monthly_start_date')
    def _onchange_monthly_start_date(self):
        self.monthly_end_date = self.monthly_start_date


    @api.depends('monthly_start_time', 'monthly_end_time')
    def _compute_time_difference(self):
        for record in self:
            if record.monthly_start_time and record.monthly_end_time:
                # Calculate the time difference in hours
                record.time_difference = record.monthly_end_time - record.monthly_start_time
            else:
                record.time_difference = 0.0

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
    
    @api.onchange('drive_c_free_type')
    def _onchange_drive_c_free_type(self):
        self.drive_c_total_type = self.drive_c_free_type

    @api.onchange('drive_d_free_type')
    def _onchange_drive_d_free_type(self):
        self.drive_d_total_type = self.drive_d_free_type

    @api.onchange('drive_special_free_type')
    def _onchange_drive_special_free_type(self):
        self.drive_special_total_type = self.drive_special_free_type


    def action_duplicate_recordd(self):
        self.ensure_one()
        # Define the fields you want to copy and their values
        default_vals = {
            'customer_id': self.customer_id.id,
            'customer_nickname': self.customer_nickname,
            'user_name': self.user_name,
            'drive_c_free_type': self.drive_c_free_type,
            'drive_c_total_size': self.drive_c_total_size,
            'drive_c_total_type': self.drive_c_total_type,
            'drive_d_free_type': self.drive_d_free_type,
            'drive_d_total_size': self.drive_d_total_size,
            'drive_d_total_type': self.drive_d_total_type,
            'drive_special_name': self.drive_special_name,
            'drive_special_total_size': self.drive_special_total_size,
            'drive_special_total_type': self.drive_special_total_type,
            'doctor_data_total': self.doctor_data_total,
            'doctor_data_type': self.doctor_data_type,
            'doctor_basic_total': self.doctor_basic_total,
            'doctor_basic_type': self.doctor_basic_type,
            'data_type': self.data_type,
            'basic_type': self.basic_type,
            'evolio_type': self.evolio_type,
            'location': self.location,
            # Set other fields to False or their default value if you want to reset them
            # Clear specified fields
            'charge': False,
            'complete': False,
            'work_result': False,
            'remark': False,
            'doctor_basic_free': False,
            'doctor_data_free': False,
            'oracle_log': False,
            'data_size': False,
            'basic_size': False,
            'evolio_size': False,
            'outside_backup': False,
            'server_backup': False,
            'drive_special_free_size': False,
            'drive_d_free_size': False,
            'drive_c_free_size': False,
            'monthly_end_time': False,
            'monthly_start_time': False,
            'monthly_end_date':  fields.Date.context_today(self),
            'monthly_start_date': fields.Date.context_today(self),
        }
        # Duplicate the record with the specified default values
        new_context = self.env.context.copy()
        new_context.update({'default_' + field: value for field, value in default_vals.items()})

        # Return an action to open a new form view in 'edit' mode with the default values
        return {
            'name': _('Duplicate Monthly Report'),
            'type': 'ir.actions.act_window',
            'res_model': 'monthly.report',
            'views': [(False, 'form')],
            'target': 'new',
            'context': new_context,
        }
