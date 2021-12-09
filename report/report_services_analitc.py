# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class ServicesReport(models.Model):
    _name = "services.report"
    _description = "Analisis Reportes Autoservicio"
    _auto = False
    _order = 'amount_total'

    @api.model
    def _get_done_states(self):
        return ['sale', 'done', 'paid']

    quantity = fields.Integer('Cantidad', readonly=True)
    product_id = fields.Many2one('product.template', 'Product Variant', readonly=True)
    product_name = fields.Char(string="Producto")
    amount_total = fields.Float('Monto Facturado', readonly=True)



    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            aml.product_id as id,aml.product_id as product_id,count(aml.product_id) as "quantity",sum(aml.price_unit) as "amount_total",pd.name as product_name from account_move_line as aml
            inner join account_move as am on am.id=aml.move_id
            inner join product_template as pd on pd.id=aml.product_id
            where aml.product_id IS NOT NULL and am.state='posted' and am.type='out_invoice' and pd.is_auto_service=True
        """


        groupby_ = """
            aml.price_unit,aml.product_id,pd.name,aml.product_id
            
        """ 
        orderby_ = """
            amount_total 

            
        """ 
        return '(SELECT %s GROUP BY %s ORDER BY %s DESC)' % ( select_, groupby_,orderby_)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

class ServocesReportReport(models.AbstractModel):
    _name = 'report.services.report_report'
    _description = 'Proforma Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['auto.services'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'auto.services',
            'docs': docs,
            'proforma': True
        }
