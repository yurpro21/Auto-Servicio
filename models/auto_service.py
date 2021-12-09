# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tests import Form

class AutoService(models.Model):
    _name = 'auto.service'
    _description = 'Auto Servicios'

    name = fields.Char(string='Patente/matrícula del vehículo.',required=True)
    partner_id = fields.Many2one('res.partner', string='Dueño del vehículo',required=True)
    service_invoice_id = fields.Many2one('account.move', string='Factura')
    product_ids = fields.Many2many('product.product',string='Servicios',required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('done', 'Hecho'),
        ('cancel', 'Cancelado'),
    ], string='Estado', default='draft')




    def action_to_done(self):
        for line in self:
            line.state = 'done'



    def action_return_to_draft(self):
        for line in self:
            line.state = 'draft'


#generamos la factura con el documento del servicio solicitado 

    def action_create_invoice(self):
        self.ensure_one()
        company_id=self.env.user.company_id
        move_form = Form(self.env["account.move"].with_context(
                    force_company=company_id.id ))

        date = fields.Date.today()
        line_form = move_form.invoice_line_ids.new()
        
        invoice_line_values = line_form._values_to_save(all_fields=True)
        

        invoice_vals = move_form._values_to_save(all_fields=True)
        invoice_vals.update({
            'company_id': self.env.user.company_id.id,
            'ref':self.name,
            'journal_id': self.get_invoice_journal().id,
            'user_id': self.env.user.id,
            'currency_id': self.partner_id.property_product_pricelist.currency_id.id,
            'invoice_date': date,
            'partner_id':self.partner_id,
            'type':'out_invoice'
        })
        
        
        for product in self.product_ids:

            invoice_line_values=({
                "quantity": 1,
                "product_id": product.id,
                "product_uom_id": product.uom_id.id,
                "name":'Auto servicio',
                "price_unit": product.list_price,
                
            })
            
        
            invoice_vals["invoice_line_ids"].append((0, 0, invoice_line_values))
        

        invoice = self.env['account.move'].create(invoice_vals)


        invoice.action_post()
        self.service_invoice_id = invoice

        return True


    def get_invoice_journal(self):
        return self.env['account.journal'].search([('type', '=', 'sale')], limit=1)

class ProductTemplate(models.Model):
    _inherit = 'product.template'


    id_service = fields.Many2one(
        'auto.service.vehicle',
    )

    is_auto_service = fields.Boolean(string='Auto Servicio')
