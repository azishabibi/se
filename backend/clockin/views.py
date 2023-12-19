from django.http import JsonResponse
from clockin.models import OrthodonticCheckIn
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from user.models import User
import json
import numpy as np
from django.utils import timezone
import pytz
from datetime import timedelta,datetime
# Set the desired timezone (Asia/Shanghai for Beijing time)
beijing_tz = pytz.timezone('Asia/Shanghai')
timezone.activate(beijing_tz)

#@login_required
@csrf_exempt
def orthodontic_check_in(request):
    if request.method == 'POST':
        if not request.body:
            return JsonResponse({'error': 'Empty request body'}, status=400)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': str(e)}, status=400)

        user_id = data.get('user_id')
        if user_id is None:
            return JsonResponse({'error': 'Missing user_id'}, status=400)
        
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        check_in_type = data.get('check_in_type')
        if check_in_type not in ['on', 'off']:
            return JsonResponse({'error': 'Invalid check-in type'}, status=400)
        #import pdb;pdb.set_trace()
        if check_in_type == 'on':
            last_off_checkin = OrthodonticCheckIn.objects.filter(
                user=user, check_in_type='off'
            ).order_by('-date').first()

            if last_off_checkin:
                duration_since_last_off = datetime.now() - last_off_checkin.date
                if duration_since_last_off > timedelta(minutes=30):
                    # 调用提醒功能
                    set_reminder_for_user(user_id)
        OrthodonticCheckIn.objects.create(
            user=user,
            check_in_type=check_in_type,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return JsonResponse({'success': 'Check-in recorded'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)
@csrf_exempt
def set_reminder_for_user(user_id):
    reminder_time = datetime.now() # 假设提醒是在 1 分钟后发送
    message = "Please remember to wear your braces"

    # 调用 reminder 应用的功能
    # 您可能需要稍微修改 reminder 应用的代码以使其可以被外部调用
    from reminder.models import Reminder
    Reminder.objects.create(user_id=str(user_id), reminder_time=reminder_time, message=message)


# 计算每一zhou的佩戴时间
@csrf_exempt
def weekly_check_in_duration(user, start_date, end_date):
    duration_list = []
    current_date = start_date
    last_on_time = None
    while current_date < end_date:
        next_day = current_date + timedelta(days=1)
        check_ins = OrthodonticCheckIn.objects.filter(
            user=user,
            date__range=[current_date, next_day]
        ).order_by('date')

        total_duration = timedelta(0)
        
        #import pdb;pdb.set_trace()
        for check_in in check_ins:
            if check_in.check_in_type == 'on':
                last_on_time = check_in.date
            elif check_in.check_in_type == 'off' and last_on_time:
                total_duration += check_in.date - last_on_time
                last_on_time = None

        duration_list.append(total_duration)
        current_date = next_day
    # if last_on_time:
    #     duration_list.append(end_date - last_on_time)

    return duration_list

# 计算每一yue的佩戴时间
@csrf_exempt
def monthly_check_in_duration(user, start_date, end_date):
    #import pdb;pdb.set_trace()
    duration_list = []

    while start_date < end_date:
        week_end_date = start_date + timedelta(days=7)
        week_duration = weekly_check_in_duration(user, start_date, week_end_date)
        total_week_duration = sum(week_duration, timedelta(0))
        duration_list.append(total_week_duration)
        start_date = start_date+timedelta(days=7)

    return duration_list

# 生成周报或月报
@csrf_exempt
def generate_report(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': str(e)}, status=400)

    user_id = data.get('user_id')
    if user_id is None:
        return JsonResponse({'error': 'Missing user_id'}, status=400)
    
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    report_type=data.get("report_type")
    if report_type is None:
        return JsonResponse({'error': 'Missing report type'}, status=400)
    today = datetime.now()
    if report_type == 'weekly':
        start_date = today - timedelta(days=7)
        end_date = today
        report_data = weekly_check_in_duration(user, start_date, end_date)
    elif report_type == 'monthly':
        end_date = today
        start_date = (end_date - timedelta(days=28))
        report_data = monthly_check_in_duration(user, start_date, end_date)
    report_data_hour = [duration.total_seconds()/3600 for duration in report_data]

    # 返回 JSON 响应
    return JsonResponse({'report_data': report_data_hour,'mean':np.mean(report_data_hour)})


    # 返回或处理报告结果
