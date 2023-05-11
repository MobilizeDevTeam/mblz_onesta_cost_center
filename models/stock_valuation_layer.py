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
                    line.analytic_distribution = {str(purchase_id.analytic_account_id.id): 100}
            
            sale_id = rec.stock_move_id.picking_id.sale_id
            if sale_id:
                for line in rec.account_move_id.line_ids:
                    line.analytic_distribution = {str(sale_id.o_analytic_account_id.id): 100}
        return res