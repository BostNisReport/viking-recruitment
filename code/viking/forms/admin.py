from blanc_pages import block_admin
from models import *


block_admin.site.register(ContactFormBlock)
block_admin.site.register_block(ContactFormBlock, 'Forms')
block_admin.site.register(CadetApplicationFormBlock)
block_admin.site.register_block(CadetApplicationFormBlock, 'Forms')
block_admin.site.register(RequestQuoteFormBlock)
block_admin.site.register_block(RequestQuoteFormBlock, 'Forms')
