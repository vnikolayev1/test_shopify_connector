
from odoo import models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def update_product_qty(self, update_dict):
        """Updated product qty in stock, bypassing admin"""
        admin_id = self.env.ref('base.partner_admin').sudo().user_ids[0].id
        for update_key, update_val in update_dict.items():
            stock_quant = self.env['stock.quant'].sudo().search([
                ('product_id', '=', update_key.id)], limit=1)
            warehouse = self.env['stock.warehouse'].search(
                [('company_id', '=', self.env.company.id)], limit=1)
            lot_stock_id = warehouse.lot_stock_id
            if not stock_quant:
                stock_quant = self.env["stock.quant"].with_user(admin_id).create({
                    "inventory_quantity": update_val,
                    "product_id": update_key.id,
                    "location_id": lot_stock_id.id
                })
            if stock_quant.inventory_quantity != update_val:
                stock_quant.with_user(admin_id).write({
                    "inventory_quantity": update_val,
                })
            stock_quant.with_user(admin_id).action_apply_inventory()
