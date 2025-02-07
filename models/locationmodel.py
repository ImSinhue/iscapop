from odoo import models, fields, api

class LocationModel(models.Model):
    _name = 'iscapop_app.location_model'
    _description = 'Location Model'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    location_type = fields.Selection([('warehouse', 'Warehouse'), ('class', 'Class'), ('retired', 'Retired')], string='Location Type', required=True)
    item_detail_ids = fields.One2many('iscapop_app.item_detail_model', 'location_id', string='Items')
    # Related fields
    item_state = fields.Selection(related='item_detail_ids.state', string='Item State', readonly=True, store=True)
    item_stock = fields.Integer(related='item_detail_ids.stock', string='Item Stock', readonly=True, store=True)

    def open_move_items_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Move Items to Warehouse',
            'res_model': 'iscapop_app.move_items_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_source_location_id': self.id,
            }
        }

    def open_move_to_donation_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Move Items to Donation',
            'res_model': 'iscapop_app.move_to_donation_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_source_location_id': self.id,
            }
        }


    def open_move_items_to_retired_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Move Items to Retired',
            'res_model': 'iscapop_app.move_items_to_retired_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_source_location_id': self.id}
        }
    
    def delete_all_items_in_retired(self):
        self.ensure_one()
        if self.location_type != 'retired':
            raise KeyError("Esta acción solo puede realizarse en la ubicación 'Retired'.")

        if not self.item_detail_ids:
            raise KeyError("No hay ítems en esta ubicación para eliminar.")

        self.item_detail_ids.unlink()

        return {
            'effect': {
                'fadeout': 'slow',
                'message': "All items in ‘Retired’ have been removed.",
                'type': 'rainbow_man',
            }
        }
