from blanc_pages import block_admin

from .models import (
    LargeBannerBlock, LatestTweetsBlock, RelatedLink, RelatedLinkListBlock, SmallBannerBlock)


class RelatedLinkInline(block_admin.StackedInline):
    model = RelatedLink
    extra = 1


class RelatedLinkListBlockAdmin(block_admin.BlockModelAdmin):
    inlines = [RelatedLinkInline]


block_admin.site.register((SmallBannerBlock, LargeBannerBlock, LatestTweetsBlock))
block_admin.site.register_block(SmallBannerBlock, 'Common')
block_admin.site.register_block(LargeBannerBlock, 'Common')
block_admin.site.register_block(LatestTweetsBlock, 'Viking Recruitment')
block_admin.site.register(RelatedLinkListBlock, RelatedLinkListBlockAdmin)
block_admin.site.register_block(RelatedLinkListBlock, 'Viking Recruitment')
