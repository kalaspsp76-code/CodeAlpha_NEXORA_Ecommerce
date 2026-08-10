from django.core.management.base import BaseCommand
from shop.models import Product
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Create demo products"
    def handle(self, *args, **kwargs):
        products = [
            ("Nova Wireless Headphones","Electronics","Premium wireless headphones with deep bass and long battery life.",2499,"https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"),
            ("Pulse Smart Watch","Electronics","Modern smartwatch with fitness tracking and notification support.",3999,"https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800"),
            ("Urban Classic Sneakers","Fashion","Comfortable everyday sneakers with a clean streetwear design.",2199,"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800"),
            ("Minimal Backpack","Fashion","Lightweight water-resistant backpack for college and work.",1799,"https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800"),
            ("Aero Desk Lamp","Home","Minimal LED desk lamp with adjustable brightness.",1299,"https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800"),
            ("Aura Coffee Mug","Home","Elegant ceramic mug for your daily coffee or tea.",599,"https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=800"),
        ]
        for name, category, description, price, image_url in products:
            Product.objects.update_or_create(
                slug=slugify(name),
                defaults={"name":name,"category":category,"description":description,
                          "price":price,"image_url":image_url,"stock":25}
            )
        self.stdout.write(self.style.SUCCESS("Demo products created successfully."))
