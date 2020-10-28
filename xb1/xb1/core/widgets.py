from django.forms import DateTimeInput, DateInput

class DateTimePickerInput(DateTimeInput):
    template_name = "datetimepicker.html"
    
class DatePickerInput(DateInput):
    template_name = "datepicker.html"