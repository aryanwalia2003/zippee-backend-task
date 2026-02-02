from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_add_email_to_users'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE app_users ADD COLUMN role VARCHAR(20) DEFAULT 'user';",
            reverse_sql="ALTER TABLE app_users DROP COLUMN role;"
        )
    ]
