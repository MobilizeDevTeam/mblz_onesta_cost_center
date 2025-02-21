# -*- coding: utf-8 -*-
from odoo import models, api, _, fields
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger('onesta --> ')


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'
    
    def _validate_accounting_entries(self):
        res = super(StockValuationLayer, self)._validate_accounting_entries()
        for rec in self:
            purchase_id = rec.stock_move_id.picking_id.purchase_id
            sale_id = rec.stock_move_id.picking_id.sale_id
            if purchase_id:
                for line in rec.account_move_id.line_ids:
                    if purchase_id.order_line[0].analytic_distribution:
                        analytic = list(purchase_id.order_line[0].analytic_distribution.keys())[0]
                        # NOTE: se presentan casos donde el analitico es así: {"false": 100}
                        # terminando en un error por no poder convertirlo a un entero
                        if analytic.isdigit():
                            line.analytic_distribution = {str(analytic): 100}
            elif sale_id:
                for line in rec.account_move_id.line_ids:
                    if sale_id.order_line[0].analytic_distribution:
                        analytic = list(sale_id.order_line[0].analytic_distribution.keys())[0]
                        if analytic.isdigit():
                            line.analytic_distribution = {str(analytic): 100}
                        
            # NOTE: este bloque depende del modulo mblz_onesta_lot_analytic
            # no usa como dependencia ya que genera un efecto cíclico
            elif rec.stock_move_id.analytic_distribution:
                for line in rec.account_move_id.line_ids:
                    line.analytic_distribution = rec.stock_move_id.analytic_distribution
                    if rec.stock_move_id.picking_id and rec.stock_move_id.picking_id.sh_cost_center_id:
                        line.sh_cost_center_id = rec.stock_move_id.picking_id.sh_cost_center_id
        return res