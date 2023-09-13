# from datetime import datetime

from odoo import api, fields, models, _


class CarsRental(models.Model):
    _name = "cars.rental"

    name = fields.Char(string="Name", required=True)
    address = fields.Char('Address')

    day_price = fields.Float(string='Day Price', digits=(16, 0))
    start_date = fields.Date(string="Start Date", tracking=1)
    end_date = fields.Date(string="Received Date", tracking=1)
    currency_id = fields.Many2one('res.currency',readonly=True, default=lambda self: self.env['res.currency'].search([('name', '=', 'AED')], limit=1))
    price = fields.Monetary(string='Price', digits=(16, 0), readonly=True,
                            compute="_compute_price", currency_field='currency_id')
    
    km = fields.Float(string="KM")
    fine = fields.Float(string="Delay tax")


    @api.depends("day_price", "start_date", "end_date", "fine")
    def _compute_price(self):
        for rec in self:
            if rec.day_price and rec.start_date and rec.end_date:
                rec.price = rec.day_price * float((rec.end_date - rec.start_date).days)
                if rec.km > 200:
                    var = (rec.km - 200) * rec.fine
                    rec.price += var

            elif rec.day_price and not rec.start_date and rec.end_date:
                rec.start_date = fields.Datetime.today()
                rec.price = rec.day_price * float((rec.start_date - rec.end_date).days)
                if rec.km > 200:
                    var = (rec.km - 200) * rec.fine
                    rec.price += var

            else:
                rec.price = 0


    # def action_draft(self):
    #     return self.write({'state': 'draft'})

    # def action_rented(self):
    #     return self.write({'state': 'rented'})

    # def action_cancel(self):
    #     return self.write({'state': 'cancel'})

    # @api.model
    # def create(self, vals):
    #     if not self.ref and not vals.get('ref'):
    #         vals['ref'] = self.env['ir.sequence'].next_by_code('cars.rental')
    #     return super(CarsRental, self).create(vals)




