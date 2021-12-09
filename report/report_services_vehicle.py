
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class ServicesVehicleReport(models.Model):
    _name = "services.vehicle.report"
    _description = "Analisis Reportes Autoservicio"
    _auto = False
    _order = 'services'

    @api.model
    def _get_done_states(self):
        return ['sale', 'done', 'paid']

    services = fields.Integer('Cantidad de Servicios', readonly=True)
    vehicle = fields.Char(string="Producto")



    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            autoser.id as id ,autoser.name as vehicle,count(asppl.product_product_id) as "services" from auto_service_product_product_rel as asppl
            inner join auto_service as autoser on autoser.id=asppl.auto_service_id
            inner join account_move as am on autoser.service_invoice_id=am.id
            where am.state='posted'

        """

        groupby_ = """
            autoser.name,autoser.id
            
        """ 
        orderby_ = """
            services

            
        """ 
        return '(SELECT %s GROUP BY %s ORDER BY %s DESC)' % ( select_, groupby_,orderby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

class ServicesReportVehicle(models.AbstractModel):
    _name = 'report.services.report_vehicle'
    _description = 'Reporte Vehiculos'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['services.vehicle.report'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'services.vehicle.report',
            'docs': docs,
            'proforma': True
        }
