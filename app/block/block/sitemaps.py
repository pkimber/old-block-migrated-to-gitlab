#TBUSHELL sitemap instance
from django.contrib.sitemaps import Sitemap
from block.models import Page
from django.utils import timezone

class SiteMapName(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        #return ['test1','test2','test3']
        pgs = Page.objects.all().order_by('order')
        return pgs

    def lastmod(self,obj):
        #return timezone.now()
        return obj.modified

    def location(self,obj):
        #return '/'
        #return '/'+obj+'/'
        return obj.get_absolute_url()
