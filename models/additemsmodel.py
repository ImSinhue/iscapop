from odoo import models, fields, api
from odoo.exceptions import UserError

class AddItemsWizard(models.TransientModel):
    _name = 'iscapop_app.add_items_wizard'
    _description = 'Wizard to add items to a location'

    location_id = fields.Many2one('iscapop_app.location_model', string='Location', required=True)
    item_id = fields.Many2one('iscapop_app.item_model', string='Item', required=True)
    quantity = fields.Integer(string='Quantity', required=True, default=1)
    state = fields.Selection([
        ('new', 'New'),
        ('good', 'Good'),
        ('bad', 'Bad'),
    ], string='State', required=True)

    def add_items_to_location(self):
        self.ensure_one()
        existing_item_detail = self.env['iscapop_app.item_detail_model'].search([
            ('item_id', '=', self.item_id.id),
            ('location_id', '=', self.location_id.id),
            ('state', '=', self.state)
        ], limit=1)
        if existing_item_detail:
            existing_item_detail.stock += self.quantity
        else:
            self.env['iscapop_app.item_detail_model'].create({
                'item_id': self.item_id.id,
                'location_id': self.location_id.id,
                'stock': self.quantity,
                'state': self.state
            })
        return {'type': 'ir.actions.act_window_close'}
