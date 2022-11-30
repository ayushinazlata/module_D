from allauth.account.signals import user_signed_up
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory


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


@receiver(m2m_changed, sender=PostCategory,)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers, instance.id)



