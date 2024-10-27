from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        post_migrate.connect(load_initial_data, sender=self)

def load_initial_data(sender, **kwargs):
    from products.models import Product
    try:
        if not Product.objects.exists():
            print("Loading initial data from dataset_paku.json...")
            call_command('loaddata', 'dataset_paku.json')
    except Exception as e:
        print(f"Error loading initial data: {e}")