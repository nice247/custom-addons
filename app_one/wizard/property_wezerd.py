from odoo import fields, models

class PropertyWizard(models.TransientModel):
    _name = 'property.wizard'
    _description = 'Property Wizard'

    property_id = fields.Many2one('property')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending')
    ], default='draft')
    reason = fields.Char()

    def action_confirm(self):
        if self.property_id.status == 'closed':
            self.property_id.status = self.status