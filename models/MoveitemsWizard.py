from odoo import models, fields, api
from odoo.exceptions import UserError

class MoveItemsWizard(models.TransientModel):
    _name = 'iscapop_app.move_items_wizard'
    _description = 'Wizard to move items to another location'

    source_location_id = fields.Many2one('iscapop_app.location_model', string='Source Location', required=True)
    target_location_id = fields.Many2one('iscapop_app.location_model', string='Target Location', required=True)
    item_detail_id = fields.Many2one('iscapop_app.item_detail_model', string='Item', required=True, domain="[('location_id', '=', source_location_id)]")
    quantity = fields.Integer(string='Quantity', required=True, default=1)

    @api.onchange('source_location_id')
    def _onchange_source_location_id(self):
        if self.source_location_id:
            item_details = self.env['iscapop_app.item_detail_model'].search([('location_id', '=', self.source_location_id.id)])
            item_ids = [detail.item_id.id for detail in item_details]
            location_type = self.source_location_id.location_type

            if location_type == 'class':
                return {
                    'domain': {
                        'item_detail_id': [('id', 'in', item_ids)],
                        'target_location_id': [('location_type', '=', 'warehouse')]
                    }
                }
            elif location_type == 'warehouse':
                return {
                    'domain': {
                        'item_detail_id': [('id', 'in', item_ids)],
                        'target_location_id': [('id', '!=', self.source_location_id.id)]
                    }
                }

    def move_items(self):
        self.ensure_one()
        source_item_detail = self.item_detail_id
        if source_item_detail.stock >= self.quantity:
            source_item_detail.stock -= self.quantity
            target_item_detail = self.env['iscapop_app.item_detail_model'].search([
                ('item_id', '=', self.item_detail_id.item_id.id),
                ('location_id', '=', self.target_location_id.id)
            ], limit=1)
            if target_item_detail:
                target_item_detail.stock += self.quantity
            else:
                self.env['iscapop_app.item_detail_model'].create({
                    'item_id': self.item_detail_id.item_id.id,
                    'location_id': self.target_location_id.id,
                    'stock': self.quantity,
                    'state': self.item_detail_id.state
                })

            if source_item_detail.stock <= 0:
                source_item_detail.active = False
        else:
            raise UserError('Not enough stock in the source location.')
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def default_get(self, fields):
        res = super(MoveItemsWizard, self).default_get(fields)
        if 'source_location_id' in self.env.context:
            res['source_location_id'] = self.env.context['source_location_id']
        return res
