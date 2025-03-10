# Generated by Django 5.0.6 on 2024-08-30 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0010_rename_discount_price_new_product_discount_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_topic', models.TextField()),
                ('main_body_first', models.TextField()),
                ('main_body_sec', models.TextField()),
                ('main_body_third', models.TextField()),
                ('main_blockquote', models.TextField()),
                ('sub_topic_first', models.TextField()),
                ('sub_content_first', models.TextField()),
                ('article_tags', models.TextField()),
                ('article_category', models.CharField(choices=[('Clothing', 'Clothing'), ('Footwear', 'Footwear'), ('Accessories', 'Accessories'), ('Jewellery', 'Jewellery')], max_length=20)),
                ('author', models.CharField(max_length=7)),
                ('main_img', models.ImageField(blank=True, upload_to='static/blog_images')),
                ('sub_img', models.ImageField(blank=True, upload_to='static/blog_images')),
            ],
        ),
    ]
