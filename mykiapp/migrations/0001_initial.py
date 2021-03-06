# Generated by Django 2.2.10 on 2020-03-02 12:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('name', models.CharField(max_length=40)),
                ('employees', models.ManyToManyField(related_name='teams', to='mykiapp.Employee')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('items', models.ManyToManyField(to='mykiapp.Item')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TeamItemAccess',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('access_level', models.IntegerField(choices=[(1, 'ADMIN'), (2, 'STANDARD')], default=2)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mykiapp.Item')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='mykiapp.Team')),
            ],
            options={
                'unique_together': {('team', 'item')},
            },
        ),
        migrations.CreateModel(
            name='TeamFolderAccess',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('access_level', models.IntegerField(choices=[(1, 'ADMIN'), (2, 'STANDARD')], default=2)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mykiapp.Folder')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folders', to='mykiapp.Team')),
            ],
            options={
                'unique_together': {('team', 'folder')},
            },
        ),
        migrations.CreateModel(
            name='EmployeeItemAccess',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('access_level', models.IntegerField(choices=[(1, 'ADMIN'), (2, 'STANDARD')], default=2)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='mykiapp.Employee')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mykiapp.Item')),
            ],
            options={
                'unique_together': {('employee', 'item')},
            },
        ),
        migrations.CreateModel(
            name='EmployeeFolderAccess',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('access_level', models.IntegerField(choices=[(1, 'ADMIN'), (2, 'STANDARD')], default=2)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folders', to='mykiapp.Employee')),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mykiapp.Folder')),
            ],
            options={
                'unique_together': {('employee', 'folder')},
            },
        ),
    ]
