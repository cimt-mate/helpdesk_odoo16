from odoo import models, fields, api

class MonthlyReport(models.Model):
    _name = 'monthly.report'
    _description = 'Monthly Report'

    customer_id = fields.Many2one(
        'res.partner', 
        string='Customer', 
        domain=[('is_customer', '=', True)], 
        required=True,
    )
    user_id = fields.Many2one('res.users', string='Worker', default=lambda self: self.env.user, readonly=True)
    location = fields.Char(string='Location')
    monthly_start_date = fields.Date(string='Monthly Start Date', required=True, default=fields.Date.context_today)
    monthly_end_date = fields.Date(string='Monthly End Date', required=True)
    monthly_start_time = fields.Float(string='Start time')
    monthly_end_time = fields.Float(string='End time')

    # monthly_end = fields.Datetime(string='Monthly End Date', required=True, default=fields.Date.context_today) 
    drive_c_free_size = fields.Float(string='Drive C Free')
    drive_c_free_type = fields.Selection([('GB', 'GB'), ('TB', 'TB')], string='C Type')
    drive_c_total_size = fields.Float(string='Drive C Total')
    drive_c_total_type = fields.Selection([('GB', 'GB'), ('TB', 'TB')], string='C Type')
    drive_d_free_size = fields.Float(string='Drive D Free')
    drive_d_free_type = fields.Selection([('GB', 'GB'), ('TB', 'TB')], string='D Type')
    drive_d_total_size = fields.Float(string='Drive D Total')
    drive_d_total_type = fields.Selection([('GB', 'GB'), ('TB', 'TB')], string='D Type')
    drive_special_free_size = fields.Float(string='Drive Special Free')
    drive_special_free_type = fields.Selection([('GB', 'GB'), ('TB', 'TB')], string='Special Type')
    drive_special_total_size = fields.Float(string='Drive Special Total')
    drive_special_total_type = fields.Selection([('GB', 'GB'), ('TB', 'TB')], string='Special Type')

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
    doctor_data_type = fields.Selection([('MB', 'MB')], string='Unit')
    doctor_basic_free = fields.Float(string='Doctor Basic Free', required=True)
    doctor_basic_total = fields.Float(string='Doctor Basic Total', required=True)
    doctor_basic_type = fields.Selection([('MB', 'MB')], string='Unit')


    charge = fields.Boolean(string='Charge')
    complete = fields.Boolean(string='Complete')    
    
    work_result = fields.Text(string='Work Result')
    remark = fields.Text(string='Remark')
    
    
    
    @api.onchange('monthly_start_date')
    def _onchange_monthly_start_date(self):
        self.monthly_end_date = self.monthly_start_date