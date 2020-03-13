from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TextEquation
from .traph import grapher, file_numberer    # The functions that will graph the equation and tell us the number
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Graph

def calculator(request):

    if request.method == 'POST':

        form = TextEquation(request.POST)
        if form.is_valid():
            equation = form.cleaned_data.get('equation') # Getting the equation that the user had written
            image_number = file_numberer.get_number()    # Getting the number

        if ("x" in equation) and ("exit" not in equation) and ("quit" not in equation):         # Making sure no one wants to put mischievous functions ;)
            try:                                          # Making sure the funcion is correct
                grapher.graph_it(equation, request.user.is_authenticated)                # Graphing the function
                if request.user.is_authenticated:
                    graph_history = Graph(name=f'graph{image_number}', image=f'calculator/saved_graphs/graph{image_number}.png', author=request.user)
                    graph_history.save()
                    static_media = 'media'
            except Exception:
                image_number += 1                         # As the graph doesn't exist, the alt message of <img> will appear
                static_media = 'static'
        else:
            image_number += 1                             # As the graph doesn't exist, the alt message of <img> will appear
            static_media = 'static'

    else:                                                 # Defualt settings
        form = TextEquation()
        equation = 'null'
        image_number = 3
        static_media = 'static'



    return render(request, 'calculator/calculator.html', {'form': form, "equation": equation, 'image_number': image_number, 'static_media':static_media})


def register(request):

    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)

        if register_form.is_valid():
            register_form.save()                                                # Saving the user
            username = register_form.cleaned_data.get('username')
            messages.success(request, f'{username} has been succesfuly created! Log in to continue.')
            return redirect('GraphingCalculator')


    else:
        register_form = UserCreationForm()

    return render(request, 'calculator/register.html', {'register_form': register_form})

@login_required
def profile(request):
    current_user = request.user
    graphs_images = current_user.graph_set.all()
    graphs_images = reversed(graphs_images)
    return render(request, 'calculator/profile.html', {'graphs_url':graphs_images})
