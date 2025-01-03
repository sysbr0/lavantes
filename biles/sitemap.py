from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import MainProduct

class MainProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Return all MainProduct instances
        return MainProduct.objects.all()

    def location(self, obj):
        # Generate the URL for each MainProduct instance
        return reverse('fatch_Product', kwargs={
            'id': obj.pk  # Adjust to use 'id' to match the URL pattern
        })

    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page, site, protocol)
        for url in urls:
            obj = url['item']  # Get the product object for each URL
            # Add the product name as the title
            url['title'] = obj.product_name
        return urls
