/*@cc_on _d=document;eval('var document=_d')@*/

document.addEventListener('DOMContentLoaded', function() {

  flatpickr.l10ns.ja.firstDayOfWeek = 0;  
  flatpickr('#flatpickr_date', {
     wrap : true,
     dateFormat : 'Y-m-d',
     locale : 'ja',
    //  clickOpens : false,
     allowInput : true,
    //  monthSelectorType : 'static'
   });
   
   let now = new Date();
   flatpickr('#flatpickr_time', {
     wrap : true,
     enableTime : true,
     noCalendar : true,
     defaultHour : now.getHours(),
     defaultMinute : now.getMinutes(),
     dateFormat : 'H:i',
     minuteIncrement : 1,
     locale : 'ja',
    //  clickOpens : false,
     allowInput : true,
   });
   
   flatpickr('#flatpickr_date_time', {
     wrap : true,
     enableTime : true,
     dateFormat : 'Y-m-d H:i',
     defaultHour : now.getHours(),
     defaultMinute : now.getMinutes(),
     minuteIncrement : 1,
     locale : 'ja',
    //  clickOpens : false,
     allowInput : true,
    //  monthSelectorType : 'static'
   });
 });