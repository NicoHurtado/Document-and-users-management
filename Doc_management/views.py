from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Estudiante, Taller




def home(request):
	Estudiantes = Estudiante.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'Estudiante':Estudiantes})


def estudiantes_por_taller(request, taller_id):
    taller = Taller.objects.get(nombre=taller_id)
    estudiantes = Estudiante.objects.filter(taller=taller)
    return render(request, 'home.html', {'taller': taller, 'Estudiante': estudiantes})


def search(request):
    query = request.GET.get('query')
    estudiantes = Estudiante.objects.filter(nombre__icontains=query)
    return render(request, 'home.html', {'estudiantes': estudiantes, 'query': query})

def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


def loginAdmin(request):
    # Define un diccionario de usuarios permitidos para acceder al registro
    usuarios_permitidos = {
        'cesarherrera': 'fontan123',
        'usuario2': 'password2',
        'usuario3': 'password3',
        'usuario4': 'password4',
        'usuario5': 'password5',
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username in usuarios_permitidos and usuarios_permitidos[username] == password:
            # Si el usuario está en el diccionario y la contraseña coincide, permite el acceso
            return render(request, 'register.html')
        else:
            # Si el usuario no está en el diccionario o la contraseña no coincide, muestra un mensaje de error
            error_message = 'Usuario o contraseña incorrectos.'
            return render(request, 'home.html', {'error_message': error_message})

    # Si la solicitud es GET (no se ha enviado un formulario), renderiza la página de inicio de sesión
    return render(request, 'loginAdmin.html')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        
        estudiante = Estudiante.objects.get(id=pk)
        
        
        

        
        dbx = dropbox.Dropbox(TOKEN)

        
        carpeta = '/' + estudiante.cedula  
        
        try:
            
            result = dbx.files_list_folder(carpeta)
            archivos = []
            
            for entry in result.entries:
                
                shared_link_metadata = dbx.sharing_create_shared_link(carpeta + '/' + entry.name)
                shared_link = shared_link_metadata.url
                
                
                archivos.append({'nombre': entry.name, 'enlace_compartido': shared_link})
            
            
            return render(request, 'record.html', {'Estudiante': estudiante, 'Archivos': archivos})
        
        except dropbox.exceptions.ApiError as err:
            
            messages.error(request, f'Error al listar archivos en Dropbox: {err}')
            return render(request, 'record.html', {'Estudiante': estudiante, 'Archivos': None})
        
    else:
        #
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')





def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Estudiante.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


def add_record(request):
	form = AddRecordForm(request.POST or None, request.FILES or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				new_record = form.save(commit=False)

				new_record.save()

				document = request.FILES.get('document')
				if document:
					try:

						dbx = dropbox.Dropbox(TOKEN)

						carpeta = '/' + new_record.cedula

						try:
							dbx.files_create_folder(carpeta, autorename=False)
						except dropbox.exceptions.ApiError as api_err:
							if api_err.error.is_path() and api_err.error.get_path().is_conflict():

								pass
							else:

								raise

						dbx.files_upload(document.file.read(), carpeta + '/' + document.name)

						messages.success(request, "Documento subido correctamente a Dropbox.")
					except dropbox.exceptions.ApiError as err:
						messages.error(request, f'Error al subir el documento a Dropbox: {err}')

				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form': form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')


def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Estudiante.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, request.FILES or None, instance=current_record)
		if form.is_valid():

			updated_record = form.save(commit=False)

			updated_record.save()

			document = request.FILES.get('document')
			if document:
				try:

					dbx = dropbox.Dropbox(TOKEN)

					carpeta = '/' + updated_record.cedula

					try:
						dbx.files_create_folder(carpeta, autorename=False)
					except dropbox.exceptions.ApiError as api_err:
						if api_err.error.is_path() and api_err.error.get_path().is_conflict():

							pass
						else:

							raise

					dbx.files_upload(document.file.read(), carpeta + '/' + document.name)

					messages.success(request, "Documento subido correctamente a Dropbox.")
				except dropbox.exceptions.ApiError as err:
					messages.error(request, f'Error al subir el documento a Dropbox: {err}')

			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form': form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
