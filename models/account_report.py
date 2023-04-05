# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, _, _lt, fields
from odoo.tools.misc import format_date
from datetime import timedelta

from collections import defaultdict

import logging
_logger = logging.getLogger('onesta --> ')


class AccountReport(models.AbstractModel):
    _inherit = "account.report"
    
    @api.model
    def _get_options_costcenter_domain(self, options):
        domain = []
        if options.get('costcenter'):
            costcenter = [int(costcenter) for costcenter in options['costcenter']]
            domain.append(('sh_cost_center_id', 'in', costcenter))
        return domain
    
    def _get_options_domain(self, options, date_scope):
        domain = super(AccountReport, self)._get_options_domain(options, date_scope)
        domain += self._get_options_costcenter_domain(options)
        return domain
    
    @api.model
    def _get_options(self, previous_options=None):
        options = super(AccountReport, self)._get_options(previous_options)
        options.update({'use_costcenter': True, 'costcenter': previous_options.get('costcenter', []) if previous_options else []})
        return options
    
    def get_report_informations(self, previous_options):
        info = super(AccountReport, self).get_report_informations(previous_options)
        return info