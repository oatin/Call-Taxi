from django.shortcuts import render
from django.db.models import Count, Sum
from login.models import *
from home.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models.functions import TruncMonth,TruncDate

# @login_required
def dashboard(request):
    now = timezone.now()
    total_value = Ride.objects.filter(status='completed').aggregate(Sum('fare'))['fare__sum'] or 0
    total_users = CustomUser.objects.count()
    total_Jobs = Ride.objects.count()
    total_tickets = Ride.objects.filter(status='requested').count()
    
    last_month = now - timezone.timedelta(days=30)
    
    monthly_data = Ride.objects.annotate(month=TruncMonth('request_time')).values('month').annotate(count=Count('id')).order_by('month')
    
    user_types = CustomUser.objects.values('role').annotate(count=Count('id'))
    
    active_users = CustomUser.objects.filter(last_login__gte=now - timezone.timedelta(minutes=15)).count()
    
    line_chart_data = Ride.objects.annotate(date=TruncDate('request_time')).values('date').annotate(count=Count('id')).order_by('date')[:30]
    
    formatted_monthly_data = [
        {'month': entry['month'].strftime('%Y-%m'), 'count': entry['count']}
        for entry in monthly_data
    ]
    formatted_line_chart_data = [
        {'date': entry['date'].strftime('%Y-%m-%d'), 'count': entry['count']}
        for entry in line_chart_data
    ]
    
    context = {
        'total_value': total_value,
        'total_users': total_users,
        'total_Jobs': total_Jobs,
        'total_tickets': total_tickets,
        'monthly_data': formatted_monthly_data,
        'user_types': list(user_types),
        'active_users': active_users,
        'line_chart_data': formatted_line_chart_data,
    }
    
    return render(request, 'customadmin/dashboard.html', context)