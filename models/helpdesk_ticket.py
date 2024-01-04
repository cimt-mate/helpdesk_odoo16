from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    _name = 'cimt_helpdesk.ticket'
    _description = 'Helpdesk Ticket'

    customer_id = fields.Many2one(
        'res.partner', 
        string='Customer', 
        domain=[('is_customer', '=', True)], 
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
    
    ticket_date = fields.Date(
        'Ticker Date', 
        required=True, 
        default=fields.Date.context_today
    )
    worker_name = fields.Char(string='Contact Name')
    ticket_minutes = fields.Integer('Ticket Minutes')
    ticket_detail = fields.Text('Ticket Detail')
    
    @api.model
    def _default_user_name(self):
        # Return the current user's login name
        return self.env.user.name