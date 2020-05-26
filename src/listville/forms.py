from django import forms

class CountryForm(forms.Form):
	OPTIONS = (("Casablanca","Casablanca"),("Beni-Mellal","Beni-Mellal"),("Meknes","Meknes"),("Marrakesh","Marrakesh"),("Larache","Larache"),("Fes","Fes"),("Mohammedia","Mohammedia"),("Midelt","Midelt"),("El Hoceima","El Hoceima"),("Tangier","Tangier"),("Rabat","Rabat"),("Agadir","Agadir"),("Essaouira","Essaouira"),("Tetouan","Tetouan"),("Sidi Slimane","Sidi Slimane"),("Chefchaouen","Chefchaouen"),("Kenitra","Kenitra"),("Ifran","Ifran"),("Nador","Nador"),("Taroudant","Taroudant"),("Settat","Settat"),("Guelmim","Guelmim"),("Khouribga","Khouribga"),)
	countries = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={
		'id':'form-control','size': 5,
		}),choices=OPTIONS
		)