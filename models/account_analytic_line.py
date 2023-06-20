# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, exceptions
import logging

_logger = logging.getLogger('onesta --> ')


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    sh_cost_center_id = fields.Many2one('sh.cost.center', 'Centro de Costo', compute='_compute_cost_center', store=True)
    
    @api.depends('move_line_id')
    def _compute_cost_center(self):
        for rec in self:
            rec.sh_cost_center_id = rec.move_line_id.sh_cost_center_id.id
    