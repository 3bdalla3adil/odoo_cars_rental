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
    
    price            = fields.Monetary(string='Price',compute="_compute_price", currency_field='currency_id')
    currency_id      = fields.Many2one('res.currency',readonly=True)
    distance_per_day = fields.Integer(string="distance_per_day")

    # to set the currency to be 'AED' 
    def define_currency_name(self):
        # find the 'AED' currency id in 'res.currency' model
        currency = self.env['res.currency'].search([('name', '=', 'AED')], limit=1)
        
        # check if 'AED' id found (if not present will be False)
        # if 'AED' not present to the 'res.currency' model 
        if not currency:
            
            # create a new currency with name of 'AED' and add it to the 'res.currency' model
            currency = self.env['res.currency'].create({'name': 'AED'})
            
        # set currency_id field to 'AED' id
        self.currency_id = currency

    def check_exceeded_distance(self,distance_per_day,price):
        if distance_per_day > 200:
            # calculate the extra kilometers as 10 AED Fine 
            extra_km_fine = int(distance_per_day - 200) * 10
            # and add the Fine to the price
            price += extra_km_fine

    @api.depends( "rent_start_period", "rent_end_period")
    def _compute_price(self):
        
        for record in self:

            # chech if user set starting period and ending period
            if  record.rent_start_period and record.rent_end_period:
                # calculate price upon the start date and end date 
                # assuming the customer is able to rent at any period of time
                record.price = 100 * int((record.rent_end_period - record.rent_start_period).days)
                
                # check if the distance exceeded 200 KM
                self.check_exceed_distance(record.distance_per_day,record.price)

            elif  not record.rent_start_period and record.rent_end_period:
                # assuming the starting period and ending period is the time when user saved the record 
                record.rent_start_period = fields.Datetime.today()
                # count the deifference between starting and ending date to calculate price over the renting period
                record.price = 100 * int((record.rent_start_period - record.rent_end_period).days)
                # check if the distance exceeded the 200 KM
                self.check_exceed_distance(record.distance_per_day,record.price)
                
            # if niether starting nor ending rent period set
            else:
                # check if the distance exceeded 200 KM
                self.check_exceed_distance(record.distance_per_day,record.price)

                # set price as zero
                record.price = 100