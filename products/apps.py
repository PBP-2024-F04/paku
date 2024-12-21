from django.apps import AppConfig
from django.db.models.signals import post_migrate
import json
from django.conf import settings
from pathlib import Path

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        post_migrate.connect(load_initial_data, sender=self)

def load_initial_data(sender, **kwargs):
    from products.models import Product
    
    try:
        dataset_path = Path(settings.BASE_DIR) / 'dataset_paku.json'
        
        # Membaca file JSON
        with open(dataset_path, 'r') as file:
            data = json.load(file)

            for item in data:
                fields = item['fields']
                products = Product.objects.filter(product_name = fields['product_name'])

                if products.count() > 0 :
                    for productDuplicate in products:
                        productDuplicate.restaurant=fields['restaurant']
                        productDuplicate.price=fields['price']
                        productDuplicate.description=fields['description']
                        productDuplicate.category=fields['category']
                        productDuplicate.product_image=fields.get('product_image', '')

                        productDuplicate.save()
                else :
                    product = Product(
                    product_name=fields['product_name'],
                    restaurant=fields['restaurant'],
                    price=fields['price'],
                    description=fields['description'],
                    category=fields['category'],
                    product_image=fields.get('product_image', '')
                    ).save()
    except Exception as e:
        print(f"Error loading initial data: {e}")