"""Remove legacy EmailUser from migration state without dropping its table.

Existing installations may have adopted django_boost_emailuser as the physical
table for an application-owned user model. Never delete that table.
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("django_boost", "0003_alter_emailuser_first_name"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[migrations.DeleteModel(name="EmailUser")],
        ),
    ]
