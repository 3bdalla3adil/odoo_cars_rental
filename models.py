# from datetime import datetime

from odoo import api, fields, models, _


class CustomerInfo(models.Model):
    _name = 'client.info'

    name    = fields.Char('Name')
    address = fields.Char('Address')

    rent_start_period = fields.Date(string='Period Start Date')
    rent_end_period   = fields.Date(string='Period End Date')


class CarsRental(models.Model):
    _name = "cars.rental"
    _inherit = "client.info"

    # name    = fields.Char(string="Name", required=True)
    # address = fields.Char('Address')

    # day_price    = fields.Float(string='Day Price', digits=(16, 0))
    # start_period = fields.Date(string="Start Date", tracking=1)
    # end_period   = fields.Date(string="Received Date", tracking=1)
    currency_id  = fields.Many2one('res.currency',readonly=True, 
                    default=lambda self: self.env['res.currency'].search([('name', '=', 'AED')], limit=1))
    price        = fields.Monetary(string='Price',compute="_get_price", currency_field='currency_id')
    
    distance_per_day = fields.Integer(string="KM")
    # fine = fields.Float(string="Fine")


    #Adds Interactive Calculation Feature
    @api.depends('distance_per_day')
    def _get_price(self):
        if self.distance_per_day > 200:

            # Assuming that we our client rent cars for a 100 AED/day and Add 10 AED fine
            return 100 + ( ( self.distance_per_day - 200 ) * 10 )
        else:
            return 100
        
    # @api.depends("day_price", "start_date", "end_date", "fine")
    # def _compute_price(self):
    #     for rec in self:
    #         if rec.day_price and rec.start_date and rec.end_date:
    #             rec.price = rec.day_price * float((rec.end_date - rec.start_date).days)
    #             if rec.km > 200:
    #                 var = (rec.km - 200) * rec.fine
    #                 rec.price += var

    #         elif rec.day_price and not rec.start_date and rec.end_date:
    #             rec.start_date = fields.Datetime.today()
    #             rec.price = rec.day_price * float((rec.start_date - rec.end_date).days)
    #             if rec.km > 200:
    #                 var = (rec.km - 200) * rec.fine
    #                 rec.price += var

    #         else:
    #             rec.price = 0






