from django import template
from django.utils import timezone

register = template.Library()


# コンペ進行率
@register.filter
def date2progressrate(start, close):

    now = timezone.localtime(timezone.now())
    start = timezone.localtime(start)
    close = timezone.localtime(close)

    term = int( (close - start).total_seconds() )
    remain = int( (close - now).total_seconds() )
    if term == 0 or remain < 0:
        return 100
    else:
        return int( ((term - remain)/term)*100 )


# スタートからの経過日数
@register.filter
def date2progress_days(start):

    now = timezone.localtime(timezone.now())
    start = timezone.localtime(start)

    progress_days = int( (now-start).days )
    progress_seconds = int( (now - start).total_seconds() )

    if progress_seconds > 0:
        if progress_days == 0:
            return f"today"
        elif  progress_days >= 0:
            if ( progress_days / 31 ) > 1:
                if ( progress_days / 365 ) > 1:
                    return f"{int(progress_days/365)} years ago"
                else:
                    return f"{int(progress_days/30)} months ago"
            else:
                return f"{progress_days} days ago"
    else:
        return "This competition is scheduled to be START"


# クローズまでの残り日数
@register.filter
def date2remain_days(close):

    now = timezone.localtime(timezone.now())
    close = timezone.localtime(close)

    remain_days = int( (close - now).days )
    remain_seconds = int( (close - now).total_seconds() )

    if remain_seconds > 0:
        if remain_seconds / (24*60*60) > 1:
            if ( remain_days / 31 ) > 1:
                if ( remain_days / 365 ) > 1:
                    return f"{int(remain_days/365)} years to go"
                else:
                    return f"{int(remain_days/30)} months to go"
            else:
                return f"{remain_days} days to go"
        else:
            if int(remain_seconds/(60*60)) >= 1:
                return f"{int(remain_seconds/(60*60))} hours to go"
            else:
                return f"Close Soon!!"

    else:
        return f"Close this Competition"