from base64 import b64encode
import shopify
import requests
from odoo import models

from .tools import shopify_session_required


class ProductProduct(models.Model):
    _inherit = "product.product"

    def update_product_info(self, product, image_data):
        """Generates dict for data updating, updates product on new data"""
        self.ensure_one()
        write_dict = {}
        title = product.attributes.get('title')
        if title and self.name != title:
            write_dict["name"] = product.attributes.title
        description = product.attributes.get('body_html')
        if description and self.description_sale != description:
            write_dict["description_sale"] = product.attributes.body_html
        if image_data and self.image_variant_1920 != image_data:
            write_dict["image_variant_1920"] = image_data
        if write_dict:
            self.sudo().write(write_dict)

    @shopify_session_required
    def update_shopify_products(self):
        """Take products from shopify, updates name, description, img, qty.
         Creates product if it does not exists."""
        # TODO pagination (250 records atm)
        products = shopify.Product.find()
        for product in products:
            product_id = self.env["product.product"].sudo().search([
                ("default_code", "=", str(product.id))], limit=1)
            image_data = False
            images = product.attributes['images']
            if images and images[0].attributes['src']:
                url = images[0].attributes['src']
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    image_data = b64encode(response.content)
            if product_id:
                product_id.update_product_info(product, image_data)
            else:
                product_id = self.env["product.product"].sudo().create({
                    "name": product.attributes.get('title'),
                    "detailed_type": "product",
                    "description_sale": product.attributes.get('body_html'),
                    "image_variant_1920": image_data,
                    "default_code": str(product.id),
                })
            # Updating product qty in stock
            variants = product.attributes.get("variants", [])
            qty =\
                sum([item.attributes.get("inventory_quantity", 0) for item in variants])
            self.env["stock.quant"].update_product_qty({product_id: qty or 0})
