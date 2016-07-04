# -*- coding: utf-8 -*-
##############################################################################
#
#    odoo-saas-model , Open Source Management Solution
#    Copyright (C) 2016 binhes (<http://www.binhes.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp import release

class saas_website(http.Controller):
    @http.route('/saas/apply/', auth='public', website=True)
    def list(self, **kwargs):
        password = request.session.password
        version = release.version_info[0]
        users = http.request.env['saas.user.info']
        servers = http.request.env['saas.server']
        if version==9:
            csrf_token = request.csrf_token()
        else :
            csrf_token = 'None'
        values = {
            'users': users.search([]),
            'servers': servers.search([]),
            'password':password,
            'csrf_token':csrf_token
        }
        return http.request.render('saas_website.list', values)
    @http.route('/saas/create/', auth='user', website=True)
    def create(self, **kwargs):
        cr, uid, context = request.cr, request.session.uid, request.context
        password = request.session.password
        version = release.version_info[0]
        if version==9:
            csrf_token = request.csrf_token()
        else :
            csrf_token = 'None'
        if not request.session.uid:
            return http.local_redirect('/saas/create')
        else :
            user_id = request.session.uid
            partner_id = request.registry['res.users'].read(cr, uid, user_id, ['partner_id'])['partner_id'][0]
        if len(kwargs):
            values = {'user':partner_id,
                  'host_name': kwargs['domain_name'],
                  'server':kwargs.get('server_select', False),
                  }
            ids = request.registry['saas.user.info'].create(cr, uid, values,context=context)
            request.registry['saas.user.info'].create_use_db(cr, uid, [ids],password,context=context)
            template = request.registry('ir.model.data').get_object(cr, SUPERUSER_ID, 'saas_admin', 'registry_saas_db_email')
            request.registry('mail.template').send_mail(cr, SUPERUSER_ID, template.id, ids, force_send=True, raise_exception=True, context=context)
        users = http.request.env['saas.user.info']
        servers = http.request.env['saas.server']
        values = {
            'users': users.search([]),
            'servers': servers.search([]),
            'password':password,
            'csrf_token':csrf_token
        }
        return http.request.render('saas_website.list', values)