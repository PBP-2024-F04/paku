from django.apps import AppConfig
from django.db.utils import OperationalError


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        from django.core.management import call_command
        from products.models import Product

        try:
            if not Product.objects.exists():
                print("Loading initial data from dataset_paku.json...")
                call_command('loaddata', 'dataset_paku.json')
        except OperationalError:
            pass