from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Removes all news from any category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        categories = Category.objects.all()
        category_list = list(categories.values())
        find_category = [category['name_category'] for category in category_list]

        if options["category"] in find_category:
            self.stdout.write(f'Do you really want to delete all posts in category {options["category"]} ? yes/no')
            answer = input()

            if answer == 'yes':
                category = Category.objects.get(name_category=options['category'])
                Post.objects.filter(post_category=category).delete()
                self.stdout.write(self.style.SUCCESS(
                    f'All posts in category {category.name_category} removed successfully'))
            else:
                self.stdout.write(self.style.ERROR('Canceled'))

        else:
            self.stdout.write(self.style.ERROR(f'Не удалось найти категорию {options["category"]}'))

        return
