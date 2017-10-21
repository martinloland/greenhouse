from ..models import SystemStatus


def system_active(request):
    status = SystemStatus.objects.get().report
    return {'system_status': status['ok'],
            'system_message': status['message'],
            'system_free_space':status['free_space']}
