from django import template
from django.utils import timezone
import datetime

register = template.Library()


# 基準日までの残り日数か基準日からの経過日数を返す
# reference_date は一旦将来日として仮置きして判定
#   : now => reference_date なら +
#   : reference_date => now なら -
@register.filter
def date2remain_days_or_progress_days(reference_date):

    now = timezone.localtime(timezone.now())
    reference_date = timezone.localtime(reference_date)

    remain_days = int( (reference_date - now).days )
    # 当日の引き算は -1day ...why?
    if remain_days < 0:
        remain_days += 1

    if remain_days == 0:
        return f"today"
    elif  remain_days > 0:
        if ( remain_days / 31 ) > 1:
            if ( remain_days / 365 ) > 1:
                return f"{int(remain_days/365)} years to go"
            else:
                return f"{int(remain_days/30)} months to go"
        else:
            return f"{remain_days} days to go"
    else:
        remain_days = abs(remain_days)
        if ( remain_days // 31 ) > 1:
            if ( remain_days / 365 ) > 1:
                return f"{int(remain_days/365)} years ago"
            else:
                return f"{int(remain_days/30)} months ago"
        else:
            return f"{remain_days} days ago"