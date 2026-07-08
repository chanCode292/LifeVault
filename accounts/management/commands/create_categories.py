from django.core.management.base import BaseCommand
from accounts.models import DocCategory


class Command(BaseCommand):
    help = 'Create default document categories for LifeVault'

    def handle(self, *args, **options):
        categories_data = [
            {
                'cat_name': 'Government IDs',
                'description': 'Government identification documents such as passport, driver\'s license, national ID'
            },
            {
                'cat_name': 'Certificates',
                'description': 'Education certificates, professional certifications, and diplomas'
            },
            {
                'cat_name': 'School Records',
                'description': 'School transcripts, mark sheets, admission letters'
            },
            {
                'cat_name': 'Medical Records',
                'description': 'Medical prescriptions, vaccination records, health checkups'
            },
            {
                'cat_name': 'Financial Documents',
                'description': 'Bank statements, investment papers, tax documents, insurance policies'
            },
            {
                'cat_name': 'Receipts',
                'description': 'Purchase receipts, warranties, invoices'
            },
            {
                'cat_name': 'Contracts',
                'description': 'Legal contracts, agreements, lease documents'
            },
            {
                'cat_name': 'Others',
                'description': 'Miscellaneous documents'
            },
        ]

        created_count = 0
        for cat_data in categories_data:
            category, created = DocCategory.objects.get_or_create(
                cat_name=cat_data['cat_name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {category.cat_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⊘ Already exists: {category.cat_name}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Total categories created: {created_count}'))
