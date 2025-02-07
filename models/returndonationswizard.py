from odoo import models, fields, api
from odoo.exceptions import UserError

class ReturnToWarehouseWizard(models.TransientModel):
    _name = 'iscapop_app.return_to_warehouse_wizard'
    _description = 'Wizard to return items to warehouse'

    donation_id = fields.Many2one('iscapop_app.donation_model', string='Donation', required=True)
    target_warehouse_id = fields.Many2one('iscapop_app.location_model', string='Target Warehouse', required=True, domain="[('location_type', '=', 'warehouse')]")
    quantity = fields.Integer(string='Quantity', required=True, default=1)

    def return_items_to_warehouse(self):
        self.ensure_one()
        donation = self.donation_id
        if donation.quantity >= self.quantity:
            donation.quantity -= self.quantity
            target_item_detail = self.env['iscapop_app.item_detail_model'].search([
                ('item_id', '=', donation.item_id.id),
                ('location_id', '=', self.target_warehouse_id.id),
                ('state', '=', donation.state)
            ], limit=1)
            if target_item_detail:
                target_item_detail.stock += self.quantity
            else:
                self.env['iscapop_app.item_detail_model'].create({
                    'item_id': donation.item_id.id, 
                    'location_id': self.target_warehouse_id.id,
                    'stock': self.quantity,
                    'state': donation.state
                })
            if donation.quantity <= 0:
                donation.unlink()
        else:
            raise UserError('Not enough quantity in the donation.')
        return {'type': 'ir.actions.act_window_close'}

