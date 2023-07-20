import logging
import shopify
from odoo import _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


def get_shopify_session(shop_address, admin_token):
    """Connects with shopify, gets session"""
    return shopify.Session(
        shop_address, '2021-10', admin_token)


def shopify_session_required(func):
    def wrapper(self, *args, **kwargs):
        admin_token = self.env['ir.config_parameter'].sudo().get_param(
            'test_shopify_connector.vn_shopify_admin_token')
        shop_address = self.env['ir.config_parameter'].sudo().get_param(
            'test_shopify_connector.vn_shopify_shop_address')
        if not admin_token or not shop_address:
            if self.env.context.get('is_cron', False):
                _logger.warning(
                    "Shopify admin token and/or shop address not set."
                    " Skipping execution silently."
                )
                return func(self, *args, **kwargs)
            raise UserError(_("Shopify admin token and/or shop address not set."))
        session = get_shopify_session(shop_address, admin_token)
        shopify.ShopifyResource.activate_session(session)
        return func(self, *args, **kwargs)
    return wrapper
