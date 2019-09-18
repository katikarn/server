from odoo import models, fields, api
from datetime import datetime


class Car(models.Model):
    _name = 'tms.car'
    _rec_name = 'name'
    _order = 'name'
    image = fields.Binary("Image", attachment=True)
    name = fields.Char(string='Name', required=True, help="Enter a car name")
    model = fields.Char(string='Model')
    reg_id = fields.Char(string='Reg ID')
    driver_name = fields.Char(string='Driver Name')
    type = fields.Selection([('S', 'รถเก๋ง'), ('P', 'รถปิกอัพ'), ('T', 'รถบรรทุก')], string='Type', default='S')
    year = fields.Char(string='Year')
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible")


class Product(models.Model):
    _inherit = 'product.template'
    gallery = fields.Binary("Gallery", attachment=True)
