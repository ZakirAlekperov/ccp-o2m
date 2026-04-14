# Generated manually 2026-04-14
# Syncs users.User model with 0001_initial:
#   - role choices: old (superuser/planner/external_operator) -> new (operator/analyst/viewer)
#   - default role: external_operator -> viewer
#   - keycloak_id: unique/null=True -> blank=True (not unique, not null)
#   - add auth_token field
#   - add avatar field
#   - remove created_at / updated_at (not in new model)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        # 1. Update role choices and default
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

        # 2. Fix keycloak_id: remove unique constraint, remove null, keep blank
        migrations.AlterField(
            model_name='user',
            name='keycloak_id',
            field=models.CharField(
                blank=True,
                max_length=100,
                verbose_name='Keycloak ID',
            ),
        ),

        # 3. Add auth_token field
        migrations.AddField(
            model_name='user',
            name='auth_token',
            field=models.CharField(
                blank=True,
                max_length=100,
                verbose_name='Auth Token',
            ),
        ),

        # 4. Add avatar field
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

        # 5. Remove created_at (not in new model)
        migrations.RemoveField(
            model_name='user',
            name='created_at',
        ),

        # 6. Remove updated_at (not in new model)
        migrations.RemoveField(
            model_name='user',
            name='updated_at',
        ),

        # 7. Update model ordering (remove -created_at)
        migrations.AlterModelOptions(
            name='user',
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
