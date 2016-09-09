# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    View
)
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin

from ..attachment.models import Attachment
from ..base.choices import TICKET_STATUS
from ..base.notifications import (
    send_agent_ticket_creation_email,
    send_client_ticket_creation_email,
    send_client_ticket_closing_email,
    send_client_ticket_reopening_email,
    send_agent_comment_creation_email,
    send_client_comment_creation_email,
)
from ..base.utils import send_email
from ..comment.forms import CommentCreationForm
from ..comment.models import Comment
from ..ticket.models import Ticket

from .forms import TicketPropertiesForm, TicketCreationForm


class SuperuserRequiredExceptionMixin(LoginRequiredMixin, SuperuserRequiredMixin):
    raise_exception = True


class AdminHomeView(SuperuserRequiredExceptionMixin, ListView):
    context_object_name = 'ticket_list'
    model = Ticket
    paginate_by = 10

    template_name = 'support_tickets/admin/home.html'

    def get_queryset(self, **kwargs):

        status = self.request.GET.get('status', None)

        ticket = self.model.objects.all()

        if status is not None:
            if status == 'open':
                ticket = ticket.filter(
                    Q(status=TICKET_STATUS.open) |
                    Q(status=TICKET_STATUS.reopened)
                )

            if status == 'closed':
                ticket = ticket.exclude(status=TICKET_STATUS.open)
                ticket = ticket.exclude(status=TICKET_STATUS.reopened)

        ticket = ticket.prefetch_related("category")
        ticket = ticket.prefetch_related("agent")
        ticket = ticket.order_by('status', 'priority')

        return ticket


class AdminTicketCreateView(SuperuserRequiredExceptionMixin, SuccessMessageMixin, CreateView):
    form_class = TicketCreationForm
    template_name = 'support_tickets/admin/ticket/create.html'
    success_message = _('The ticket was successfully created')

    raise_exception = True

    def get_success_url(self):
        return reverse('tickets:admin_home')

    def form_valid(self, form):
        user = self.request.user

        # Save the ticket first, because a comment needs a ticket before it
        # can be saved.
        ticket = form['ticket'].save(commit=False)
        # Make sure the ticket has an agent
        if not ticket.agent:
            ticket.agent = user
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

        # Send emails to agent and submitter
        send_agent_ticket_creation_email(self.request, ticket)
        send_client_ticket_creation_email(self.request, ticket)

        return redirect(self.get_success_url())


class AdminTicketDetailView(SuperuserRequiredExceptionMixin, SuccessMessageMixin, FormMixin, DetailView):
    form_class = CommentCreationForm
    model = Ticket
    success_message = _('Your message was successfully sent')
    template_name = 'support_tickets/admin/ticket/view.html'

    def get_success_url(self):
        return reverse(
            'tickets:admin_ticket_detail',
            kwargs={'pk': self.object.pk}
        )

    def get_initial(self):
        return {
            'ticket': {
                'status': self.object.status
            },
        }

    def get_context_data(self, **kwargs):
        context = super(AdminTicketDetailView, self).get_context_data(**kwargs)

        # Comments
        comments = Comment.objects.filter(ticket=self.object)
        comments = comments.order_by('created')
        comments = comments.prefetch_related("user")
        comments = comments.prefetch_related("attachments")

        context['comments_list'] = comments

        # Comment form
        form = self.get_form()
        context['form'] = form

        # Ticket property form
        ticket_properties_form = TicketPropertiesForm(initial={
            'status': self.object.status,
            'category': self.object.category,
            'priority': self.object.priority,
            'agent': self.object.agent,
        })
        context['ticket_properties_form'] = ticket_properties_form

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

            # Send email to ticket's submitter & agent
            send_agent_comment_creation_email(request, self.object)
            send_client_comment_creation_email(request, self.object)

            return self.form_valid(form)

        else:
            return self.form_invalid(form)


class AdminTicketDeleteView(SuperuserRequiredExceptionMixin, SuccessMessageMixin, DeleteView):
    model = Ticket
    success_message = _('The ticket was successfully deleted')
    template_name = 'support_tickets/admin/ticket/delete.html'

    def get_success_url(self):
        return reverse('tickets:admin_home')


class AdminTicketCloseView(SuperuserRequiredExceptionMixin, SingleObjectMixin, View):
    model = Ticket
    success_message = _('The ticket was successfully closed')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.status != TICKET_STATUS.closed:
            self.object.status = TICKET_STATUS.closed
            self.object.save()

            # Send email to submitter
            send_client_ticket_closing_email(request, self.object)

            # Send success message
            messages.success(self.request, self.success_message)

        return redirect('tickets:admin_ticket_detail', pk=self.object.pk)

    def post(self, request, *args, **kwargs):
        return super(AdminTicketCloseView, self).get(request, *args, **kwargs)


class AdminTicketOpenView(SuperuserRequiredExceptionMixin, SingleObjectMixin, View):
    model = Ticket
    success_message = _('The ticket was successfully reopened')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.status != TICKET_STATUS.open and self.object.status != TICKET_STATUS.reopened:
            self.object.status = TICKET_STATUS.reopened
            self.object.save()

            # Send email to submitter
            send_client_ticket_reopening_email(request, self.object)

            # Send success message
            messages.success(self.request, self.success_message)

        return redirect('tickets:admin_ticket_detail', pk=self.object.pk)

    def post(self, request, *args, **kwargs):
        return super(AdminTicketCloseView, self).get(request, *args, **kwargs)


class AdminTicketPropertiesUpdateView(SuperuserRequiredExceptionMixin, SuccessMessageMixin, FormMixin, SingleObjectMixin, View):
    form_class = TicketPropertiesForm
    model = Ticket
    success_message = _('Your changes were successfully saved.')

    def get_success_url(self):
        return reverse(
            'tickets:admin_ticket_detail',
            kwargs={'pk': self.object.pk}
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect('tickets:admin_ticket_detail', pk=self.object.pk)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()

        if form.is_valid():
            # Update last active field
            self.object.last_active = timezone.now()

            # Update category
            self.object.category = form.cleaned_data['category']

            # Update Agent
            self.object.agent = form.cleaned_data['agent']

            # Update Status
            self.object.status = form.cleaned_data['status']

            if self.object.status == TICKET_STATUS.closed:
                send_client_ticket_closing_email(request, self.object)

            if self.object.status == TICKET_STATUS.reopened:
                send_client_ticket_reopening_email(request, self.object)

            # Update Priority
            self.object.priority = form.cleaned_data['priority']

            # Save object
            self.object.save()

            return self.form_valid(form)

        else:
            return self.form_invalid(form)
