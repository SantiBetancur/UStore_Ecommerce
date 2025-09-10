import factory
from .models import Product
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    name = factory.Faker('company')
    price = factory.Faker('random_int', min=1000, max=100000)
    image = factory.django.ImageField(filename='default.png')
    description = factory.Faker('text', max_nb_chars=100)
    category = factory.Faker('random_element', elements=('Electronics', 'Clothing&Accessories', 'Academic', 'Food', 'Other'))
    type = factory.Faker('random_element', elements=('product', 'service'))
    created_at = factory.Faker('date_time')
    updated_at = factory.Faker('date_time')
