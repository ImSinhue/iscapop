from odoo import models, fields, api

class ItemDetail(models.Model):
    _name = 'iscapop_app.item_detail_model'
    _description = 'Item Detail Model'
    _rec_name = 'item_state'



    item_id = fields.Many2one('iscapop_app.item_model', string='Equipment', required=True,ondelete="cascade")
    location_id = fields.Many2one('iscapop_app.location_model', string='Location', required=True)
    quantity = fields.Integer(string='Quantity', required=True, default=1)
    stock = fields.Integer(string='Stock', required=True, default=0)
    state = fields.Selection([('new', 'New'),('good', 'Good'),('bad', 'Bad'),], string='State', required=True)
    photo = fields.Binary(related="item_id.photo")
    active = fields.Boolean(string='Active', default=True)
    item_state = fields.Char(string="Item and State", compute="_compute_item_state", store=True)

    @api.onchange('stock')
    def _onchange_stock(self):
        if self.stock <= 0:
            self.active = False

    @api.depends('item_id', 'state')
    def _compute_item_state(self):
        for record in self:
            item_name = record.item_id.name if record.item_id else ''
            state = record.state if record.state else ''
            record.item_state = f"{item_name}, {state}"