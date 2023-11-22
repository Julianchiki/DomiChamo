from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from .models import Categories, MeasurementUnits, Elements, Inventories, Domicilies, DomicilieDetail, AssignDomicilies
from .forms import FormAddElements, FormEditElements, AddInventory, FormAddInventory, AddElements, Assign
from datetime import datetime, timedelta

# Create your views here.

def signin(request):
    if request.method == 'GET':
        return render(request, 'authentication/login.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'authentication/login.html', {'error': 'Credenciales incorrectas'})
        else:
            login(request, user)
            if user.groups.filter(name='Administrador').exists():
                return redirect('categories')
            elif user.groups.filter(name='Domiciliario').exists():
                return redirect('my_domicilies')
            else:
                return redirect('domicilie')
                
        
def register(request):
    if request.method == 'GET':
        return render(request, 'authentication/register.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=request.POST['password1'], email=request.POST['email'])
                
                # Asignar el usuario al grupo "Cliente"
                cliente_group, created = Group.objects.get_or_create(name='Usuario')
                user.groups.add(cliente_group)

                user.save()
                login(request, user)
                return redirect('login')
            except:
                return render(request, 'authentication/register.html', {'error': 'El usuario ya existe'})
        return render(request, 'authentication/register.html', {'error': 'No coinciden las contraseñas ingresadas'})

def signout(request):
    logout(request)
    return redirect('login')

def categories(request):
    categories = Categories.objects.all()
    title = 'Categorias'
    return render(request, 'parameters/categories/index.html', {'categories': categories, 'title': title})

def measurement_units(request):
    measurement_units = MeasurementUnits.objects.all()
    title = 'Unidades de medida'
    return render(request, 'parameters/measurement_unit/index.html', {'measurement_units': measurement_units, 'title': title})

def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name:
            Categories.objects.create(name=name)
            # Puedes redirigir a una página de éxito o hacer lo que necesites aquí.
            return redirect('categories')  # Cambia 'exito' por la URL a la que deseas redirigir.
        # Si los datos del formulario no son válidos, puedes manejar los errores aquí.
    return render(request, 'parameters/categories/index.html')  # Cambia 'tu_template.html' por el nombre de tu plantilla modal.

def edit_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        name = request.POST.get('name')
        
        # Obtener el objeto de la categoría a editar
        category = get_object_or_404(Categories, id=category_id)
        
        # Actualizar los datos
        category.name = name
        category.save()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('categories')
    else:
        return JsonResponse({'error': 'Método no permitido'})
    
def delete_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('delete_category_id')
        
        # Obtener el objeto de la categoría a editar
        category = get_object_or_404(Categories, id=category_id)
        
        # Actualizar los datos
        category.delete()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('categories')
    else:
        return JsonResponse({'error': 'Método no permitido'})


def add_measurement_unit(request):
    if request.method == 'POST':
        name = request.POST['name_measurement']
        abbreviation = request.POST['abbreviation']
        if name:
            unit = MeasurementUnits(
                name=name,
                abbreviation=abbreviation,
            )
            unit.save()
            # Puedes redirigir a una página de éxito o hacer lo que necesites aquí.
            return redirect('measurement_units')  # Cambia 'exito' por la URL a la que deseas redirigir.
        # Si los datos del formulario no son válidos, puedes manejar los errores aquí.
    return render(request, 'parameters/measurement_unit/index.html')  # Cambia 'tu_template.html' por el nombre de tu plantilla modal.

def edit_measurement_unit(request):
    if request.method == 'POST':
        measurement_unit_id = request.POST.get('measurement_unit_id')
        name = request.POST.get('name_measurement')
        abbreviation = request.POST.get('abbreviation')
        
        # Obtener el objeto de la categoría a editar
        measurement_unit = get_object_or_404(MeasurementUnits, id=measurement_unit_id)
        
        # Actualizar los datos
        measurement_unit.name = name
        measurement_unit.abbreviation = abbreviation

        measurement_unit.save()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('measurement_units')
    else:
        return JsonResponse({'error': 'Método no permitido'})
    
def delete_measurement_unit(request):
    if request.method == 'POST':
        measurement_unit_id = request.POST.get('delete_measurement_unit_id')
        
        # Obtener el objeto de la categoría a editar
        measurement_unit = get_object_or_404(MeasurementUnits, id=measurement_unit_id)
        
        # Actualizar los datos
        measurement_unit.delete()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('measurement_units')
    else:
        return JsonResponse({'error': 'Método no permitido'})

def elements_index(request):
    form = AddElements()
    formulario = FormAddElements(request.POST or None)
    formularioEdit = FormEditElements(request.POST or None)
    elements = Elements.objects.all()
    categories = Categories.objects.all()
    measurement_units = MeasurementUnits.objects.all()
    title = 'Productos'
    return render(request, 'elements/index.html', {'form': form, 'formulario': formulario, 'formularioEdit': formularioEdit ,'elements': elements, 'categories': categories, 'measurement_units': measurement_units, 'title': title})

def add_elements(request):
    if request.method == 'POST':
        formulario = FormAddElements(request.POST or None, request.FILES or None)
        if formulario.is_valid():
            element = formulario.save(commit=False)
            category_id = request.POST['category_id']
            measurement_unit_id = request.POST['measurement_unit_id']
            user_id = request.user.id

            element.category_id = category_id
            element.measurement_unit_id = measurement_unit_id
            
            element.save()
            # Puedes redirigir a una página de éxito o hacer lo que necesites aquí.
            return redirect('elements.index')  # Cambia 'exito' por la URL a la que deseas redirigir.
        # Si los datos del formulario no son válidos, puedes manejar los errores aquí.
    else:
        formulario = FormAddElements()
    return render(request, 'elements/index.html')  # Cambia 'tu_template.html' por el nombre de tu plantilla modal.

def edit_elements(request):
    element_id = request.POST.get('element_id')
    if request.method == 'POST':
        id = get_object_or_404(Elements, id=element_id)
        form = FormEditElements(request.POST, request.FILES, instance=id)
        if form.is_valid():
            element = form.save(commit=False)
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            category_id = request.POST.get('category_id')
            measurement_unit_id = request.POST.get('measurement_unit_id')
            
            # Actualizar los datos
            element.name = name
            element.description = description
            element.price = price
            element.category_id = category_id
            element.measurement_unit_id = measurement_unit_id
            element.save()
        
            # Redirigir al usuario a la página deseada, por ejemplo:
            return redirect('elements.index')
    else:
        return JsonResponse({'error': 'Método no permitido'})

def delete_elements(request):
    if request.method == 'POST':
        element_id = request.POST.get('element_id')
        
        # Obtener el objeto de la categoría a editar
        element = get_object_or_404(Elements, id=element_id)
        
        # Actualizar los datos
        element.delete()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('elements.index')
    else:
        return JsonResponse({'error': 'Método no permitido'})
    
def inventories_index(request):
    form = AddInventory()
    formulario = FormAddInventory(request.POST or None)
    data = Inventories.objects.all()
    elements = Elements.objects.all()
    title = 'Inventario'
    return render(request, 'inventories/index.html', {'form': form, 'formulario': formulario, 'data': data, 'elements': elements, 'title': title})

def add_inventories(request):
    if request.method == 'POST':
        formulario = FormAddInventory(request.POST or None)
        if formulario.is_valid():
            inventory = formulario.save(commit=False)
            element_id = request.POST['element_id']
            user_id = request.user.id

            inventory.user_id = user_id
            inventory.element_id = element_id
            inventory.save()
            # Puedes redirigir a una página de éxito o hacer lo que necesites aquí.
            return redirect('inventories.index')  # Cambia 'exito' por la URL a la que deseas redirigir.
        # Si los datos del formulario no son válidos, puedes manejar los errores aquí.
    else:
        formulario = FormAddElements()
    return render(request, 'inventories/index.html')  # Cambia 'tu_template.html' por el nombre de tu plantilla modal.

def edit_inventories(request):
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory_id')
        element_select = request.POST.get('element_select')
        amount = request.POST.get('amount')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        expiration_date = request.POST.get('expiration_date')
        lot_number = request.POST.get('lot_number')

        # Obtener el objeto de la categoría a editar
        inventory = get_object_or_404(Inventories, id=inventory_id)
        
        # Actualizar los datos
        inventory.element_id = element_select
        inventory.amount = amount
        inventory.stock = stock
        inventory.price = price
        inventory.expiration_date = expiration_date
        inventory.lot_number = lot_number
        inventory.save()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('inventories.index')
    else:
        return JsonResponse({'error': 'Método no permitido'})
    
def delete_inventories(request):
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory_id')
        
        # Obtener el objeto de la categoría a editar
        inventory = get_object_or_404(Inventories, id=inventory_id)
        
        # Actualizar los datos
        inventory.delete()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('inventories.index')
    else:
        return JsonResponse({'error': 'Método no permitido'})


def domicilie(request):
    title = 'Domicilios'
    inventories = Inventories.objects.all()
    current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M")
    return render(request, 'user/add_domicilie.html', {'datetime': current_datetime, 'title': title, 'inventories': inventories})

def save_domicilie(request):
    if request.method == 'POST':
        # Obtiene la información del formulario
        product_ids = request.POST.getlist('products[]')
        print('Productos: ' + str(product_ids))
        amounts = request.POST.getlist('amount[]')
        print('Cantidades: ' + str(amounts))
        subtotals = request.POST.getlist('subtotal[]')
        print('Subtotales: ' + str(subtotals))
        user = request.user.id
        date_time = request.POST['date_time']
        addres = request.POST['addres']

        total = 0
        for t in range(len(subtotals)):
            subtotal = subtotals[t]
            print(subtotal)
            total += int(subtotal)
        
        domicilie = Domicilies(
            date_time=date_time,
            state='En proceso',
            addres = addres,
            total=total,
            user_id=user
        )
        domicilie.save()

        for i in range(len(product_ids)):
            inventory_id = product_ids[i]
            amount = amounts[i]
            subtotal = subtotals[i]
            amount = int(amount)
            inventory = get_object_or_404(Inventories, id=inventory_id)
            
            if inventory.amount < amount:
                error = 'Cantidad de producto insuficiente'
                print('Error: ' + error)
                break  # Salir del bucle si se encuentra un error

            domicilie_detail = DomicilieDetail(
                amount=amount,
                subtotal=subtotal,
                inventory_id=inventory_id,
                domicilie_id=domicilie.id,
                user_id=user
            )

            inventory.amount -= amount
            inventory.save()
            domicilie_detail.save()
        
        return redirect('domicilie')

    return redirect('domicilie')


def cancel(request):
    if request.method == 'POST':
        domicilie_id = request.POST.get('domicilie')

        # Obtener el objeto de la categoría a editar
        domicilie = get_object_or_404(Domicilies, id=domicilie_id)
        
        # Actualizar los datos
        domicilie.state = 'Cancelado'
        domicilie.save()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('domicilie')
    else:
        return JsonResponse({'error': 'Método no permitido'})

def assign_domicilies(request):
    title = 'Asignar Domicilios'
    form = Assign()
    domicilies = AssignDomicilies.objects.all()
    return render(request, 'admin/my_domicilies.html', {'title': title, 'domicilies': domicilies, 'form': form})

def assign(request):
    if request.method == 'POST':
        domicilie_id = request.POST['domicilie_id']
        user_id = request.POST['user_id']
        if domicilie_id:
            assign = AssignDomicilies(
                domicilie_id=domicilie_id,
                user_id=user_id,
            )
            assign.save()
            # Puedes redirigir a una página de éxito o hacer lo que necesites aquí.
            return redirect('assign_domicilies')  # Cambia 'exito' por la URL a la que deseas redirigir.
        # Si los datos del formulario no son válidos, puedes manejar los errores aquí.
    return render(request, 'admin/my_domicilies.html')  # Cambia 'tu_template.html' por el nombre de tu plantilla modal.

def my_domicilies(request):
    title = 'Mis Domicilios'
    user = request.user.id
    domicilies = AssignDomicilies.objects.filter(user_id=user)
    return render(request, 'domicilier/domicilies.html', {'title': title, 'domicilies': domicilies})

def complete(request):
    if request.method == 'POST':
        domicilie_id = request.POST.get('domicilie')

        # Obtener el objeto de la categoría a editar
        domicilie = get_object_or_404(Domicilies, id=domicilie_id)
        
        # Actualizar los datos
        domicilie.state = 'Entregado'
        domicilie.save()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('my_domicilies')
    else:
        return JsonResponse({'error': 'Método no permitido'})


def domicilies_user(request):
    title = 'Domicilios'
    user = request.user.id
    domicilies = Domicilies.objects.filter(user_id=user)
    return render(request, 'user/domicilies.html', {'title': title, 'domicilies': domicilies})
