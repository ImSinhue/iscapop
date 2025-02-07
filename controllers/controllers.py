# -*- coding: utf-8 -*-
# from odoo import http


# class IscapopApp(http.Controller):
#     @http.route('/iscapop_app/iscapop_app', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iscapop_app/iscapop_app/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iscapop_app.listing', {
#             'root': '/iscapop_app/iscapop_app',
#             'objects': http.request.env['iscapop_app.iscapop_app'].search([]),
#         })

#     @http.route('/iscapop_app/iscapop_app/objects/<model("iscapop_app.iscapop_app"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iscapop_app.object', {
#             'object': obj
#         })

