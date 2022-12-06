from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta

from .models import PostCategory, Post, Category


@shared_task
def send_notifications(preview, pk, title, subscribers, id):
    mailing_list = list(PostCategory.objects.filter(post_through_id=id).values_list(
        'category_through__subscribers__username',
        'category_through__subscribers__first_name',
        'category_through__subscribers__email',
        'category_through__name_category',
        )
    )

    for user, first_name, email, category in mailing_list:
        if not first_name:
            first_name = user

        html_content = render_to_string(
            'new_created_email.html',
            {
                'name': first_name,
                'category': category,
                'title': title,
                'text': preview,
                'link': f'{settings.SITE_URL}/news/{pk}',
            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers,
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def notify_weekly():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(date_creation__gte=last_week)
    categories = set(posts.values_list('post_category__name_category', flat=True))
    subscribers = set(Category.objects.filter(name_category__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='All publications from the last week',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
