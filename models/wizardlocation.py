from odoo import models, fields, api

class LocationWizard(models.TransientModel):
    _name = 'iscapop_app.location_wizard'
    _description = 'Location Wizard'

    donation_id = fields.Many2one(
        'iscapop_app.donation_model', 
        string='Donation', 
        required=True, 
        default=lambda self: self.env.context.get('default_donation_id')
    )
    location_id = fields.Many2one(
        'iscapop_app.location_model', 
        string='Location', 
        required=True
        # No modificamos el campo aquí
    )

    def confirm_location(self):
        self.donation_id.write({
            'reserved_by': self.env.uid,
            'reserved': True,
            'location_id': self.location_id.id
        })
