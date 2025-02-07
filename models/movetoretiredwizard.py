from odoo import models, fields, api
from odoo.exceptions import UserError

class MoveItemsToRetiredWizard(models.TransientModel):
    _name = 'iscapop_app.move_items_to_retired_wizard'
    _description = 'Wizard to move bad items to retired location'

    source_location_id = fields.Many2one('iscapop_app.location_model', string='Source Location', required=True, domain="[('location_type', 'in', ['warehouse', 'class'])]")
    target_location_id = fields.Many2one('iscapop_app.location_model', string='Retired Location', required=True, domain="[('location_type', '=', 'retired')]")
    item_detail_id = fields.Many2one('iscapop_app.item_detail_model', string='Item', required=True, domain="[('location_id', '=', source_location_id), ('state', '=', 'bad')]")
    quantity = fields.Integer(string='Quantity', required=True, default=1)

    @api.onchange('source_location_id')
    def _onchange_source_location_id(self):
        if self.source_location_id:
            item_details = self.env['iscapop_app.item_detail_model'].search([('location_id', '=', self.source_location_id.id), ('state', '=', 'bad')])
            item_ids = [detail.id for detail in item_details]
            return {
                'domain': {
                    'item_detail_id': [('id', 'in', item_ids)]
                }
            }

    def move_items_to_retired(self):
        self.ensure_one()
        if not self.target_location_id:
            raise UserError('Please select a retired location.')

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
        res = super(MoveItemsToRetiredWizard, self).default_get(fields)
        if 'source_location_id' in self.env.context:
            res['source_location_id'] = self.env.context['source_location_id']
        return res
