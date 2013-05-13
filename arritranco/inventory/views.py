# Create your views here.

@permission_required('change_machine')
def update_update_date(request, machine_id):
    m = Machine.objects.get(pk = machine_id)
    m.up_to_date_date = datetime.datetime.today()
    m.save()
    return HttpResponseRedirect(reverse('update-list'))

