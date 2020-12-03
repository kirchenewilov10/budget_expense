from django.urls import path

from . import views

urlpatterns = [
    path('dashboard', views.dashboardview, name='dashboard'),

    path('guard', views.guardview, name='guard'),
    path('guard/add', views.guardadd, name='guard_add'),
    path('guard/update', views.guardupdate, name='guard_update'),
    path('guard/del', views.guardupdel, name='guard_del'),
    path('guard/calculation', views.guardcalculation, name='guardcalculation'),
    path('guard/cost', views.guardcostsetview, name='guardcostsetview'),
    path('guard/set_guard_cost', views.set_guard_cost, name='set_guard_cost'),
    path('guard/save_attendances', views.save_attendances, name='save_attendances'),

    path('location', views.locationview, name='location'),
    path('location/add', views.locationadd, name='locationadd'),
    path('location/update', views.locationupdate, name='locationupdate'),
    path('location/del', views.locationdel, name='locationdel'),

    path('equipment', views.equipmentview, name='equipment'),
    path('equipment/add', views.equipmentadd, name='locationadd'),
    path('equipment/update', views.equipmentupdate, name='locationupdate'),
    path('equipment/del', views.equipmentdel, name='locationdel'),
    path('equipment/cost', views.equipmentcostview, name='equipmentcost'),
    path('equipment/purchase', views.equipmentpurchase, name='equipmentpurchase'),
    path('equipment/del_equipcost', views.del_equipcost, name='del_equipcost'),
    path('equipment/update_equipcot', views.update_equipcot, name='update_equipcot'),

    path('monthly', views.monthlyview, name='monthlyview'),
    path('monthly/filter', views.monthlyfilter, name='monthlyfilter'),
    path('monthly/export', views.export_monthly_report, name='export_monthly_report'),

    path('yearly', views.yearlyview, name='yearlyview'),
    path('yearly/filter', views.yearlyfilter, name='yearlyfilter'),

    path('incident', views.incidentview, name='incident'),
    path('incident/add', views.incidentadd, name='incident'),
    path('incident/update', views.incidentupdate, name='incident'),
    path('incident/del', views.incidentdel, name='incident'),

]