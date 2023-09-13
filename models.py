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

    currency_id  = fields.Many2one('res.currency',readonly=True, 
                    default=lambda self: self.env['res.currency'].search([('name', '=', 'AED')], limit=1))
    price        = fields.Monetary(string='Price',compute="_compute_price", currency_field='currency_id')
    
    distance_per_day = fields.Integer(string="distance_per_day")


    #Adds Interactive Calculation Feature
    # @api.depends('distance_per_day')
    # def _get_price(self):
    #     if self.distance_per_day > 200:

    #         # Assuming that we our client rent cars for a 100 AED/day and Add Fine AED 10
    #         return 100 + int( ( self.distance_per_day - 200 ) * 10 )
    #     else:
    #         return 100
        
    @api.depends( "rent_start_period", "rent_end_period")
    def _compute_price(self):
        for rec in self:
            if  rec.rent_start_period and rec.rent_end_period:
                rec.price = 200 * float((rec.rent_end_period - rec.rent_start_period).days)
                if rec.distance_per_day > 200:
                    var = (rec.distance_per_day - 200) * 10
                    rec.price += var

            elif  not rec.rent_start_period and rec.rent_end_period:
                rec.rent_start_period = fields.Datetime.today()
                rec.price = 200 * float((rec.rent_start_period - rec.rent_end_period).days)
                if rec.distance_per_day > 200:
                    var = (rec.distance_per_day - 200) * 10
                    rec.price += var

            else:
                rec.price = 0






