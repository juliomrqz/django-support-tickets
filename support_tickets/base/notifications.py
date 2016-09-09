# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext as _

from utils import send_email


def send_agent_ticket_creation_email(request, ticket):
    if ticket.agent != request.user:
        send_email(
            request,
            _("New ticket created"),
            ticket.agent.email,
            settings.DEFAULT_FROM_EMAIL,
            {
                'ticket': ticket,
                'agent': ticket.agent
            },
            'support_tickets/email/new_ticket_agent.txt',
            'support_tickets/email/new_ticket_agent.html'
        )


def send_client_ticket_creation_email(request, ticket):
    send_email(
        request,
        _("New ticket created"),
        ticket.agent.email,
        settings.DEFAULT_FROM_EMAIL,
        {
            'ticket': ticket,
            'submitter': ticket.submitter
        },
        'support_tickets/email/new_ticket_submitter.txt',
        'support_tickets/email/new_ticket_submitter.html'
    )


def send_client_ticket_closing_email(request, ticket):
    send_email(
        request,
        _("Your ticket #%s was closed") % (ticket.pk),
        ticket.agent.email,
        settings.DEFAULT_FROM_EMAIL,
        {
            'ticket': ticket,
            'submitter': ticket.submitter
        },
        'support_tickets/email/closed_ticket_submitter.txt',
        'support_tickets/email/closed_ticket_submitter.html'
    )


def send_client_ticket_reopening_email(request, ticket):
    send_email(
        request,
        _("Your ticket #%s was reopen") % (ticket.pk),
        ticket.agent.email,
        settings.DEFAULT_FROM_EMAIL,
        {
            'ticket': ticket,
            'submitter': ticket.submitter
        },
        'support_tickets/email/reopen_ticket_submitter.txt',
        'support_tickets/email/reopen_ticket_submitter.html'
    )


def send_agent_comment_creation_email(request, ticket):
    send_email(
        request,
        _("New comment created"),
        ticket.agent.email,
        settings.DEFAULT_FROM_EMAIL,
        {
            'ticket': ticket,
            'submitter': ticket.submitter
        },
        'support_tickets/email/new_comment_submitter.txt',
        'support_tickets/email/new_comment_submitter.html'
    )


def send_client_comment_creation_email(request, ticket):
    if ticket.agent:
        if ticket.agent != request.user:
            send_email(
                request,
                "New comment created",
                ticket.agent.email,
                settings.DEFAULT_FROM_EMAIL,
                {
                    'ticket': ticket,
                    'agent': ticket.agent
                },
                'support_tickets/email/new_comment_agent.txt',
                'support_tickets/email/new_comment_agent.html'
            )
