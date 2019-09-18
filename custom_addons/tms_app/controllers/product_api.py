import json
from odoo import http
from odoo.http import request, Response


class ProductAPI(http.Controller):

    @http.route('/product/list', type='http', website=True, methods=['GET'], auth="public")
    def product_list(self):
        products = request.env['product.template'].sudo().search([])
        rows = []
        for p in products:
            data = {
                'code': p.default_code,
                'name': p.name,
                'barcode': p.barcode,
                'sale_price': p.list_price,
                'cost_price': p.standard_price,
            }
            rows.append(data)
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')
