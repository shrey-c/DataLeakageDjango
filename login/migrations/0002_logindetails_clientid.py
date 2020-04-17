
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logindetails',
            name='clientid',
            field=models.CharField(default='xyz', max_length=17),
        ),
    ]
