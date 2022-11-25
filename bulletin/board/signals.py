from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from .models import Reaction
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Reaction)
def reaction_mail(sender, instance, **kwargs):
    html_content = render_to_string(
        'reaction_mail.html',
        {
            'reaction': instance,
        }
    )

    if instance.accepted:
        subject = f'Ваш отклик на объявление{instance.announce.heading} принят'
    else:
        subject = f'Вы оставили отклик на объявление{instance.announce.heading}'

    msg = EmailMultiAlternatives(
        subject=subject,
        body=instance.content,
        from_email='garamet01@gmail.com',
        to=[instance.author.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
