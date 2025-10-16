from odoo import models, fields

class building(models.Model):
    _name = 'building'
    _description = 'Building'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    no = fields.Integer(string='No')
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)