import json

from django.shortcuts import render, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.auth_logs.models import UserAuthLog


@superuser_required
def auth_log_detail_view(request, log_id):
    log = get_object_or_404(UserAuthLog, id=log_id)
    log_data = {
        'id': log.id,
        'profile': {
            'id': log.user.id,
            'full_name': log.user.full_name,
            'email': log.user.email
        },
        'ip': log.ip,
        'timestamp': log.timestamp.isoformat(),
        'user_agent': log.user_agent,
        'location': {
            'country': log.country,
            'country_code': log.country_code,
            'region': log.region,
            'region_name': log.region_name,
            'city': log.city,
            'zip_code': log.zip_code,
            'coordinates': {
                'latitude': log.latitude,
                'longitude': log.longitude
            },
            'timezone': log.timezone
        },
        'network': {
            'isp': log.isp,
            'organization': log.organization,
            'as_number': log.as_number
        },
        'security': {
            'is_mobile': log.is_mobile,
            'is_proxy': log.is_proxy,
            'is_hosting': log.is_hosting
        }
    }

    log_data_json = json.dumps(log_data, indent=2, ensure_ascii=False)

    context = {
        'log': log,
        'log_data_json': log_data_json,
    }
    return render(request, 'admin_panel/users/user_auth_log_detail.html', context)
