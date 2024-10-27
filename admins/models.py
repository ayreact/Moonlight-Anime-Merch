from django.db import models

category_choice = [
    ('Clothing', 'Clothing'),
    ('Footwear', 'Footwear'),
    ('Accessories', 'Accessories'),
    ('Jewellery', 'Jewellery')
]

#Products
class new_product(models.Model):
    product_name = models.CharField(max_length=40)
    product_price = models.FloatField()
    discount_value = models.IntegerField(default=0)
    actual_prod_price = models.FloatField(default=0)
    product_desc = models.TextField()
    product_quantity = models.IntegerField(default=0)
    product_rating = models.IntegerField(default=5)
    product_img = models.ImageField(upload_to="static/product_images", blank=True)
    product_category = models.CharField(
        max_length=20,
        choices=category_choice
    )
    
    def __str__(self):
        return self.product_name

#Team
class team(models.Model):
    name = models.CharField(max_length=30)
    position = models.TextField()
    email = models.CharField(max_length=40)
    user_img = models.ImageField(upload_to="static/team_images", blank=True)
    whatsapp = models.CharField(max_length=20)
    instagram = models.TextField()
    twitter = models.TextField()
    phone_number = models.CharField(max_length=20)
    user_cover = models.ImageField(upload_to="static/team_images", blank=True)
    
    def __str__(self):
        return self.name

#Blog
class blog(models.Model):
    main_topic = models.TextField()
    main_body_first = models.TextField()
    main_body_sec = models.TextField()
    main_body_third = models.TextField()
    main_blockquote = models.TextField()
    sub_topic_first = models.TextField()
    sub_content_first = models.TextField()
    sub_topic_sec = models.TextField(default="")
    sub_content_sec = models.TextField(default="")
    article_tags = models.TextField()
    article_category = models.CharField(
        max_length=20,
        choices=category_choice
    )
    author = models.CharField(max_length=7)
    main_img = models.ImageField(upload_to="static/blog_images", blank=True)
    sub_img = models.ImageField(upload_to="static/blog_images", blank=True)
    
    def __str__(self):
        return self.main_topic
  
#Tasks
class New_task(models.Model):
    new_task = models.TextField()
    
    def __str__(self):
        return self.new_task