from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from buex.database.orm.models import *
from buex.module.buex import common as mcm
from buex.module.buex import excel
from buex.module.buex.constant import *
from django.db import transaction
from django.http import HttpResponse
from datetime import datetime, timedelta, date
from dateutil import relativedelta
import json
from django.utils.translation import ugettext_lazy as _
# Create your views here.

@login_required
def dashboardview(request, template_name='user/dashboard.html'):
    equipmenttpls = list(equipmenttpl.objects.all().values())
    guards = list(guard.objects.all().values())
    locations = list(location.objects.all().values())

    guard_info = {}
    guard_info['count'] = len(guards)

    locations_info = {}
    locations_info['count'] = len(locations)

    equipmenttpls_info = {}
    equipmenttpls_info['count'] = len(equipmenttpls)

    data = {
        "menu_data": mcm.get_user_menu_data(),
        "menu_id": 1,
        "page_title": "Dashboard",
        "guard": guard_info,
        "location": locations_info,
        "equipmenttpl": equipmenttpls_info,

    }
    return render(request, template_name, data)

@login_required
def guardview(request, template_name='user/guard.html'):
    guards = list(guard.objects.all().values())

    header_data = []
    header_data.append({"name": _("ID")})
    header_data.append({"name": _("Username")})
    header_data.append({"name": _("Email")})
    header_data.append({"name": _("Action")})

    data = {
        "menu_data": mcm.get_user_menu_data(),
        "menu_id": 9,
        "page_title": "Guard",
        "gurads_list": guards,
        "header_data": header_data,
    }
    return render(request, template_name, data)

@login_required
def guardadd(request):
    try:
        params = request.POST

        new_params = {}
        new_params['name'] = params['reg_guard_name']
        new_params['email'] = params['reg_guard_email']

        if list(guard.objects.filter(name=new_params['name']).values()):
            return HttpResponse("name_exists")

        guard_obj = guard(**new_params)
        guard_obj.save()

        return HttpResponse("success")
    except:
        mcm.print_exception()
        return HttpResponse("failure")

@login_required
def guardupdate(request):
    try:
        params = request.POST
        row_id = int(params['row_id'])
        not_updating_name = int(params['not_updating_name'])

        new_params = {}
        if not_updating_name:
            new_params['name'] = params['reg_guard_name']
        new_params['email'] = params['reg_guard_email']

        if list(guard.objects.filter(name=params['reg_guard_name']).values()) and not_updating_name:
            return HttpResponse("name_exists")

        guard_obj = guard.objects.get(pk=row_id)
        for key, value in new_params.items():
            setattr(guard_obj, key, value)
        guard_obj.save()

        return HttpResponse("success")
    except:
        mcm.print_exception()
        return HttpResponse("failure")

@login_required
def guardupdel(request):
    try:
        params = request.POST
        row_id = params['row_id']
        guard.objects.filter(pk=row_id).delete()
        return HttpResponse("success")
    except:
        mcm.print_exception()
        return HttpResponse("failure")

@login_required
def guardcalculation(request, template_name='user/attendance.html'):
    try:
        params = request.GET

        guard_cost = 0
        cost_obj = list(serivcecost.objects.filter(service_name=GAURAD_SERVICE_NAME).values())
        if len(cost_obj) == 1:
            guard_cost = cost_obj[0]['service_cost']
        guards = mcm.get_guards()

        locations = list(location.objects.all().values())
        location_id = locations[0]['id']
        if "location_id" in params:
            location_id = int(params['location_id'])

        filter_date = date.today()
        filter_date_str = filter_date.strftime("%Y-%m-%d")
        if "filter_date" in params:
            filter_date_str = params["filter_date"]
            filter_date = datetime.strptime(filter_date_str, "%Y-%m-%d").date()

        attendance_info = list(attendance.objects.filter(location_id=location_id, attended_date=filter_date).values())
        attendance_per_day_list = []
        total_hour = 0
        for item in guards:
            new_params = {}
            new_params['name'] = item['name']
            new_params['attended_hour'] = mcm.get_attendance_hour(attendance_info, item['id'])
            total_hour += new_params['attended_hour']
            new_params['guard_id'] = item['id']
            attendance_per_day_list.append(new_params)

        total_hour = round(float(total_hour), 2)
        total_cost = round(total_hour * guard_cost, 2)

        header_data = []
        header_data.append({"name": _("Guard ID")})
        header_data.append({"name": _("Guard Name")})
        header_data.append({"name": _("Attendance Hour")})

        data = {
            "menu_data": mcm.get_user_menu_data(),
            "menu_id": 14,
            "page_title": "Daily Attendace",
            "attendance_per_day_list": attendance_per_day_list,
            "header_data": header_data,
            "filter_date": filter_date_str,
            "guard_cost": guard_cost,
            "location_id": location_id,
            "total_hour": total_hour,
            "locations": locations,
            "total_cost": total_cost
        }
        return render(request, template_name, data)
    except:
        mcm.print_exception()
        return HttpResponse("Unexpected Error")

@login_required
def guardcostsetview(request, template_name="user/guard_cost.html"):
    guard_cost = 0
    cost_obj = list(serivcecost.objects.filter(service_name=GAURAD_SERVICE_NAME).values())
    if len(cost_obj) == 1:
        guard_cost = cost_obj[0]['service_cost']

    data = {
        "menu_data": mcm.get_user_menu_data(),
        "menu_id": 10,
        "page_title": "Guard Cost Set up",
        "guard_cost": guard_cost
    }
    return render(request, template_name, data)

@login_required
def set_guard_cost(request):
    try:
        params = request.POST
        set_guard_cost = params['ga_rateperhour']
        set_guard_cost = float(set_guard_cost)

        cost_obj = list(serivcecost.objects.filter(service_name=GAURAD_SERVICE_NAME).values())
        if len(cost_obj) == 1:
            serivcecost.objects.filter(service_name=GAURAD_SERVICE_NAME).update(service_cost=set_guard_cost)
        elif len(cost_obj) == 0:
            new_params = {}
            new_params['service_name'] = GAURAD_SERVICE_NAME
            new_params['service_cost'] = set_guard_cost
            serivcecost_obj = serivcecost(**new_params)
            serivcecost_obj.save()
        else:
            pass
        return HttpResponse(HTTPRESTPNSE_SUCCESS_STR)
    except:
        mcm.print_exception()
        return HttpResponse(HTTPRESTPNSE_FAILURE_STR)

@login_required
def save_attendances(request):
    try:
        params = request.POST

        ga_today_date_str = params['ga_today_date']
        ga_today_date = datetime.strptime(ga_today_date_str, "%Y-%m-%d").date()

        location_id = int(params['location_id'])

        guard_attendance = json.loads(params['guard_attendance'])
        for item in guard_attendance:
            if float(item['loc_attended_hour']) <= 0:
                continue

            attendance_info = list(attendance.objects.filter(location_id=location_id, guard_id=int(item['guard_id']), attended_date=ga_today_date).values())
            if len(attendance_info) == 0:
                new_params = {}
                new_params['guard_id'] = item['guard_id']
                new_params['location_id'] = location_id
                new_params['attented_hour'] = float(item['loc_attended_hour'])
                new_params['attended_date'] = ga_today_date
                attendance_obj = attendance(**new_params)
                attendance_obj.save()
            elif len(attendance_info) == 1:
                pk_id = attendance_info[0]['id']
                new_params = {}
                new_params['attented_hour'] = float(item['loc_attended_hour'])
                attendance_obj = attendance.objects.get(pk=pk_id)
                for key, value in new_params.items():
                    setattr(attendance_obj, key, value)
                attendance_obj.save()
            else:
                pass
        return HttpResponse(HTTPRESTPNSE_SUCCESS_STR)
    except:
        return HttpResponse(HTTPRESTPNSE_FAILURE_STR)

@login_required
def locationview(request, template_name='user/location.html'):
    locations = list(location.objects.all().values())

    header_data = []
    header_data.append({"name": _("ID")})
    header_data.append({"name": _("Location Name")})
    header_data.append({"name": _("Description")})
    header_data.append({"name": _("Action")})

    data = {
        "menu_data": mcm.get_user_menu_data(),
        "menu_id": 3,
        "page_title": "Location",
        "locations_list": locations,
        "header_data": header_data,
    }
    return render(request, template_name, data)

@login_required
def locationadd(request):
    try:
        params = request.POST

        new_params = {}
        new_params['name'] = params['reg_location_name']
        new_params['description'] = params['reg_location_desp']

        if list(location.objects.filter(name=new_params['name']).values()):
            return HttpResponse("name_exists")

        location_obj = location(**new_params)
        location_obj.save()

        return HttpResponse(HTTPRESTPNSE_SUCCESS_STR)
    except:
        mcm.print_exception()
        return HttpResponse(HTTPRESTPNSE_FAILURE_STR)

@login_required
def locationupdate(request):
    try:
        params = request.POST
        row_id = int(params['row_id'])
        not_updating_name = int(params['not_updating_name'])

        new_params = {}
        if not_updating_name:
            new_params['name'] = params['reg_location_name']
        new_params['description'] = params['reg_location_desp']

        if list(location.objects.filter(name=params['reg_location_name']).values()) and not_updating_name:
            return HttpResponse("name_exists")

        location_obj = location.objects.get(pk=row_id)
        for key, value in new_params.items():
            setattr(location_obj, key, value)
        location_obj.save()

        return HttpResponse(HTTPRESTPNSE_SUCCESS_STR)
    except:
        mcm.print_exception()
        return HttpResponse(HTTPRESTPNSE_FAILURE_STR)

@login_required
def locationdel(request):
    try:
        params = request.POST
        row_id = params['row_id']
        location.objects.filter(pk=row_id).delete()
        return HttpResponse(HTTPRESTPNSE_SUCCESS_STR)
    except:
        mcm.print_exception()
        return HttpResponse(HTTPRESTPNSE_FAILURE_STR)

@login_required
def equipmentview(request, template_name='user/equipmenttpl.html'):
    equipmenttpls = list(equipmenttpl.objects.all().values())

    header_data = []
    header_data.append({"name": _("ID")})
    header_data.append({"name": _("Equipment Name")})
    header_data.append({"name": _("Equipment Alias")})
    header_data.append({"name": _("Equipment Description")})
    header_data.append({"name": _("Action")})

    data = {
        "menu_data": mcm.get_user_menu_data(),
        "menu_id": 11,
        "page_title": "Equipment Templates",
        "equipmenttpls_list": equipmenttpls,
        "header_data": header_data,
    }
    return render(request, template_name, data)

@login_required
def equipmentadd(request):
    try:
        params = request.POST

        new_params = {}
        new_params['equipment_name'] = params['reg_equipment_name']
        new_params['equipment_desp'] = params['reg_equipment_desp']
        new_params['equipment_alias'] = params['reg_equipment_alias']

        if list(equipmenttpl.objects.filter(equipment_name=params['reg_equipment_name']).values()):
            return HttpResponse("name_exists")

        equipmenttpl_obj = equipmenttpl(**new_params)
        equipmenttpl_obj.save()
        return HttpResponse(HTTPRESTPNSE_SUCCESS_STR)
    except:
        mcm.print_exception()
        return HttpResponse(HTTPRESTPNSE_FAILURE_STR)

@login_required
def equipmentupdate(request):
    try:
        params = request.POST
        row_id = int(params['row_id'])
        not_updating_name = int(params['not_updating_name'])

        new_params = {}
        if not_updating_name:
            new_params['equipment_name'] = params['reg_equipment_name']
        new_params['equipment_desp'] = params['reg_equipment_desp']
        new_params['equipment_alias'] = params['reg_equipment_alias']

        if list(equipmenttpl.objects.filter(equipment_name=params['reg_equipment_name']).values()) and not_updating_name:
            return HttpResponse("name_exists")

        equipmenttpl_obj = equipmenttpl.objects.get(pk=row_id)
        for key, value in new_params.items():
            setattr(equipmenttpl_obj, key, value)
        equipmenttpl_obj.save()
        return HttpResponse(HTTPRESTPNSE_SUCCESS_STR)
    except:
        mcm.print_exception()
        return HttpResponse(HTTPRESTPNSE_FAILURE_STR)

@login_required
def equipmentdel(request):
    try:
        params = request.POST
        row_id = params['row_id']
        equipmenttpl.objects.filter(pk=row_id).delete()
        return HttpResponse(HTTPRESTPNSE_SUCCESS_STR)
    except:
        mcm.print_exception()
        return HttpResponse(HTTPRESTPNSE_FAILURE_STR)

@login_required
def equipmentcostview(request, template_name='user/equipment_expenses.html'):
    equipment_costs = list(equipmentcost.objects.all().values())
    locations = list(location.objects.all().values())
    equipmenttpls = list(equipmenttpl.objects.all().values())

    header_data = []
    header_data.append({"name": _("Equipment Template")})
    header_data.append({"name": _("Price")})
    header_data.append({"name": _("Amount")})
    header_data.append({"name": _("Assigned Location")})
    header_data.append({"name": _("Purchased Date")})
    header_data.append({"name": _("Action")})

    for item in equipment_costs:
        item['purchased_date'] = item['purchased_date'].strftime("%Y-%m-%d")

    data = {
        "menu_data": mcm.get_user_menu_data(),
        "menu_id": 12,
        "page_title": "Equipment Expenses",
        "equipmentcost_list": equipment_costs,
        "locations": locations,
        "equipmenttpls": equipmenttpls,
        "header_data": header_data,
    }
    return render(request, template_name, data)

@login_required
def equipmentpurchase(request):
    try:
        params = request.POST
        new_params = {}
        new_params['purchased_date'] = params['purchased_date']
        new_params['equipment_cost'] = params['equipment_cost']
        new_params['purchased_count'] = params['equipment_amount']
        new_params['assigning_loc_id'] = params['assigning_location']
        new_params['equipmenttpl_id'] = params['equipment_template']

        equipmentcost_obj = equipmentcost(**new_params)
        equipmentcost_obj.save()

        return HttpResponse(HTTPRESTPNSE_SUCCESS_STR)
    except:
        mcm.print_exception()
        return HttpResponse(HTTPRESTPNSE_FAILURE_STR)

@login_required
def del_equipcost(request):
    try:
        params = request.POST
        equipmentcost_id = params['id']
        equipmentcost.objects.filter(pk=equipmentcost_id).delete()
        return HttpResponse(HTTPRESTPNSE_SUCCESS_STR)
    except:
        mcm.print_exception()
        return HttpResponse(HTTPRESTPNSE_FAILURE_STR)

@login_required
def update_equipcot(request):
    try:
        params = request.POST
        new_params = {}
        new_params['purchased_date'] = params['purchased_date']
        new_params['equipment_cost'] = params['equipment_cost']
        new_params['purchased_count'] = params['equipment_amount']
        new_params['assigning_loc_id'] = params['assigning_location']
        new_params['equipmenttpl_id'] = params['equipment_template']

        row_id = params['id']
        equipmentcost_obj = equipmentcost.objects.get(pk=row_id)
        for key, value in new_params.items():
            setattr(equipmentcost_obj, key, value)
        equipmentcost_obj.save()
        return HttpResponse(HTTPRESTPNSE_SUCCESS_STR)
    except:
        mcm.print_exception()
        return HttpResponse(HTTPRESTPNSE_FAILURE_STR)


@login_required
def monthlyview(request, template_name='user/monthly.html'):
    data = {}
    data['menu_data'] = mcm.get_user_menu_data()
    data['locations'] = mcm.get_locations()
    data['page_title'] = "Monthly Expenses"
    data['menu_id'] = 13
    data['current_year'] = datetime.now().year
    return render(request, template_name, data)

@login_required
def monthlyfilter(request, template_name='user/monthly_statistics_part.html'):
    params = request.POST
    location_id = int(params['location_id'])
    data = mcm.get_monthly_statistics(location_id)
    return render(request, template_name, data)

@login_required
def yearlyview(request, template_name='user/yearly.html'):
    data = {}
    data['menu_data'] = mcm.get_user_menu_data()
    data['locations'] = mcm.get_locations()
    data['page_title'] = "Yearly Expenses"
    data['menu_id'] = 5
    data['current_year'] = datetime.now().year
    years = []
    for i in range(0, 5):
        years.append(data['current_year'] - i)
    data['years'] = years
    return render(request, template_name, data)

@login_required
def yearlyfilter(request, template_name='user/yearly_statistics_part.html'):
    params = request.POST
    location_id = int(params['location_id'])
    year = int(params['year_selected'])
    data = mcm.get_yearly_statistics(location_id, year)
    return render(request, template_name, data)

@login_required
def incidentview(request, template_name='user/incident.html'):
    incidents = list(incident.objects.all().values())
    locations = list(location.objects.all().values())
    guards = list(guard.objects.all().values())

    for item in incidents:
        try:
            item['location'] = mcm.get_location_by_id(item['location_id'])['name']
        except:
            item['location'] = '-'
        try:
            item['guard'] = mcm.get_guard_by_id(item['guard_id'])['name']
        except:
            item['guard'] = '-'
        item['occured_at_date'] = item['event_time'].strftime("%Y-%m-%d")
        item['occured_at_time'] = item['event_time'].strftime("%H:%M")

    header_data = []
    header_data.append({"name": _("ID")})
    header_data.append({"name": _("Type")})
    header_data.append({"name": _("Description")})
    header_data.append({"name": _("Occured At")})
    header_data.append({"name": _("Location")})
    header_data.append({"name": _("Guard")})
    header_data.append({"name": _("Action")})

    data = {
        "menu_data": mcm.get_user_menu_data(),
        "menu_id": 7,
        "page_title": "Incident",
        "incidents_list": incidents,
        "locations": locations,
        "guards": guards,
        "header_data": header_data,
    }
    return render(request, template_name, data)

@login_required
def incidentadd(request):
    try:
        params = request.POST

        new_params = {}
        new_params['location_id'] = params['assigning_location']
        new_params['guard_id'] = params['assigning_guard']
        new_params['event_time'] = params['occured_at_date'] + ' ' + params['occured_at_time']
        new_params['event_type'] = params['event_type']
        new_params['event_desp'] = params['event_desp']

        incident_obj = incident(**new_params)
        incident_obj.save()

        return HttpResponse("success")
    except:
        mcm.print_exception()
        return HttpResponse("failure")

@login_required
def incidentupdate(request):
    try:
        params = request.POST
        row_id = int(params['row_id'])

        new_params = {}
        new_params['name'] = params['assigning_location']
        new_params['guard_id'] = params['assigning_guard']
        new_params['event_time'] = params['occured_at_date'] + ' ' + params['occured_at_time']
        new_params['event_type'] = params['event_type']
        new_params['event_desp'] = params['event_desp']


        incident_obj = incident.objects.get(pk=row_id)
        for key, value in new_params.items():
            setattr(incident_obj, key, value)
        incident_obj.save()

        return HttpResponse("success")
    except:
        mcm.print_exception()
        return HttpResponse("failure")

@login_required
def incidentdel(request):
    try:
        params = request.POST
        row_id = params['row_id']
        incident.objects.filter(pk=row_id).delete()
        return HttpResponse("success")
    except:
        mcm.print_exception()
        return HttpResponse("failure")

def export_monthly_report(request):
    current_year = datetime.today().year

    new_params = {}
    new_params['current_year'] = current_year

    directory_name = "static/buex/public/hFlRe6811i7aKLtcbpcj0FIzrqdKyguJXQnY+51Xs0S7Qk1Oy6bANdbAUDM/"
    excel_filename = directory_name + "/" + "monthly_report_" + datetime.today().strftime("%m%d%Y") + ".xlsx"

    context = {'contentAlias': 'monthlyreport',
               'request': request,
               'param': new_params}

    excel.render_excel(context, excel_filename)
    return HttpResponse(excel_filename)