from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("issues", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="issue",
            options={"ordering": ["-created_at"]},
        ),
    ]
