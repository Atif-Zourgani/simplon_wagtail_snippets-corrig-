



from wagtail.models import Page
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
# register snippet: transforme le modele django classique en snippet wagtail


class CoachPage(Page):
    photo = models.ForeignKey(
        "wagtailimages.Image", #pointer vers la biblio d'images wagtail
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  #si l'img est supprimée, le champs redevient vide 
        related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel("photo")
    ]

@register_snippet # je déclare mon DECORATEUR snippet
class Cours(models.Model): #dit a wagtail que ce model doit apparaitre dans l'admin et etre administrable avec form
    
    # defini le contenu de mon model (= moule = template)
    nom = models.CharField(max_length=100)
    horaire = models.CharField(max_length=100, blank=True)
    niveau = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    panels = [
        FieldPanel("nom"),
        FieldPanel("horaire"),
        FieldPanel("niveau"),
        FieldPanel("description")
        #liste les champs visible dans le form admin de CE snippet
        #panels et pas content panel parcequ'un snippet n'est pas une page -> ca exclu donc le slug, le btn publié etc
    ]

    # donne la valeur dans la variable "nom", aux snippets qu'on va créer'
    def __str__(self):
        return self.nom

       
class CoursPage(Page):
    def get_context(self, request):
        #get context permet de construire les données envoyées à cette page
        context = super().get_context(request)
        context["cours_list"] = Cours.objects.all()
        return context #renvois le dictionnaire complet 
        


class ContactPage(Page):
    pass
