from odoo import models, fields, api
from datetime import datetime
from .bahttext import bahttext


class Ticket(models.Model):
    _name = 'tms.ticket'
    _rec_name = 'ticket_no'
    ticket_no = fields.Char(string='Ticket No')
    ticket_date = fields.Datetime(string='Ticket Date', default=datetime.now())
    description = fields.Text()
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    est_time = fields.Float(string='Estimate Time (Hrs)', digits=(6, 2), readonly=True)
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible")
    car_id = fields.Many2one('tms.car', ondelete='set null', string="Car")
    ticket_items = fields.One2many('tms.ticket_item', 'ticket_id', string="Ticket Items")
    state = fields.Selection([('draft', 'Draft'), ('approve', 'Approve'), ('complete', 'Complete')], default='draft')
    total_qty = fields.Integer("Total Qty", compute="_get_sum_qty")
    total_amount = fields.Float("Total Amount", digits=(6, 2), compute="_get_total_amount")

    @api.multi
    @api.onchange('ticket_items')
    def _get_sum_qty(self):
        total_qty = 0
        for r in self:
            for item in r.ticket_items:
                total_qty += item.qty
        self.total_qty = total_qty

    @api.multi
    @api.onchange('ticket_items')
    def _get_total_amount(self):
        total_amount = 0
        for r in self:
            for item in r.ticket_items:
                total_amount += item.amount
        self.total_amount = total_amount

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('ticket.doc_no') or '-'
        vals['ticket_no'] = seq
        return super(Ticket, self).create(vals)

    # @api.model
    # def _get_ticket_no(self):
    #     seq = self.env['ir.sequence'].next_by_code('ticket.doc_no') or '-'
    #     return seq

    @api.one
    def do_ticket_approve(self):
        self.write({'state': 'approve'})

    @api.one
    def do_ticket_completed(self):
        self.write({'state': 'complete'})

    @api.one
    def do_ticket_draft(self):
        self.write({'state': 'draft'})

    @api.model
    def get_baht_text(self):
        return bahttext(self.total_amount)


class TicketItem(models.Model):
    _name = 'tms.ticket_item'
    ticket_id = fields.Many2one('tms.ticket', ondelete='cascade', string="Ticket", required=True)
    product_id = fields.Many2one('product.product', string="Product")
    ref_doc = fields.Char(string='Ref Doc')
    price = fields.Float(string='Price', digits=(6, 2))
    qty = fields.Integer(string='Qty')
    amount = fields.Float(string='Amount', digits=(6, 2))
    line_amount = fields.Float(string='Amount', readonly=True, stored=False)
    remark = fields.Text()

    @api.multi
    @api.onchange('product_id')
    def _product_id_changed(self):
        self.price = self.product_id.list_price
        if not self.qty:
            self.qty = 1
        self.amount = self.price * self.qty
        self.line_amount = self.amount

    @api.multi
    @api.onchange('price', 'qty')
    def _price_changed(self):
        self.amount = self.price * self.qty
        self.line_amount = self.amount


class ParticularReport(models.AbstractModel):
    _name = 'report.tms_app.report_ticket_view'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('tms_app.report_ticket_view')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('tms_app.report_ticket_view', docargs)

    @api.multi
    def _get_report_values(self, docids, data=None):
        docs = self.env['tms.ticket'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'tms.ticket',
            'docs': docs,
        }
