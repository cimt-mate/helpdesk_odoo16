from odoo import models, fields, api
from odoo.exceptions import UserError
import datetime

class HelpdeskTicket(models.Model):
    _name = 'cimt_helpdesk.ticket'
    _description = 'Helpdesk Ticket'
    _order = 'ticket_date desc'

    cim_field = fields.Char(string='CIM Field')

    customer_id = fields.Many2one(
        'res.partner', 
        string='Customer', 
        domain=[('is_client', '=', True)], 
        required=True,
        help="Select a customer from the list of partners who are marked as customers."
    )
    # Get the current user's login name as the default value for user_name
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, readonly=True)
    # Free text input field with the current user's name as the default value
    user_name = fields.Char(
        string='User Name', 
        default=lambda self: self._default_user_name()
    )
    customer_nickname = fields.Char(
        string='Nickname', 
        related='customer_id.nickname',
        readonly=True,
        store=True,  # Set to True if you need to store it in the database, otherwise you can omit this or set it to False
        help="Displays the nickname of the selected customer."
    )
    
    ticket_date = fields.Date(
        'Ticker Date', 
        required=True, 
        default=fields.Date.context_today
    )
    worker_name = fields.Char(string='Contact Name')
    ticket_minutes = fields.Integer('Ticket Minutes')
    ticket_detail = fields.Text('Ticket Detail')
    company_id = fields.Many2one('res.company', string='Company', 
        default=lambda self: self.env.company)
    
    @api.model
    def _default_user_name(self):
        # Return the current user's login name
        return self.env.user.name
    
    def action_print_tickets(self):
        context = dict(self.env.context or {})
        active_ids = context.get('active_ids', [])
        
        if not active_ids:
            raise UserError(_("No tickets to print."))

        tickets = self.env['cimt_helpdesk.ticket'].browse(active_ids)

        # Example of custom file name: "Helpdesk_Tickets_YYYY-MM-DD"
        report_name = f"Helpdesk_Tickets_{datetime.datetime.now().strftime('%Y-%m-%d')}"

        
        return {
            'type': 'ir.actions.act_url',
            'url': '/report/pdf/helpdesk_odoo16.action_report_helpdesk_tickets/%s?download=true' % ','.join(map(str, active_ids)),
            'target': 'new',
            'print_report_name': report_name,
        }