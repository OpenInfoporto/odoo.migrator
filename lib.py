import xmlrpclib


class Odoo():
    # describe Odoo Instance

    def __init__(self, host, port, user, pwd, db, vers=6):
        self.host = host
        self.port = int(port)
        self.user = user
        self.pwd = pwd
        self.db = db
        self.vers = vers

    def connect(self):
        sock = xmlrpclib.ServerProxy('%s:%s/xmlrpc/common' % (self.host, self.port))
        uid = sock.login(self.db, self.user, self.pwd)
        sock = xmlrpclib.ServerProxy('%s:%s/xmlrpc/object' % (self.host, self.port))

        self.uid = uid
        self.sock = sock

        return uid, sock

    def fetch(self, model, args=[], fields=[]):
        ids = self.sock.execute(self.db, self.uid, self.pwd, model, 'search', args)
        res = self.sock.execute(self.db, self.uid, self.pwd, model, 'read', ids, fields)

        return res

    def create(self, model, data, dryrun=False):
        if not dryrun:
            cid = self.sock.execute(self.db, self.uid, self.pwd, model, 'create', data)
            return cid

        return True
        
    def alter(self, data, change):
        altered = []
        for el in data:
            el[change['field']] = change['value']
            altered.append(el)
        
        return altered


class Partner():
    args = []
    fields = ['id', 'name', 'active', 'customer', 'supplier', 
              'lang', 'vat', 'ref', 'website',
              'mobile', 'phone', 'user_id']

    def __init__(self, odoo):
        self.odoo = odoo

    def get_all(self):
        return self.odoo.fetch('res.partner', args=self.args, fields=self.fields)


class Contact():
    args = []
    fields = ['id', 'function', 'fax', 'street2', 'street', 'phone', 'active',
              'city', 'name','mobile', 'lang','email','user_id',
              'country_id','partner_id', 'birthdate','customer', 'supplier',
              'state_id','contact_id', 'first_name', 'last_name']

    def __init__(self, odoo):
        self.odoo = odoo

    def get_by_partner_id(self, id):
        args = [('partner_id', '=', id)]
        return self.odoo.fetch('res.partner.contact', args=args, fields=self.fields)
    
