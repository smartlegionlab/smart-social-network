from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from apps.reports.forms import UserReportForm
from apps.reports.models import UserReport
from apps.users.models import User


@login_required
def user_report_view(request, username):
    reported_user = request.user if username is None else get_object_or_404(User, username=username)

    if request.user.id == reported_user.id:
        messages.error(request, "You cannot file a complaint against yourself!")
        return redirect('users:current_user')

    if UserReport.objects.filter(
            reporter=request.user,
            reported_user_id=reported_user.id,
            status__in=['submitted', 'in_progress']
    ).exists():
        messages.error(request, 'You already have an active report for this user.')
        return redirect('users:current_user')

    if request.method == 'POST':
        report_form = UserReportForm(request.POST, request.FILES)
        if report_form.is_valid():
            report = report_form.save(commit=False)
            report.reporter_id = request.user.id
            report.reported_user_id = reported_user.id
            report.status = 'submitted'
            try:
                report.save()
                messages.success(request, 'Report submitted successfully. Thank you!')
                return redirect('users:current_user')
            except IntegrityError:
                messages.error(request, 'You already have an active report for this user.')
                return redirect('users:current_user')
    else:
        report_form = UserReportForm()

    context = {
        'form': report_form,
        'active_page': 'report',
        'reported_user': reported_user
    }

    return render(request, 'reports/user_report.html', context)
