from django import forms

class CountryForm(forms.Form):
	OPTIONS = (("Casablanca","Casablanca"),("Beni-Mellal","Beni-Mellal"),("Meknes","Meknes"),("Marrakesh","Marrakesh"),
		("Larache","Larache"),("Fes","Fes"),("Mohammedia","Mohammedia"),("Midelt","Midelt"),("El Hoceima","El Hoceima"),
		("Tangier","Tangier"),("Rabat","Rabat"),("Agadir","Agadir"),("Essaouira","Essaouira"),("Tetouan","Tetouan"),
		("Sidi Slimane","Sidi Slimane"),("Chefchaouen","Chefchaouen"),("Kenitra","Kenitra"),("Ifran","Ifran"),("Nador","Nador"),
		("Taroudant","Taroudant"),("Settat","Settat"),("Guelmim","Guelmim"),("Khouribga","Khouribga"),("Dakhla","Dakhla"),
		("Laayoune","Laayoune"),("Al Mahbes","Al Mahbes"),("Saidia","Saidia"),("Zagora","Zagora"),("Merzouga","Merzouga"),
		("Ouarzazate","Ouarzazate"),("Awsard","Awsard"),("Moulay Idriss Zerhoun","Moulay Idriss Zerhoun"),("Tarfaya","Tarfaya"),
		("Lagouira","Lagouira"),("Oujda","Oujda"),)
	countries = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={
		'id':'form-control','size': 10,
		}),choices=OPTIONS
		)

class ContactForm(forms.Form):
	Sujet = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control input-custom input-full','placeholder':'sujet'}))
	Email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control input-custom input-full','placeholder':'Email'}))
	Message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control textarea-custom input-full','id':'ccomment','row':'8','placeholder':'Message'}))
	# def __str__(self):
	# 	return self.Email
class num_jours(forms.Form):
	OPTIONS = (("1","1 Jour"),("2","2 Jours"),("3","3 Jours"),("4","4 Jours"),("5","5 Jours"),("6","6 Jours"),("7","7 Jours"),("8","8 Jours"),
		("9","9 Jours"),("10","10 Jours"),("11","11 Jours"),("12","12 Jours"),("13","13 Jours"),("14","14 Jours"),("15","15 Jours"),)
	N_jours = forms.ChoiceField(required=True, choices=OPTIONS)
class mot_cle(forms.Form):
	mot_cle = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder':'Que cherchez-vous?'}))