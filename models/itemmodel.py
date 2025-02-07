from odoo import models, fields

class ItemModel(models.Model):
    _name = 'iscapop_app.item_model'
    _description = 'iscapop_app.item_model'
    _rec_name = 'name'


    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    photo = fields.Binary(string='Foto')
    category_id = fields.Many2one('iscapop_app.category_model', string='Category', required=True)
    state = fields.Selection([('new', 'New'),('good', 'Good'),('bad', 'Bad'),], string='State', default='new', required=True)
    documentation = fields.Binary(string='Documentation')

    item_detail_ids = fields.One2many('iscapop_app.item_detail_model', 'item_id', string='Article Details',ondelete="cascade")
    full_stock = fields.Integer(string='Total Stock', compute='_compute_full_stock', readonly=True)


    def _compute_full_stock(self):
        for item in self:
            item.full_stock = sum(detail.stock for detail in item.item_detail_ids)
