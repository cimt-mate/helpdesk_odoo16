from odoo import models, fields, api

class HelpdeskResPartnerInfo(models.Model):
    _name = 'helpdesk.res.partner.info'
    _description = 'Additional Info for Partners'

   # Many2one relationship to res.partner
    partner_id = fields.Many2one('res.partner', string="Partner", required=True, domain=[('is_client', '=', True)])

    # Related fields to access res.partner data
    partner_name = fields.Char(related='partner_id.name', string="Customer Name", readonly=True)
    partner_street = fields.Char(related='partner_id.street', string="Street", readonly=True)
    partner_nickname = fields.Char(related='partner_id.nickname', string="Nick Name", readonly=True)
    # partner_trader = fields.Char(related='partner_id.trader_selection', string="Trader", readonly=True)
    

    # Your new fields
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
    max_contract_end_date = fields.Date(string='Contract End Date', compute='_compute_max_contract_end_date')

    @api.depends('partner_id.sale_order_ids.contract_end_date')
    def _compute_max_contract_end_date(self):
        for record in self:
            # Filter out False values which represent empty dates in Odoo
            related_enddates = filter(None, record.partner_id.sale_order_ids.mapped('contract_end_date'))
            record.max_contract_end_date = max(related_enddates) if related_enddates else False