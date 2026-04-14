# Generated manually 2026-04-14 (v2)
# Uses SeparateDatabaseAndState for fields that may already exist in DB

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        # 1. Update role choices and default (safe — only metadata)
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[
                    ('admin',    'Администратор'),
                    ('operator', 'Оператор'),
                    ('analyst',  'Аналитик'),
                    ('viewer',   'Наблюдатель'),
                ],
                default='viewer',
                max_length=20,
                verbose_name='Роль',
            ),
        ),

        # 2. Fix keycloak_id
        migrations.AlterField(
            model_name='user',
            name='keycloak_id',
            field=models.CharField(
                blank=True,
                max_length=100,
                verbose_name='Keycloak ID',
            ),
        ),

        # 3. auth_token — update Django state only, skip SQL (column already exists in DB)
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='user',
                    name='auth_token',
                    field=models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name='Auth Token',
                    ),
                ),
            ],
        ),

        # 4. avatar — update Django state only, skip SQL (column already exists in DB)
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='user',
                    name='avatar',
                    field=models.ImageField(
                        blank=True,
                        null=True,
                        upload_to='avatars/',
                        verbose_name='Аватарка',
                    ),
                ),
            ],
        ),

        # 5. Remove created_at
        migrations.RemoveField(
            model_name='user',
            name='created_at',
        ),

        # 6. Remove updated_at
        migrations.RemoveField(
            model_name='user',
            name='updated_at',
        ),

        # 7. Update model options
        migrations.AlterModelOptions(
            name='user',
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
