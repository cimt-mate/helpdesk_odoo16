from odoo import models, fields, api

class HelpdeskResPartner(models.Model):
    _inherit = 'res.partner'

    # # New field
    remark = fields.Text(string="Remark")
    server_name = fields.Char(string="Server Name")
    os_name = fields.Char(string="OS Name")
    ip = fields.Char(string="IP")
    domain = fields.Char(string="Domain")
    user_login = fields.Char(string="Login User")
    password = fields.Char(string="Password")
    oracle_version = fields.Char(string="Oracle Version")
    oracle_path = fields.Char(string="Oracle Path")
    backup_path = fields.Char(string="Backup Path")
    backup_out_path = fields.Char(string="Backup Outside Path") 
    oracle_language = fields.Char(string="Oracle Language")
    doctor_data_name = fields.Char(string="Doctor Data Name")
    doctor_basic_name = fields.Char(string="Doctor Basic Name")
    license_info = fields.Text(string="License Info")
    license_expired_date = fields.Date(string="License Expired Date")
    # Get Max Contract End Date From Sales Order
    max_contract_end_date = fields.Date(
        string='Contract End Date',
        compute='_compute_max_contract_end_date',
        store=True,  # Storing the value is optional depending on your needs
    )

    @api.depends('sale_order_ids.contract_end_date')  # Assuming sale_order_ids is the reverse one2many relation
    def _compute_max_contract_end_date(self):  # Make sure this matches the name in the field definition
        for partner in self:
            related_enddates = partner.sale_order_ids.mapped('contract_end_date')
            dates = [date for date in related_enddates if isinstance(date, fields.Date)]
            partner.max_contract_end_date = max(dates) if dates else False