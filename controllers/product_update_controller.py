import json

from odoo import http
from odoo.http import request, Response
from odoo.tools.translate import _


class ProductUpdateController(http.Controller):

    def generate_update_dict(self, inc_data):
        """Generates dict where key is product.product and
        val is qty of this product in stock, returns error message if """
        update_dict = {}
        if not inc_data:
            response_err = _("Please, provide json with SKU and qty")
        for inc_key, inc_val in inc_data.items():
            update_key = request.env["product.product"].sudo().search(
                [("default_code", "=", inc_key)])
            response_err = False
            if not inc_key:
                response_err = _("Could not find %(code)s", code=inc_key)
            if isinstance(inc_val, float) or isinstance(inc_val, int):
                # rounding to 2 decimals, so we don't mess with stock
                update_dict[update_key] = round(inc_val, 2)
            else:
                response_err = _("Update qty should be int/float")
            if response_err:
                response = Response(response_err, status=403)
                response.headers['Content-Type'] = 'application/json'
                return response
        return update_dict

    @http.route('/product_update', methods=['POST'], type='json', auth='none')
    def product_update(self, **kwargs):
        """Updates information on product stock. Returns err on wrong request"""
        inc_data = json.loads(request.httprequest.data)
        update_dict = self.generate_update_dict(inc_data)
        if isinstance(update_dict, Response):
            return update_dict
        request.env["stock.quant"].update_product_qty(update_dict)
        json_data = json.dumps({"result": "OK"})
        return json_data
