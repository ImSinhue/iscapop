from odoo import models, fields, api
from odoo.exceptions import UserError

class MoveToDonationWizard(models.TransientModel):
    _name = 'iscapop_app.move_to_donation_wizard'
    _description = 'Wizard to move items to donation'

    source_location_id = fields.Many2one('iscapop_app.location_model', string='Source Location', required=True)
    item_detail_id = fields.Many2one('iscapop_app.item_detail_model', string='Item', required=True, domain="[('location_id', '=', source_location_id)]")
    quantity = fields.Integer(string='Quantity', required=True, default=1)

    def move_items_to_donation(self):
        self.ensure_one()
        source_item_detail = self.item_detail_id
        if source_item_detail.stock >= self.quantity:
            source_item_detail.stock -= self.quantity
            
            # Eliminar la lógica de búsqueda de donaciones existentes
            self.env['iscapop_app.donation_model'].create({
                'name': source_item_detail.item_id.name,
                'description': source_item_detail.item_id.description,
                'photo': source_item_detail.item_id.photo,
                'state': source_item_detail.state,
                'documentation': source_item_detail.item_id.documentation,
                'quantity': self.quantity,
                'item_id': source_item_detail.item_id.id,
                'donated_by': self.env.user.id
            })
            
            if source_item_detail.stock <= 0:
                source_item_detail.active = False
        else:
            raise UserError('Not enough stock in the source location.')
        return {'type': 'ir.actions.act_window_close'}

