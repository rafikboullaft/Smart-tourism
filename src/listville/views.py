from django.shortcuts import render
from listville.forms import CountryForm, ContactForm, num_jours, mot_cle
import random
from itertools import combinations
import pandas as pd
import numpy as np
import json
from .models import Ville
import googlemaps
from itertools import combinations
from django.core.mail import EmailMessage
from mysite.settings import EMAIL_HOST_USER
#librerary 
# Create your views here.
countries = []
mes_villes = []
def display_destination_villes(request): 

    if request.method == "POST":
        form = CountryForm(request.POST)
        if form.is_valid():
            countries = form.cleaned_data.get('countries')
            pass
        pass
    else:
        form = CountryForm
        villes = Ville.objects.all()
    return render(request, 'display_villes.html', {'form': form, 'display_villes' : villes} )
def webpage1(request):
	if request.method == "POST":
		form = CountryForm(request.POST)
		if form.is_valid():
			countries = form.cleaned_data.get('countries')
	else:
		form = CountryForm
	return render(request,'display_villes.html', {'form': form})

def webpage2(request):
    countries = []
    mylist = []
    global mes_villes
    if request.method == "POST":
        villes = Ville.objects.all()
        form = CountryForm(request.POST)
        if form.is_valid():
            countries.append(form.cleaned_data.get('countries'))
            mes_villes = countries[0]
            #print(f" countries :{countries}")
            # do something with your results
            mylist = genetique_algo(generations = 5000, population_size= 100)
    else:
        form = CountryForm
        villes = Ville.objects.all()
    return render(request, 'yourtrip.html', {'form': form, 'countries':mes_villes, 'mylist':mylist, 'display_villes' : villes} )
    
def contact_us(request):
    sub = ContactForm
    if request.method == "POST":
        sub = ContactForm(request.POST)
        if sub.is_valid():
          sujet = sub.cleaned_data.get('Sujet')
          message = sub.cleaned_data.get('Message')
          recepient = sub.cleaned_data.get('Email')
          messagefinale = "Email: " + recepient + " \n" + message
          msg = EmailMessage(sujet,
                       messagefinale, to=['rafik.boullaft@etu.uae.ac.ma'])
          msg.send()
          return render(request, 'contact.html',{'message':message, 'subject': sujet,'form':sub})
    return render(request, 'contact.html',{'form':sub})


def visites_par_jours(request):
    if request.method == "POST":
        form = num_jours(request.POST)
        if form.is_valid():
            numm = int(form.cleaned_data.get('N_jours'))
            if numm < 4:
                optimal_chemin = ['Marrakesh','Ouarzazate','Merzouga','Fes']
            elif numm <8 and numm >3:
                optimal_chemin = ['Tangier','Chefchaouen', 'Fes','Merzouga','Ouarzazate','Marrakesh']
            elif numm > 7 and numm<10:
                optimal_chemin = ['Casablanca','Rabat','Meknes','Fes','Merzouga','Ouarzazate','Marrakesh']
            else :
                optimal_chemin = ['Tangier','Chefchaouen', 'Fes','Merzouga','Ouarzazate','Marrakesh','Essaouira','Casablanca','Rabat']

            return render(request, 'visites_par_jours.html',{'optimal_chemin': optimal_chemin,'selectform':form,'numselect':numm})
    else:
        form = num_jours

    return render(request, 'visites_par_jours.html',{'selectform':form})
def palce_proche(request):
    if request.method == "POST":
        form = mot_cle(request.POST)
        if form.is_valid():
            lemot = form.cleaned_data.get('mot_cle')
            return render(request, 'palce_proche.html',{'form':form,'lemot':lemot})
    else:
        form = mot_cle
    return render(request,'palce_proche.html',{'form':form})
#THIS BlOCK IF YOU WANT PREPARE YOUR OWN DATA 
# change this list with your locations 


# villes = ["Casablanca","Beni-Mellal","Meknes","Marrakesh","Larache","Fes","Mohammedia","Midelt","El Hoceima","Tangier","Rabat","Agadir","Essaouira","Tetouan","Sidi Slimane","Chefchaouen","Kenitra","Ifran","Nador","Taroudant","Settat","Guelmim","Khouribga",
#           "Dakhla","Laayoune","Al Mahbes","Saidia","Zagora","Merzouga","Ouarzazate","Awsard","Moulay Idriss Zerhoun","Tarfaya","Lagouira","Oujda"]
# gm_api = googlemaps.Client(key="YOUR-KEY")
# distance_villes = {}
# duree_villes ={}
# # calculer la distance et la duree entre chaque villes en mode "driving" avec le service distance_matrix de google maps
# for (ville1, ville2) in combinations(villes, 2):
#   route = gm_api.distance_matrix(origins=[ville1],
#                                  destinations=[ville2],
#                                  mode="driving",
#                                  language="English",
#                                  units="metric")
#   #retourn une valeur (distance entre 2 villes) en metres
#   distance = route['rows'][0]['elements'][0]['distance']['value']
#   #retourn une valeur (duree entre 2 villes) en seconds
#   duree = route['rows'][0]['elements'][0]['duration']['value']

#   #stocker ses valeur dans un set
#   distance_villes[frozenset([ville1,ville2])] = distance
#   duree_villes[frozenset([ville1,ville2])] = duree
# # stocker notre sets dans un seul fichier tsv
# with open("mes_villes_dist_dur.tsv", "w") as mes_villes:
#   mes_villes.write("\t".join(["ville1","ville2","distance_m","duree_s"]))
#   for (ville1, ville2) in distance_villes.keys():
#     #stockage sou forme ville1\ville2\dist_m\dur_s
#     #transformer la distance et la duree a une chaine de character
#     mes_villes.write("\n" +
#                        "\t".join([ville1,
#                                   ville2,
#                                   str(distance_villes[frozenset([ville1, ville2])]),
#                                   str(duree_villes[frozenset([ville1, ville2])])])) 

distance_villes = {}
duree_villes ={}
#list ==> set 
countries = set()
#tsv file ==> dataframe avec pandas
villes_data = pd.read_csv("mes_villes_dist_dur.tsv", sep="\t")

for i, row in villes_data.iterrows():
  distance_villes[frozenset([row.ville1, row.ville2])] = row.distance_m
  duree_villes[frozenset([row.ville1, row.ville2])] = row.duree_s
  countries.update([row.ville1, row.ville2])



# ## 
def compute_fitness(solution):
  """ cette function return la distance totale du chemin courant entre les villes"""
  solution_fitness = 0.0
  for i in range(len(solution)):
    ville1 = solution[i - 1]
    ville2 = solution[i]
    solution_fitness += distance_villes[frozenset([ville1, ville2])]
  return solution_fitness

#### choix aleatoire
def chemin_aleatoire():
  """ creer un chemin aleatoire par l'ensembles des villes donnees """
  global mes_villes
  new_chemin = mes_villes
  # melanger notre list
  random.shuffle(new_chemin)
  return tuple(new_chemin)
#### mutation 1 : echange
def mutation_agent(agent_genome, max_mutaions=3):
  """ faire l echange au max de 3 villes dans notre set """
  agent_genome = list(agent_genome)
  num_mutation = random.randint(1,max_mutaions)
  for mut in range(num_mutation):
    index_echange1 = random.randint(0,len(agent_genome)-1)

    index_echange2 = index_echange1
    # pour eviter de choisir le meme index
    while index_echange1 == index_echange2:
      index_echange2 = random.randint(0,len(agent_genome)-1)
    # faire l'echange
    agent_genome[index_echange1], agent_genome[index_echange2] = agent_genome[index_echange2], agent_genome[index_echange1]
  
  return tuple(agent_genome)

#### mutation 2 : melange 
def melange_mutation(agent_genome):
  """
   couper une sous list de taille aleatoire et la deplacer a un autre index aleatoire
  """
  agent_genome = list(agent_genome)

  debut = random.randint(0, len(agent_genome)-1)
  fin = debut + random.randint(2,10)

  sous_genome = agent_genome[debut:fin]
  agent_genome = agent_genome[:debut] + agent_genome[fin:]

  index_insertion = random.randint(0,len(sous_genome) + len(agent_genome)-1)
  #index_insertion = random.randint(0,len(agent_genome)-1)
  agent_genome = agent_genome[:index_insertion] + sous_genome + agent_genome[index_insertion:]
  return tuple(agent_genome)

##### generer une population de differents chemin

def generate_random_population(population_size):
  random_population = []
  for agent in range(population_size):
    random_population.append(chemin_aleatoire())
  return random_population

# ##### pour visualiser les resultats

progress_visualisation_y = []
progress_visualisation_x = []

# #####

def genetique_algo(generations = 5000, population_size= 100):
  """ fonction main de l algorithme genetique """
  population_subset_size = int(population_size/10)
  generation_sub = int(generations/10)
  # creer une population
  population = generate_random_population(population_size)

  

  for generation in range(generations):
    # calculer la distance entre les villes de tout la population
    population_fitness = {}

    for agent_genome in population:
      if agent_genome in population_fitness:
        continue
      population_fitness[agent_genome] = compute_fitness(agent_genome)
    
    # prendre 10% de la population qui a le chemin le optimale et produire une offspring chacun d'eux
    new_population = []
    for rank, agent_genome in enumerate(sorted(population_fitness, key=population_fitness.get)[:population_subset_size]):
      if (generation % generation_sub == 0 or generation == generations -1 ) and rank == 0:
        print(f"Generation: {generation}, optimal chemin: {population_fitness[agent_genome]} m | unique genomes: {len(population_fitness)}")

        progress_visualisation_y.append(population_fitness[agent_genome])
        progress_visualisation_x.append(generation)

        print(agent_genome)
        print("--------------------------------------------------")
      #### faire les mutation pour la 10% de la population
      # creer une copie pour chaque chemin selectee
      new_population.append(agent_genome)
      # mutation 1 : creer 2 offspring par la mutation d'echange
      for i in range(2):
        new_population.append(mutation_agent(agent_genome, 3))
      
      # mutation 2 : creer 7 offspring par la mutaion de melange
      for i in range(7):
        new_population.append(melange_mutation(agent_genome))
      
      # remplacer population ==> new population de offspring
    for i in range(len(population))[::-1]:
      del population[i]
    population = new_population
  print("================ chemin optimal ================")
  print(agent_genome)
  print("==================================================")
  return list(agent_genome)