import os
import time
import random
import string
import sys
from sty import fg, bg, ef, rs
from django.contrib.auth import authenticate
from datetime import datetime
from buex.database.orm.models import *
from buex.module.glb.ret_code import *
from buex.module.buex.constant import *
# ***********************************************************************************
# @Function: Check If All Keys in Key Array Is In Dict
# @Return: Status Code
# -----------------------------------------------------------------------------------
def check_keys(key_ary, dict_obj):
    for key in key_ary:
        if key not in dict_obj:
            return False
    return True

# ***********************************************************************************
# @Function: Authenticate User
# @Return: Status Code, User Object
# -----------------------------------------------------------------------------------
def authenticate_user(username, password):
    try:
        user_obj_list = list(tbl_user.objects.filter(username=username))
        if len(user_obj_list) == 0:
            return AUTH_ACCOUNT_NOT_FOUND, None
        user_obj = user_obj_list[0]
        if user_obj.is_active == 0:
            return AUTH_ACCOUNT_DISABLED, None

        user = authenticate(username=username, password=password)
        if user == None:
            return AUTH_WRONG_PWD, None

        return AUTH_SUCCESS, user

    except Exception as e:
        return AUTH_UNKOWN_ERROR, None

def get_user_menu_data():
    user_menu_data = [
        {
            'id': 1,
            'url': '/buex/dashboard',
            'name': 'Dashboard',
            'icon': 'icon-home',
            'parent': 0,
            'has_child': 0
        }, {
            'id': 3,
            'url': '/buex/location',
            'name': 'Locations',
            'icon': 'icon-feed',
            'parent': 0,
            'has_child': 0
        }, {
            'id': 2,
            'url': '',
            'name': 'Guards',
            'icon': 'icon-user',
            'parent': 0,
            'has_child': 1
        }, {
            'id': 6,
            'url': '',
            'name': 'Equipment',
            'icon': 'icon-camcorder',
            'parent': 0,
            'has_child': 1
        }, {
            'id': 13,
            'url': '/buex/monthly',
            'name': 'Monthly',
            'icon': 'icon-bag',
            'parent': 0,
            'has_child': 0
        }, {
            'id': 5,
            'url': '/buex/yearly',
            'name': 'Yearly',
            'icon': 'icon-calendar',
            'parent': 0,
            'has_child': 0
        }, {
            'id': 7,
            'url': '/buex/incident',
            'name': 'Incident',
            'icon': 'icon-energy',
            'parent': 0,
            'has_child': 0
        }, {
            'id': 9,
            'url': '/buex/guard',
            'name': 'Management',
            'icon': 'icon-user',
            'parent': 2,
            'has_child': 0
        }, {
            'id': 10,
            'url': '/buex/guard/cost',
            'name': 'Wage Setting',
            'icon': '',
            'parent': 2,
            'has_child': 0
        }, {
            'id': 11,
            'url': '/buex/equipment',
            'name': 'Template',
            'icon': '',
            'parent': 6,
            'has_child': 0
        }, {
            'id': 12,
            'url': '/buex/equipment/cost',
            'name': 'Expenses',
            'icon': '',
            'parent': 6,
            'has_child': 0
        }, {
            'id': 14,
            'url': '/buex/guard/calculation',
            'name': 'Daily Attendace',
            'icon': '',
            'parent': 2,
            'has_child': 0
        }

    ]
    return user_menu_data

def print_exception():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    error_msg = bg.red
    error_msg += str(exc_obj) + ", File: " + str(exc_tb.tb_frame.f_code.co_filename) + ", Line: " + str(exc_tb.tb_lineno)
    error_msg += bg.rs
    print(error_msg)

def get_by_query(array, queries):
    newArray = []
    for item in array:
        query_keys = queries.keys()
        g_query_success = 0
        for key in query_keys:
            if queries[key] != item[key]:
                g_query_success = 1
                break
        if g_query_success == 0:
            newArray.append(item)
    return newArray

def get_monthly_equppment_cost(monthly_equipment):
    t = 0
    for item in monthly_equipment:
        t += item['purchased_count'] * item['equipment_cost']
    t = round(t, 2)
    return t

def get_guards():
    arrays = list(guard.objects.all().values())
    return arrays

def get_locations():
    arrays = list(location.objects.all().values())
    return arrays

def get_equipmenttpl():
    arrays = list(equipmenttpl.objects.all().values())
    return arrays

def get_equipmentcost():
    arrays = list(equipmentcost.objects.all().values())
    return arrays

def get_attendance():
    arrays = list(attendance.objects.all().values())
    return arrays

def get_attendance_hour(attendance_info, guard_id):
    query = {'guard_id': guard_id}
    newarray = get_by_query(attendance_info, query)
    hour = 0
    if len(newarray) == 1:
        hour = newarray[0]['attented_hour']
    return hour

def get_guard_cost():
    guard_cost = 0
    cost_obj = list(serivcecost.objects.filter(service_name=GAURAD_SERVICE_NAME).values())
    if len(cost_obj) == 1:
        guard_cost = cost_obj[0]['service_cost']
    return guard_cost

def get_monthly_guard_cost(monthly_attendance):
    g_cost = get_guard_cost()
    t = 0
    for item in monthly_attendance:
        t += item['attented_hour'] * g_cost
    t = round(t, 2)
    return t

def get_monthly_statistics(location_id):
    current_year = datetime.today().year
    part_1 = []
    part_2 = []
    part_3 = []
    part_4 = []
    for k in range(0, 12):
        i = k + 1

        if location_id == 0:
            monthly_equipment = list(equipmentcost.objects.filter(purchased_date__year=current_year, purchased_date__month=i).values())
            monthly_attendance = list(attendance.objects.filter(attended_date__year=current_year, attended_date__month=i).values())
        else:
            monthly_equipment = list(equipmentcost.objects.filter(assigning_loc_id=location_id, purchased_date__year=current_year, purchased_date__month=i).values())
            monthly_attendance = list(attendance.objects.filter(location_id=location_id, attended_date__year=current_year, attended_date__month=i).values())

        monthly_guard_cost = get_monthly_guard_cost(monthly_attendance)
        monthly_equppment_cost = get_monthly_equppment_cost(monthly_equipment)
        t_monthly = monthly_equppment_cost + monthly_guard_cost
        cost = {"monthly_equppment_cost": monthly_equppment_cost, "monthly_guard_cost": monthly_guard_cost,
                "t_monthly": t_monthly}
        if i >= 1 and i <= 3:
            cost['month'] = datetime(1970, i, 1).strftime("%B")
            part_1.append(cost)
        if i >= 4 and i <= 6:
            cost['month'] = datetime(1970, i, 1).strftime("%B")
            part_2.append(cost)
        if i >= 7 and i <= 9:
            cost['month'] = datetime(1970, i, 1).strftime("%B")
            part_3.append(cost)
        if i >= 10 and i <= 12:
            cost['month'] = datetime(1970, i, 1).strftime("%B")
            part_4.append(cost)

    data = {
        "part_1": part_1,
        "part_2": part_2,
        "part_3": part_3,
        "part_4": part_4,
    }
    return data

def get_yearly_statistics(location_id, year):
    if location_id != 0:
        monthly_equipment = list(equipmentcost.objects.filter(assigning_loc_id=location_id, purchased_date__year=year).values())
        monthly_attendance = list(attendance.objects.filter(location_id=location_id, attended_date__year=year).values())
    else:
        monthly_equipment = list(equipmentcost.objects.filter(purchased_date__year=year).values())
        monthly_attendance = list(attendance.objects.filter(attended_date__year=year).values())
    monthly_guard_cost = get_monthly_guard_cost(monthly_attendance)
    monthly_equppment_cost = get_monthly_equppment_cost(monthly_equipment)
    t_monthly = monthly_equppment_cost + monthly_guard_cost
    cost = {"monthly_equppment_cost": monthly_equppment_cost, "monthly_guard_cost": monthly_guard_cost,
            "t_monthly": t_monthly}
    return cost

def get_location_by_id(location_id):
    location_obj = list(location.objects.filter(pk=location_id).values())
    if len(location_obj) == 1:
        return location_obj[0]
    else:
        return {}

def get_guard_by_id(guard_id):
    guard_obj = list(guard.objects.filter(pk=guard_id).values())
    if len(guard_obj) == 1:
        return guard_obj[0]
    else:
        return {}