# Generated by Django 4.1.13 on 2025-03-02 13:46

import authentication.models.access_key
import common.db.fields
import common.db.models
import common.db.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models.user._auth
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TempToken',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=128, verbose_name='Username')),
                ('secret', models.CharField(max_length=64, verbose_name='Secret')),
                ('verified', models.BooleanField(default=False, verbose_name='Verified')),
                ('date_verified', models.DateTimeField(null=True, verbose_name='Date verified')),
                ('date_expired', models.DateTimeField(verbose_name='Date expired')),
            ],
            options={
                'verbose_name': 'Temporary token',
            },
        ),
        migrations.CreateModel(
            name='SSOToken',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('authkey', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Token')),
                ('expired', models.BooleanField(default=False, verbose_name='Expired')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=common.db.models.CASCADE_SIGNAL_SKIP, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'SSO token',
            },
        ),
        migrations.CreateModel(
            name='SSHKey',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('private_key', common.db.fields.EncryptTextField(blank=True, null=True, verbose_name='Private key')),
                ('public_key', common.db.fields.EncryptTextField(blank=True, null=True, verbose_name='Public key')),
                ('date_last_used', models.DateTimeField(blank=True, null=True, verbose_name='Date last used')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=common.db.models.CASCADE_SIGNAL_SKIP, related_name='ssh_keys', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'SSH key',
            },
            bases=(models.Model, users.models.user._auth.AuthMixin),
        ),
        migrations.CreateModel(
            name='PrivateToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('date_last_used', models.DateTimeField(blank=True, null=True, verbose_name='Date last used')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Private Token',
            },
        ),
        migrations.CreateModel(
            name='Passkey',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Enabled')),
                ('platform', models.CharField(default='', max_length=255, verbose_name='Platform')),
                ('added_on', models.DateTimeField(auto_now_add=True, verbose_name='Added on')),
                ('date_last_used', models.DateTimeField(default=None, null=True, verbose_name='Date last used')),
                ('credential_id', models.CharField(max_length=255, unique=True, verbose_name='Credential ID')),
                ('token', models.CharField(max_length=1024, verbose_name='Token')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccessKey',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='AccessKeyID')),
                ('secret', models.CharField(default=authentication.models.access_key.default_secret, max_length=36, verbose_name='AccessKeySecret')),
                ('ip_group', models.JSONField(default=common.db.utils.default_ip_group, verbose_name='IP group')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('date_last_used', models.DateTimeField(blank=True, null=True, verbose_name='Date last used')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=common.db.models.CASCADE_SIGNAL_SKIP, related_name='access_keys', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Access key',
            },
        ),
    ]
