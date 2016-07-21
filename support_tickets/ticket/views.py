# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import (
    CreateView,
    DetailView,
    ListView
)
from django.views.generic.edit import FormMixin

from braces.views import LoginRequiredMixin, UserPassesTestMixin

from ..attachment.models import Attachment
from ..base.choices import TICKET_STATUS
from ..base.utils import send_email
from ..comment.forms import CommentCreationForm
from ..comment.models import Comment

from .forms import TicketCreationForm
from .models import Ticket


class TicketCreateView(LoginRequiredMixin, CreateView):
    form_class = TicketCreationForm
    template_name = 'support_tickets/ticket/create.html'
    success_message = _('The ticket was successfully created')

    def get_success_url(self):
        return reverse('tickets:ticket_list')

    def form_valid(self, form):
        user = self.request.user

        # Save the ticket first, because a comment needs a ticket before it
        # can be saved.
        ticket = form['ticket'].save(commit=False)
        ticket.submitter = user
        ticket.save()

        # Save comment
        comment = form['comment'].save(commit=False)
        comment.user = user
        comment.ticket = ticket
        comment.save()

        # Save attachments
        for each in form['attachments'].cleaned_data['attachments']:
            Attachment.objects.create(
                file=each,
                comment=comment,
                uploader=user
            )

        # Send success message
        messages.success(self.request, self.success_message)

        # TODO: Send emails to agent and submitter
        self.send_agent_email(ticket)
        self.send_submitter_email(ticket)

        return redirect(self.get_success_url())

    def send_agent_email(self, ticket):
        if ticket.agent:
            print('[ticket created] Message to agent')

    def send_submitter_email(self, ticket):
        print('[ticket created] Message to submitter')


class TicketListView(LoginRequiredMixin, ListView):
    context_object_name = 'ticket_list'
    model = Ticket
    paginate_by = 10

    template_name = 'support_tickets/ticket/list.html'

    def get_queryset(self, **kwargs):
        ticket = self.model.objects.filter(submitter=self.request.user)
        ticket = ticket.prefetch_related("category")
        ticket = ticket.prefetch_related("agent")
        ticket = ticket.order_by('status', 'priority')

        return ticket


class TicketDetailView(UserPassesTestMixin, SuccessMessageMixin, FormMixin, DetailView):
    form_class = CommentCreationForm
    model = Ticket
    success_message = _('Your message was successfully sent')
    template_name = 'support_tickets/ticket/view.html'

    raise_exception = True
    redirect_unauthenticated_users = True

    def test_func(self, user):
        ticket = self.get_object()

        # Cannot view ticket if the current user is not the submitter or the
        # agent
        if self.request.user.is_superuser:
            return True
        elif ticket.agent != self.request.user and ticket.submitter != self.request.user:
            return False

        return True

    def get_success_url(self):
        return reverse(
            'tickets:ticket_detail',
            kwargs={'pk': self.object.pk}
        )

    def get_initial(self):
        return {
            'ticket': {
                'status': self.object.status
            },
        }

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)

        # Comments
        comments = Comment.objects.filter(ticket=self.object)
        comments = comments.order_by('created')
        comments = comments.prefetch_related("user")
        comments = comments.prefetch_related("attachments")

        context['comments_list'] = comments

        # Comment form
        form = self.get_form()
        context['form'] = form

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Raise denied permission if ticket is closed
        if self.object.status == TICKET_STATUS.closed:
            raise PermissionDenied

        form = self.get_form()

        if form.is_valid():
            # Update last active field
            self.object.last_active = timezone.now()
            self.object.save()

            # Save comment
            comment = form['comment'].save(commit=False)
            comment.user = request.user
            comment.ticket = self.object
            comment.save()

            # Save attachments
            for each in form['attachments'].cleaned_data['attachments']:
                Attachment.objects.create(
                    file=each,
                    comment=comment,
                    uploader=request.user
                )

            # TODO: Send emails to agent and submitter
            self.send_agent_email(comment, self.object)
            self.send_submitter_email(comment, self.object)

            # Send success message
            messages.success(self.request, self.success_message)

            return self.form_valid(form)

        else:
            return self.form_invalid(form)

    def send_agent_email(self, comment, ticket):
        if ticket.agent:
            if ticket.agent != comment.user:
                send_email(
                    self.request,
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

    def send_submitter_email(self, comment, ticket):
        pass
