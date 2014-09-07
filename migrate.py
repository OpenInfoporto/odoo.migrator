from lib import *

def init():
    logging.info('connecting to source...')
    src = Odoo('http://shepherd.infoporto.it','8069','admin',
               '1nf0p0rt0','openerp.infoporto.it')

    logging.info('connecting to destination...')
    dst = Odoo('http://heisenberg.infoporto.it','8069','admin',
               '1nf0p0rt0','openerpinfoporto')

    return src, dst


if __name__ == "__main__":
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG)
    
    logging.info('Migration startup')

    src, dst = init()
    src_uid, src_sock = src.connect()
    dst_uid, dst_sock = dst.connect()

    model = sys.argv[1]
    logging.info('Migration will run for %s ...' % model)
    
    if model == 'res.partner':
        
        logging.info('* Fetching source partners ... ')
        src_partners = Partner(src).get_all()
        logging.info('* %s partners found. ' % len(src_partners))
        
        logging.info('* Creating partners on destination.')
        for p in src_partners:
            logging.info('** Creating %s with ID %s ... ' % (p['name'], p['id']))
            cid = dst.create('res.partner', p, dryrun=True)

            logging.info('** Fetching source contacts for %s ...' % p['name'])
            src_contacts = Contact(src).get_by_partner_id(p['id'])
            logging.info('** %s contacts found. ' % len(src_contacts))

            #src_contacts.create()
            
