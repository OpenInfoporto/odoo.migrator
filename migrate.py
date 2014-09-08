from lib import *
import ConfigParser


Config = ConfigParser.ConfigParser()
Config.read("config.ini")


def init():
    logging.info('connecting to source...')
    src = Odoo(Config.get('source', 'host'),
               Config.get('source', 'port'),
               Config.get('source', 'user'),
               Config.get('source', 'pwd'),
               Config.get('source', 'db'))

    logging.info('connecting to destination...')
    dst = Odoo(Config.get('destination', 'host'),
               Config.get('destination', 'port'),
               Config.get('destination', 'user'),
               Config.get('destination', 'pwd'),
               Config.get('destination', 'db'))

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
            src_contacts = src.alter(src_contacts, dict(field='partner_id', value=cid))
            for c in src_contacts:
                src.create('res.partner.contact', c)
            
