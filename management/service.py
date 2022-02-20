from register.models import *

def add_edit_order(form):
    result = {}
    if 'id' in form:
        try:
            order = SimOrder.objects.get(id=form['id'])
            gift = Gift.objects.get(id=form['gift'])
            sim_type = SimCardOption.objects.get(id=form['sim_type'])
            client = Client.objects.get(id=form['owner'])
            order.full_name = form['full_name']
            order.tel_number = form['tel_number']
            order.sim_type = sim_type
            order.gift = gift
            order.address = form['address']
            order.owner = client
            order.save()
            result['success'] = True
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
    else:
        try:
            gift = Gift.objects.get(id=form['gift'])
            sim_type = SimCardOption.objects.get(id=form['sim_type'])
            client = Client.objects.get(id=form['owner'])
            order = SimOrder.objects.create(
                owner=client,
                full_name=form['full_name'],
                tel_number=form['tel_number'],
                sim_type=sim_type,
                gift=gift,
                address=form['address'],
            )
            order.save()
            result['success'] = True
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
    return result


def delete_order(form):
    result = {}
    if SimOrder.objects.filter(id=form['id']).exists():
        print(SimOrder.objects.filter(id=form['id']))
        try:
            SimOrder.objects.filter(id=form['id']).delete()
            result['success'] = True
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
    else:
        result['success'] = False
        result['error'] = 'Object not found!'
    return result

def get_order(id):
    return SimOrder.objects.get(id=id)


def add_edit_client(form):
    result = {}
    if 'id' in form:
        try:
            client = Client.objects.get(id=form['id'])
            client.user_id = form['user_id']
            client.username = form['username']
            client.first_name = form['first_name']
            client.save()
            result['success'] = True
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
    else:
        try:
            client = Client.objects.create(
            user_id=form['user_id'],
            username=form['username'],
            first_name=form['first_name'],
            )
            client.save()
            result['success'] = True
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
    return result


def delete_client(form):
    result = {}
    if Client.objects.filter(id=form['id']).exists():
        print(Client.objects.filter(id=form['id']))
        try:
            Client.objects.filter(id=form['id']).delete()
            result['success'] = True
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
    else:
        result['success'] = False
        result['error'] = 'Object not found!'
    return result

def get_client(id):
    return Client.objects.get(id=id)