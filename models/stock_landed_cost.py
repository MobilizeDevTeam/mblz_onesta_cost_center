# -*- coding: utf-8 -*-
from odoo import models, api, _, fields
import logging

_logger = logging.getLogger('cost center --> ')


class AdjustmentLines(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'
    
    def _create_account_move_line(self, move, credit_account_id, debit_account_id, qty_out, already_out_account_id):
        res = super(AdjustmentLines, self)._create_account_move_line(move, credit_account_id, debit_account_id, qty_out, already_out_account_id)
        if self.cost_id.vendor_bill_id:
            landed_lines = self.cost_id.vendor_bill_id.invoice_line_ids.filtered(lambda l: l.is_landed_cost_line)
            if landed_lines and landed_lines[0].analytic_distribution:
                analytics = list(landed_lines[0].analytic_distribution.keys())
                for i in res:
                    i[2].update({
                        'analytic_distribution': {str(analytics[0]): 100}
                    })
        return res