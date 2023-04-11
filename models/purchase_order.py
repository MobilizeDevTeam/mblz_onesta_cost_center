# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, _, _lt, fields
from odoo.tools.misc import format_date
from datetime import timedelta

from collections import defaultdict

import logging
_logger = logging.getLogger('onesta --> ')


class PurchaseOrder(models.AbstractModel):
    _inherit = "purchase.order"
    
    def action_create_invoice(self):
        res = super(PurchaseOrder, self).action_create_invoice()
        for rec in self:
            for inv in rec.invoice_ids:
                for line in inv.line_ids:
                    if not line.sh_cost_center_id and rec.order_line[0].sh_cost_center_id:
                        line.sh_cost_center_id = rec.order_line[0].sh_cost_center_id.id
                    if not line.analytic_distribution and rec.order_line[0].analytic_distribution:
                        line.analytic_distribution = rec.order_line[0].analytic_distribution
        return res
