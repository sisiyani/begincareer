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

            # Affichage des données dans la console (logs serveur)
            print(f"Nom: {name}")
            print(f"Téléphone: {phone}")
            print(f"Email: {email}")
            print(f"Budget: {budget}")
            print(f"Message: {message_text}")
            # Envoi de l'e-mail
            subject = "[BEGIN SITE WEB] Nouveau message "
            body = f"""
            Vous avez reçu un nouveau message via le formulaire de contact :

            Nom: {name}
            Téléphone: {phone}
            Email: {email}
            Budget: {budget}
            Message:
            {message_text}
            """
            recipient_list = ["agence@begin-career.com"]  # Mets ici l'adresse qui doit recevoir l'email

            try:
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipient_list)
                message = "✅ Votre message a été envoyé avec succès !"
                form.save()
            except Exception as e:
                print(f"Erreur d'envoi d'email: {e}")
                message = "❌ Une erreur est survenue lors de l'envoi de l'e-mail."

        else:
            # Gestion des erreurs
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
                    "name": "{% trans 'Social Media & Community Management' %}",
                    "description": "{% trans 'Nous prenons en charge la gestion complète de vos réseaux sociaux afin d’optimiser votre visibilité et engagement. Chaque plateforme a ses codes, et nous adaptons les stratégies pour maximiser votre impact digital.' %}",
                    "points": [
                        "{% trans 'Élaboration et mise en place de stratégies social media.' %}",
                        "{% trans 'Gestion quotidienne des comptes (publications, stories, interactions).' %}",
                        "{% trans 'Analyse des performances et optimisation continue.' %}",
                        "{% trans 'Veille digitale et adaptation aux tendances du marché.' %}",
                        "{% trans 'Élaboration d’une ligne éditoriale cohérente.' %}",
                        "{% trans 'Création de contenus engageants adaptés aux tendances digitales.' %}",
                    ],
                },
                {
                    "name": "{% trans 'Direction Artistique",
                    "description": "{% trans 'Chaque marque a une identité unique, et notre rôle est de la sublimer à travers un univers visuel qui vous correspond. Nous conceptualisons et produisons des contenus, en parfaite adéquation avec l’ADN de la marque.' %}",
                    "points": [
                        "{% trans 'Conception de moodboards et univers graphiques.' %}",
                        "{% trans 'Production et direction artistique de shootings photo & vidéo.' %}",
                        "{% trans 'Développement d’une charte visuelle distinctive et impactante.' %}",
                    ],
                },
                {
                    "name": "{% trans 'Création & Production de Contenus' %}",
                    "description": "{% trans 'Nous orchestrons la production de contenus premium, en accord avec l’image et les ambitions de la marque. Notre approche est à la fois stratégique et esthétique, garantissant une communication cohérente et puissante.' %}",
                    "points": [
                        "{% trans 'Design graphique et création visuelle.' %}",
                        "{% trans 'Production de campagnes digitales et vidéos immersives.' %}",
                        "{% trans 'Élaboration de calendriers marketing & éditoriaux.' %}",
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
                    "name": "{% trans 'Stylisme & Sélection de Looks' %}",
                    "description": "{% trans 'Nous habillons nos clients pour tous types d’événements, en sélectionnant des tenues adaptées à leur image et à l’occasion. Chaque look est pensé avec soin pour refléter leur personnalité et leur style' %}",
                    "points": [
                        "{% trans <strong>'Red carpets, Fashion Weeks, événements privés et professionnels.'</strong> %}",
                        "{% trans <strong>'Shooting photos, clips, apparitions médiatiques.'</strong> %}",
                        "{% trans <strong>'Sélection exclusive de pièces issues en collaboration avec nos marques partenaires.'</strong> %}",
                    ],
                },
                {
                    "name": "{% trans 'Expérience sur-mesure & Accès exclusif' %}",
                    "description": "{% trans 'Nous vous offrons un service <strong>clé en main.</strong>' %}",
                    "points": [
                        "{% trans 'Organisation et coordination des <strong>fittings privés et essayages sur-mesure.</strong>' %}",
                        "{% trans <strong>'Gestion complète des looks</strong> (tenues, accessoires, ajustements, logistique).' %}",
                    ],
                },
                {
                    "name": "{% trans 'Image & Signature Visuelle' %}",
                    "description": "{% trans 'Au-delà du stylisme, nous aidons nos clients à construire <strong>une image forte et reconnaissable</strong>, qui s’inscrit dans la durée.' %}",
                    "points": [
                        "{% trans 'Sélection de <strong>photographes, directeurs artistiques et créateurs de contenu</strong> pour mettre en valeur chaque look.' %}",
                        "{% trans 'Accompagnement pour <strong>créer une cohérence stylistique</strong> à travers leurs apparitions et prises de parole publiques.' %}",

                    ],
                },
            ],
        },
        "fashion-week": {
            "title": "VIP Access & Fashion Week Coordination",
            "image": "services/fashion_week.png",
            "video": "https://begincareer.blob.core.windows.net/begincareer/vip_access.mp4",
            "sub_services": [
                {
                    "name": "{% trans 'Social Media & Community Management' %}",
                    "description": "{% trans 'Nous prenons en charge la gestion complète de vos réseaux sociaux afin d’optimiser votre visibilité et engagement. Chaque plateforme a ses codes, et nous adaptons les stratégies pour maximiser votre impact digital.' %}",
                    "points": [
                        "{% trans 'Élaboration et mise en place de stratégies social media.' %}",
                        "{% trans 'Gestion quotidienne des comptes (publications, stories, interactions).' %}",
                        "{% trans 'Analyse des performances et optimisation continue.' %}",
                        "{% trans 'Veille digitale et adaptation aux tendances du marché.' %}",
                        "{% trans 'Élaboration d’une ligne éditoriale cohérente.' %}",
                        "{% trans 'Création de contenus engageants adaptés aux tendances digitales.' %}",
                    ],
                },
                {
                    "name": "{% trans 'Direction Artistique' %}",
                    "description": "{% trans 'Chaque marque a une identité unique, et notre rôle est de la sublimer à travers un univers visuel qui vous correspond. Nous conceptualisons et produisons des contenus, en parfaite adéquation avec l’ADN de la marque.",
                    "points": [
                        "{% trans 'Conception de moodboards et univers graphiques.",
                        "{% trans 'Production et direction artistique de shootings photo & vidéo.",
                        "{% trans 'Développement d’une charte visuelle distinctive et impactante.",
                    ],
                },
                {
                    "name": "{% trans 'Création & Production de Contenus",
                    "description": "{% trans 'Nous orchestrons la production de contenus premium, en accord avec l’image et les ambitions de la marque. Notre approche est à la fois stratégique et esthétique, garantissant une communication cohérente et puissante.' %}",
                    "points": [
                        "{% trans 'Design graphique et création visuelle.' %}",
                        "{% trans 'Production de campagnes digitales et vidéos immersives.' %}",
                        "{% trans 'Élaboration de calendriers marketing & éditoriaux.' %}",
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
