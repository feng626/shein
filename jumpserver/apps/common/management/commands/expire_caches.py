from assets.signal_handlers.node_assets_mapping import expire_node_assets_mapping as _expire_node_assets_mapping
from django.core.management.base import BaseCommand

from orgs.models import Organization


def expire_node_assets_mapping():
    org_ids = Organization.objects.all().values_list('id', flat=True)
    org_ids = [*org_ids, '00000000-0000-0000-0000-000000000000']

    for org_id in org_ids:
        _expire_node_assets_mapping(org_ids=(org_id,))


class Command(BaseCommand):
    help = 'Expire caches'

    def handle(self, *args, **options):
        expire_node_assets_mapping()
