from django.db import models

# Create your models here.
class Ville(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	Nature = 'Nature'
	Architecture = 'Architecture'
	Plages = 'Plages'
	Aventure = 'Aventure'
	désert = 'désert'
	ville_types = [(Nature, 'Nature'),
				  (Architecture, 'Architecture'),
				  (Plages,'Plages'),
				  (Aventure, 'Aventure'),
				  (désert, 'désert')]
	typeV = models.CharField(max_length=50,
							choices=ville_types,
							default=Plages)
	photo = models.ImageField(upload_to='villes_images',blank=True)

	

	def  __str__(self):
		return self.name
