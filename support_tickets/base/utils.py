from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


def send_email(request, subject, to, from_email, ctx, txt_template, html_template):

    # update ctx
    ctx.update({'website_domain': get_current_site(request).domain})

    # define text and HTML content
    text_content = get_template(txt_template).render(Context(ctx))
    html_content = get_template(html_template).render(Context(ctx))

    # Define email message objects
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
