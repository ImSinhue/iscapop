from odoo import models, fields

class CategoryModel(models.Model):
    _name = 'iscapop_app.category_model'
    _description = 'iscapop_app.category_model'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    father_id = fields.Many2one('iscapop_app.category_model', string='Parent Category')
    child_ids = fields.One2many('iscapop_app.category_model', 'father_id', string='Subcategories')
    item_ids = fields.One2many('iscapop_app.item_model', 'category_id', string='Equipment')
