from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=True)
    expected_sale_date = fields.Date()
    is_late = fields.Boolean(default=False)
    expected_price = fields.Float()
    deft = fields.Float(compute='_compute_def')
    sale_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('east', 'East'), ('north', 'North'), ('west', 'West'), ('south', 'South')
    ])

    owner_id = fields.Many2one('owner')
    owner_phone = fields.Char(related='owner_id.phone')
    owner_address = fields.Char(related='owner_id.address')

    line_ids = fields.One2many('property.line', 'property_id')
    status = fields.Selection([
        ('draft', 'Draft'), ('pending', 'Pending'), ('approved', 'Approved'), ('closed', 'Closed')
    ], default='draft')
    _sql_constraints = [
        ('name', 'unique(name)', 'This name is already exist!'),
    ]

    @api.constrains('bedrooms')
    def _check_bedrooms_constraint(self):
        for record in self:
            if record.bedrooms == 0:
                raise ValidationError("Bedrooms must be greater than 0!")

    @api.depends('expected_price', 'sale_price', 'owner_id.phone')
    def _compute_def(self):
        for record in self:
            record.deft = record.expected_price - record.sale_price

    def action_draft(self):
        for record in self:
            record.status = 'draft'

    def action_pending(self):
        for record in self:
            record.status = 'pending'

    def action_approved(self):
        for record in self:
            record.status = 'approved'

    def action_closed(self):
        for record in self:
            record.status = 'closed'

    def check_expected_sale_date(self):
        property_ids = self.search([])
        for record in property_ids:
            if record.expected_sale_date and record.expected_sale_date < fields.Date.today():
               record.is_late = True
    def action_status_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.property_change_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def action_open_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action


class PropertyLine(models.Model):
    _name = 'property.line'
    _description = 'Property Line'

    area = fields.Float()
    description = fields.Text()

    property_id = fields.Many2one('property')
