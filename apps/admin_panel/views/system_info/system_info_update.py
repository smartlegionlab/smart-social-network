from django.http import JsonResponse
from django.views.decorators.http import require_GET

from apps.admin_panel.decorators.superuser import superuser_required
from apps.core.utils.informers.system import SystemInfoMaster


@superuser_required
@require_GET
def system_info_update_view(request):
    master = SystemInfoMaster()
    data = {
        'boot_time': master.info.boot_time_str,
        'cpu_count': master.cpu.count,
        'cpu_count_real': master.cpu.count_real,
        'cpu_percent': master.cpu.percent_str,
        'memory_total': master.memory.total_str,
        'memory_available': master.memory.available_str,
        'memory_free': master.memory.free_str,
        'memory_used': master.memory.used_str,
        'memory_percent': master.memory.percent_str,
        'disk_data': master.disk.system_usage,
    }
    return JsonResponse(data)
