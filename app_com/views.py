from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Appointment
from .forms import ContactForm
from django.http import JsonResponse
from django.utils.timezone import datetime
from django.core.mail import send_mail
from django.conf import settings
from .email_utils import send_acs_email

# Liste des créneaux horaires disponibles par défaut
DEFAULT_SLOTS = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"]



# Create your views here.
def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html")

def contact(request):
    message = None

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            budget = form.cleaned_data['budget']
            message_text = form.cleaned_data['message']

            print(f"Nom: {name}, Téléphone: {phone}, Email: {email}, Budget: {budget}, Message: {message_text}")

            subject = "[BEGIN SITE WEB] Nouveau message"
            body = f"""
            Vous avez reçu un nouveau message via le formulaire de contact :
            
            Nom: {name}
            Téléphone: {phone}
            Email: {email}
            Budget: {budget}
            Message:
            {message_text}
                        """

            recipient = "agence@begin-career.com"  # Adresse destinataire

            email_id = send_acs_email(recipient, subject, body)
            if email_id:
                message = "✅ Votre message a été envoyé avec succès !"
                #form.save()
            else:
                message = "❌ Une erreur est survenue lors de l'envoi de l'e-mail."

        else:
            errors = " ".join([f"{field}: {error}" for field, errors in form.errors.items() for error in errors])
            message = f"❌ Une erreur est survenue. Vérifiez vos informations. {errors}"

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, 'message': message})
def service_detail(request, service_name):
    # Dictionnaire des services avec leurs images et descriptions
    services = {
        "social-media": {
            "title": "Social Media Strategy & Design",
            "image": "services/social_media.jpg",
            "video": "https://begincareer.blob.core.windows.net/begincareer/sociale_media.mp4",
            "sub_services": [
                {
                    "name": "Social Media & Community Management",
                    "description": "Nous prenons en charge la gestion complète de vos réseaux sociaux afin d’optimiser votre visibilité et engagement. Chaque plateforme a ses codes, et nous adaptons les stratégies pour maximiser votre impact digital.",
                    "points": [
                        "Élaboration et mise en place de stratégies social media.",
                        "Gestion quotidienne des comptes (publications, stories, interactions).",
                        "Analyse des performances et optimisation continue.",
                        "Veille digitale et adaptation aux tendances du marché.",
                        "Élaboration d’une ligne éditoriale cohérente.",
                        "Création de contenus engageants adaptés aux tendances digitales.",
                    ],
                },
                {
                    "name": "Direction Artistique",
                    "description": "Chaque marque a une identité unique, et notre rôle est de la sublimer à travers un univers visuel qui vous correspond. Nous conceptualisons et produisons des contenus, en parfaite adéquation avec l’ADN de la marque.",
                    "points": [
                        "Conception de moodboards et univers graphiques.",
                        "Production et direction artistique de shootings photo & vidéo.",
                        "Développement d’une charte visuelle distinctive et impactante.",
                    ],
                },
                {
                    "name": "Création & Production de Contenus",
                    "description": "Nous orchestrons la production de contenus premium, en accord avec l’image et les ambitions de la marque. Notre approche est à la fois stratégique et esthétique, garantissant une communication cohérente et puissante.",
                    "points": [
                        "Design graphique et création visuelle.",
                        "Production de campagnes digitales et vidéos immersives.",
                        "Élaboration de calendriers marketing & éditoriaux.",
                    ],
                },
            ],
        },
        "styling": {
            "title": "Styling and Image",
            "image": "services/styling.png",
            "video": "https://begincareer.blob.core.windows.net/begincareer/styling_and_image.mp4",
            "sub_services": [
                {
                    "name": "Stylisme & Sélection de Looks",
                    "description": "Nous habillons nos clients pour tous types d’événements, en sélectionnant des tenues adaptées à leur image et à l’occasion. Chaque look est pensé avec soin pour refléter leur personnalité et leur style",
                    "points": [
                        "<strong>Red carpets, Fashion Weeks, événements privés et professionnels.</strong>",
                        "<strong>Shooting photos, clips, apparitions médiatiques.</strong>",
                        "<strong>Sélection exclusive de pièces issues en collaboration avec nos marques partenaires.</strong>",
                    ],
                },
                {
                    "name": "Expérience sur-mesure & Accès exclusif",
                    "description": "Nous vous offrons un service <strong>clé en main.</strong>",
                    "points": [
                        "Organisation et coordination des <strong>fittings privés et essayages sur-mesure.</strong>",
                        "<strong>Gestion complète des looks</strong> (tenues, accessoires, ajustements, logistique).",
                    ],
                },
                {
                    "name": "Image & Signature Visuelle",
                    "description": "Au-delà du stylisme, nous aidons nos clients à construire <strong>une image forte et reconnaissable</strong>, qui s’inscrit dans la durée.",
                    "points": [
                        "Sélection de <strong>photographes, directeurs artistiques et créateurs de contenu</strong> pour mettre en valeur chaque look.",
                        "Accompagnement pour <strong>créer une cohérence stylistique</strong> à travers leurs apparitions et prises de parole publiques.",

                    ],
                },
            ],
        },
        "fashion-week": {
            "title": "Vip & Celebrities placement",
            "image": "services/fashion_week.png",
            "video": "https://begincareer.blob.core.windows.net/begincareer/vip_access.mp4",
            "sub_services": [
                {
                    "name": "Celebrites placement",
                    "description": "De la sélection des talents à la coordination avec les marques, nous assurons un service clé en main :",
                    "points": [
                        "<strong>Styling sur mesure</strong>  en collaboration directe avec les maisons et créateurs.",
                        "<strong>Organisation logistique complète</strong>  : hôtel, transferts privés, mise à disposition de véhicules avec chauffeur.",
                        "<strong>Couverture média sur place</strong>  : photographe et vidéaste pour capturer chaque instant.",
                        "Notre expertise permet de créer des apparitions marquantes qui renforcent autant l’image des talents que celle des marques qu’ils représentent.Chaque détail compte : nous garantissons une expérience fluide, élégante et parfaitement alignée avec l’ADN de l’événement.",

                    ],
                },

            ],
        },
    }


    # Vérifie si le service existe, sinon affiche une page 404
    service_data = services.get(service_name)
    if not service_data:
        return render(request, '404.html', status=404)

    # Passer les données du service au template
    return render(request, 'service_detail.html', {"service": service_data})

def get_available_slots(request):
    date = request.GET.get("date")
    if not date:
        return JsonResponse({"error": "Aucune date fournie"}, status=400)

    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Format de date invalide"}, status=400)

    # Récupérer les créneaux déjà réservés
    booked_slots = Appointment.objects.filter(date=selected_date).values_list("time_slot", flat=True)

    # Filtrer les créneaux disponibles
    available_slots = [slot for slot in DEFAULT_SLOTS if slot not in booked_slots]

    return JsonResponse({"slots": available_slots})
