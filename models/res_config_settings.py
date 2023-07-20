from odoo import models, fields, _
from .tools import get_shopify_session


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    vn_shopify_admin_token = fields.Char(
        string="Shopify Admin Token",
        config_parameter='test_shopify_connector.vn_shopify_admin_token')
    vn_shopify_shop_address = fields.Char(
        string="Shopify Shop Address",
        config_parameter='test_shopify_connector.vn_shopify_shop_address')

    def return_sticky_note(self, msg, msg_type, is_sticky):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': msg,
                'type': msg_type,
                'sticky': is_sticky,
            }
        }

    def test_shopify_connection(self):
        if not self.vn_shopify_admin_token:
            return self.return_sticky_note(
                _("Please, enter Shopify Admin Token"), 'warning', False)
        if not self.vn_shopify_shop_address:
            return self.return_sticky_note(
                _("Please, enter Shopify Shop Address"), 'warning', False)
        api_session = get_shopify_session(
            self.vn_shopify_shop_address, self.vn_shopify_admin_token)
        # valid needs check
        if api_session.valid:
            return self.return_sticky_note(
                _("Success! Connection works fine!"), 'success', False)
        return self.return_sticky_note(
            _("Connection not valid :("), 'warning', False)
