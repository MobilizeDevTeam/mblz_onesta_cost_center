# -*- coding: UTF-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.osv import expression


class ShCostCenter(models.Model):
    _inherit = 'sh.cost.center'
    
    parent_id = fields.Many2one('sh.cost.center', 'Centro de costo padre')
    
    def _get_path_name(self):
        name = self.sh_title
        if self.parent_id:
            name = self.parent_id._get_path_name() + ' / ' + name
        return name
    
    @api.depends('sh_code', 'sh_title', 'parent_id')
    def _compute_display_name(self):
        for rec in self:
            name = rec._get_path_name()
            rec.display_name = rec.sh_code + " - " + name
    
    def name_get(self):
        return [(record.id, record.display_name) for record in self]
            
    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if not name:
            return super(ShCostCenter, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
        domain = expression.AND([['|', '|', ('sh_code', operator, name), ('sh_title', operator, name), ('display_name', operator, name)], args]) if name else args
        recs = self.search(domain, limit=limit)
        return [i[0] for i in recs.name_get()]
    
    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('No puede crear centros de costo recursivos.'))
