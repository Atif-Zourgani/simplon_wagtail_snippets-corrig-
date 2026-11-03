



from wagtail.models import Page
from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
# register snippet: transforme le modele django classique en snippet wagtail
from modelcluster.fields import ParentalKey
#(ici, les champs du formulaire appartiennent a une page Contact precise)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField

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
        
class FormField(AbstractFormField):
    # AbstractFormField fournit deja tout ce qu'il faut pour decrire UN champ
    # quelconque (label, type de champ, obligatoire ou non...). On ajoute juste
    # le lien vers la page Contact. Les vrais champs (Nom, Email, Message) ne sont
    # PAS ecrits ici : ils seront crees comme des donnees, depuis l'admin (etape 5).
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,   # si la page Contact est supprimee, ses champs le sont aussi
        related_name="form_fields",
    )

class ContactPage(AbstractEmailForm):
    # On remplace Page par AbstractEmailForm : ContactPage reste une page (AbstractEmailForm
    # herite de Page), mais une page qui sait aussi envoyer un email a chaque reponse.
    intro = RichTextField(blank=True)          # texte affiche au-dessus du formulaire
    thankyoutext = RichTextField(blank=True)  # message affiche apres l'envoi
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Champs du formulaire"),
        # InlinePanel : widget d'admin qui affiche la liste des FormField de cette page,
        # avec un bouton pour en ajouter, en retirer, ou changer leur ordre
        FieldPanel("thankyoutext"),
        FieldPanel("to_address"),    # l'email de Max, qui recevra chaque message
        FieldPanel("from_address"),  # l'adresse "expediteur" affichee sur l'email recu
        FieldPanel("subject"),       # le sujet de l'email envoye
    ]

class CoachsIndexPage(Page):

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro")
    ]

    # sous cette page on ne pourras ajouter que des fiches de coach 
    subpage_types = ["pages.CoachProfilPage"]

    # va contenir des fiche coach enfant et quand on l'affiche,
    # va les chercher pour les afficher 

    def get_context(self, request):
        context = super().get_context(request)
        context["coachs"] = CoachProfilPage.objects.child_of(self).live()

        return context  

class CoachProfilPage(Page):

    specialite = models.CharField(max_length=100, blank=True)
    nom = models.CharField(max_length=50)
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
        )
    bio = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("specialite"),
        FieldPanel("nom"),
        FieldPanel("photo"),
        FieldPanel("bio")
    ]

    parent_page_types = ["pages.CoachsIndexPage"]
