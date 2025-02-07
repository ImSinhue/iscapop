import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

class DonationModel(models.Model):
    _name = 'iscapop_app.donation_model'
    _description = 'Donation Model'

    # Campos existentes...
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    photo = fields.Binary(string='Photo')
    state = fields.Selection([('new', 'New'), ('good', 'Good'), ('bad', 'Bad')], string='State', default='new', required=True)
    documentation = fields.Binary(string='Documentation')
    quantity = fields.Integer(string='Quantity', required=True, default=1)
    item_id = fields.Many2one('iscapop_app.item_model', string='Item', required=True, ondelete="cascade")
    reserved = fields.Boolean(string='Reserved', default=False, readonly=True)
    donated_by = fields.Many2one('res.users', string='Donated by (IES)')
    donation_time = fields.Date(string='Donation Time', default=fields.Datetime.now, readonly=True)
    reserved_by = fields.Many2one('res.users', string='Reserved by (IES)')
    location_id = fields.Many2one('iscapop_app.location_model', string='Location')  # Campo nuevo

    # Métodos existentes...
    @api.onchange('quantity')
    def _onchange_quantity(self):
        if self.quantity <= 0:
            self.active = False

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

    def open_return_to_warehouse_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Return Items to Warehouse',
            'res_model': 'iscapop_app.return_to_warehouse_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_donation_id': self.id,
            }
        }

    

    def turn_to_unreserved(self):
        self.write({
            'reserved': False,
            'reserved_by': None
        })

    def open_location_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select Location',
            'res_model': 'iscapop_app.location_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_donation_id': self.id,
            }
        }
    

    def confirmDonation(self):
        item = self.item_id
        location = self.location_id

        # Validar que la cantidad sea positiva
        if self.quantity <= 0:
            raise UserError('La cantidad debe ser un número positivo.')

        # Crear un nuevo detalle de ítem con el stock correcto
        self.env['iscapop_app.item_detail_model'].create({
            'item_id': item.id,
            'location_id': location.id,
            'stock': self.quantity,  # Usamos 'stock' en lugar de 'quantity'
            'state': self.state,
        })

        reserved_user = self.reserved_by.user_ids[0]
        env_with_reserved_user = self.env(user = reserved_user)

        env_with_reserved_user['iscapop_app.item_model'].create({
            'name': item.name,
            'description': item.description,
            'photo': item.photo,
            'documentation': item.documentation,
            'state': item.state,
            'category_id': item.category_id.id
        })


        # Eliminar el registro de donación para que desaparezca de la lista
        self.unlink()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': "Donated correctly.",
                'type': 'rainbow_man',
            }
        }







