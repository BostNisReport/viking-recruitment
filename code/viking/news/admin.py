from django.contrib import admin
from blanc_pages import block_admin
from models import *



block_admin.site.register(LatestNewsPostsBlock)
block_admin.site.register_block(LatestNewsPostsBlock, 'Viking Recruitment')
