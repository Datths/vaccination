#!/usr/bin/env python
# coding: utf-8

# ## Welcome to your notebook.
# 

# #### Run this cell to connect to your GIS and get started:

# In[1]:


from arcgis.gis import GIS
gis = GIS("home") #On importe l'API et on se connecte sur le portail
"""Connexion successed"""


# In[2]:


import json #Pour manipuler le json
import urllib.request as urllib #Pour ouvrir une page internet
import pandas as pd
#import geojson #Pour JSON to GeoJSON Ne fonctionne pas, il faut télécharger le module sur \arcgis
from arcgis.mapping import WebMap #Pour la carte web

from arcgis.geometry import Point, Polyline, Polygon, Geometry #Pour dessiner les points
from arcgis.features import Feature #Pour Feature
from arcgis.features import FeatureSet
"""Modules importés"""


# In[3]:


'''Récupération des données depuis le json hébergé sur le site data.gouv'''
req = urllib.Request("https://www.data.gouv.fr/fr/datasets/r/d0566522-604d-4af6-be44-a26eefa01756") #on nomme la requête
ouverture = urllib.urlopen(req) ##on ouvre le lien
data_gouv = json.loads(ouverture.read()) #le fichier json est dans la variable data_gouv sous la forme d'un dictionnaire

"""Requête effectuée et import des données fait"""


# In[4]:


"""Création de la dataframe"""
df = pd.DataFrame(data_gouv["features"]) #presente sous la forme d'un tableau panda l'ensemble des données (features)
nbft = len(df) #Nombre d'entités a réutiliser dans la boucle pour créer les points
print('Il y a {} lignes'.format(nbft)) # On affiche le nombre de lignes
print("le nom des colonnes est :",str(df.columns.tolist())) #affiche le nom des colonnes de df
print("le type de df est: ",type(df))
"""Dataframe de longueur nbft créée"""


# In[5]:


"""Nomenclature des données de la df"""
typ = df['type']
#print(typ)
print("le type de type est :", type(typ),"\n")

###Properties
pro = df['properties']
print("le type de pro est:", type(pro))
print("Propriétés de la première entité :",pro[0],"\n")

###Geometry
geo = df['geometry']
#dfgeo = pd.DataFrame(geo)
print("le type de géo est:", type(geo),"\n") #Series c'est une liste
print(geo[0],"le type de geo[0] est :",type(geo[0]),"\n") #C'est un dictionnaire python
print(geo[0]['coordinates'],"le type de geo[0]['coordinates'] est :", type(geo[0]['coordinates']),"\n") #C'est une liste python

"""properties et geography enregistrées dans pro et geo"""


# In[6]:


"""Ouverture de la couche à modifier"""
#access the item's feature layers
items = gis.content.search("title:Couche Donnees Centres Vaccination Gouv")
item = items[0]
mylayer = item.layers[0]
type(mylayer)
#mylayer.properties.capabilities
"""Couche d'entité ouverte"""


# In[7]:


"""Suppression des anciens points"""
#mylayer.manager.truncate()
mylayer.delete_features(where="objectid > 0")
"""La carte a été nettoyée"""


# In[8]:


"""Création des points"""
###Après avoir nettoyé le feature layer on peut recréer les points
###Attention pour que les attributs s'affiches on a d'abord créé les champs manuellement
###Attention à la taille des champs exemple pour le gid 347 de cgid 491 qui a bcp de caractere en rdv modalité
### On ne peut donc pas inclure les modalités de rdv tant que cet item n'est pas modifié

#for i in range(nbft): #on va faire 0 jusqu'à nbft -1

centres = []
for i in range(nbft): #On fait tourner le code avec toutes les lignes de la dataframe
#for i in range(300,370): ###Tester avec quelques valeurs
    coord = geo[i]['coordinates'][0]# On affiche les i premières coordonnées des centres
    x = coord[0]
    y = coord[1]
    pt = Point({"x" : x, "y" : y, "spatialReference" : {"wkid" : 4326}})# on crée le point #En mettant 3857 on a pas du tout les bons points 
    #attribut1 = {"nom" : "c_nom","gid" : "100","tag":"test"} #On nomme les attributs ligne à remplacer par properties
    attribut = pro[i] #Si les champs existent sur le layers ils vont être remplis par les données de pro[i]
    ft = Feature(attributes = attribut, geometry = pt) #On crée l'entité avec la fonction feature qui emporte la localisation et les attributs
    #display(ft) #affiche les features nouvellement créés 1 par 1
    centres.append(ft) #On ajoute l'entité à la liste

#print(centres[:2])
#print(len(centres))
    
# Ne pas tenir compte des problème d'encoding dans les lignes suivantes
"""Les points ont été créés"""


# In[9]:


"""Publication de la data"""
add_result = mylayer.edit_features(adds = centres)
display(add_result)
#centres_fset = FeatureSet(features = features, geometry_type="Point", spatial_reference={'latestWkid': 4326, 'wkid': 102100})
#{"wkid": 102100, "latestWkid": 3857}}


# In[10]:


"""Affichage de la table pour vérification"""
fset_edited = mylayer.query()
fset_edited.sdf


# In[ ]:




