# -*- coding: utf-8 -*-
from odoo import models, api, _, fields


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'
    
    def _validate_accounting_entries(self):
        res = super(StockValuationLayer, self)._validate_accounting_entries()
        for rec in self:
            purchase_id = rec.stock_move_id.picking_id.purchase_id
            if purchase_id:
                for line in rec.account_move_id.line_ids:
                    analytic = list(purchase_id.order_line[0].analytic_distribution.keys())[0]
                    line.analytic_distribution = {str(analytic): 100}
            
            sale_id = rec.stock_move_id.picking_id.sale_id
            if sale_id:
                for line in rec.account_move_id.line_ids:
                    analytic = list(sale_id.order_line[0].analytic_distribution.keys())[0]
                    line.analytic_distribution = {str(analytic): 100}
        return res