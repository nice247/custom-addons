from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Task Management'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Task Name', required=True)
    description = fields.Text('Task Description')
    assignee_id = fields.Many2one('res.partner', string='Assign To')
    assign_date = fields.Date('Assign Date', default=date.today(), readonly=True)
    due_date = fields.Date('Due Date')
    is_late = fields.Boolean(default=False)
    status = fields.Selection(
        [('new', 'New'), ('in_progress', 'In Progress'), ('done', 'Done'), ('overdue', 'Overdue')], default='new')
    is_new = fields.Boolean(default=False)
    is_in_progress = fields.Boolean(default=False)
    is_done = fields.Boolean(default=False)
    active = fields.Boolean(default=True)

    # Added fields
    estimated_time = fields.Float('Estimated Time', help="Estimated time to complete the task in hours")
    timesheet_ids = fields.One2many('account.analytic.line', 'task_id', string='Timesheets')
    total_timesheet_time = fields.Float(
        string='Total Timesheet Time',
        compute='_compute_total_timesheet_time',
        store=True
    )
    remaining_time = fields.Float(
        string='Remaining Time',
        compute='_compute_remaining_time',
        store=True
    )

    @api.depends('timesheet_ids.unit_amount')
    def _compute_total_timesheet_time(self):
        for record in self:
            record.total_timesheet_time = sum(record.timesheet_ids.mapped('unit_amount'))

    @api.depends('estimated_time', 'total_timesheet_time')
    def _compute_remaining_time(self):
        for record in self:
            record.remaining_time = record.estimated_time - record.total_timesheet_time

    @api.constrains('estimated_time', 'timesheet_ids')
    def _check_timesheet_time_not_exceed_estimated(self):
        for record in self:
            if record.estimated_time > 0 and record.total_timesheet_time > record.estimated_time:
                raise ValidationError(
                    "Total timesheet time (%sh) exceeds estimated time (%sh) for task '%s'" % (
                        record.total_timesheet_time, record.estimated_time, record.name
                    ))

    def check_status(self):
        task_ids = self.search([])
        for record in task_ids:
            if record.status == 'done':
                record.is_done = True
                record.is_new = False
                record.is_in_progress = False
                record.is_late = False
            else:
                if record.assign_date == date.today() and record.due_date >= date.today():
                    record.status = 'new'
                    record.is_new = True
                    record.is_done = False
                    record.is_in_progress = False
                    record.is_late = False
                elif record.due_date > date.today():
                    record.status = 'in_progress'
                    record.is_in_progress = True
                    record.is_new = False
                    record.is_done = False
                    record.is_late = False
                else:
                    record.status = 'overdue'
                    record.is_late = True
                    record.is_new = False
                    record.is_in_progress = False
                    record.is_done = False

    def action_done(self):
        for record in self:
            record.status = 'done'


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    task_id = fields.Many2one('todo.task', string = 'Task')
