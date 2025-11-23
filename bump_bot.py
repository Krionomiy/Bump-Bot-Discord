import discord
from discord.ext import tasks
import datetime
import os # <<< AJOUT N°1 : Importation du module os pour les variables d'environnement

# --- ⚠️ CONFIGURATION ESSENTIELLE À MODIFIER (TOKEN SÉCURISÉ) ⚠️ ---
# 1. Le Token n'est PLUS ici. Il sera lu depuis la variable d'environnement DISCORD_TOKEN
TOKEN = os.getenv("DISCORD_TOKEN") 

# 2. L'ID du salon où le rappel doit être envoyé
CHANNEL_ID = 1272611563307794484 

# 3. Le message de RAPPEL avec la mention @here
BUMP_COMMAND = "🚨 @here Il est temps de faire le /bump ! Tapez la commande pour relancer le timer."
# -------------------------------------------------------------------

# Définition des intents nécessaires
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# --- TÂCHE RÉCURRENTE (Toutes les 2 heures) ---
@tasks.loop(hours=3)
async def auto_bump():
    """Tâche qui envoie le message de rappel toutes les 2 heures."""
    
    # Attend que le bot soit pleinement connecté et prêt
    await client.wait_until_ready()
    # Cherche le salon par l'ID
    channel = client.get_channel(CHANNEL_ID)

    if channel:
        try:
            # Envoi du message de rappel dans le salon
            await channel.send(BUMP_COMMAND)
            
            heure_locale = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{heure_locale}] SUCCESS : Message de rappel envoyé dans le salon '{channel.name}'.")
        
        except discord.errors.Forbidden:
            # Gestion des erreurs de permission
            heure_locale = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{heure_locale}] ERREUR : Le bot n'a pas la permission d'envoyer des messages dans le salon. Vérifiez les rôles.")
        
        except Exception as e:
            # Gestion des autres erreurs critiques
            heure_locale = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{heure_locale}] ERREUR CRITIQUE lors de l'envoi du message : {e}")

    else:
        # Gestion de l'erreur si le salon n'est pas trouvé
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] AVERTISSEMENT : Salon avec l'ID {CHANNEL_ID} non trouvé. Vérifiez l'ID.")

# --- ÉVÉNEMENT DE DÉMARRAGE DU BOT ---
@client.event
async def on_ready():
    print('--- Bot Démarré ---')
    print(f'Connecté en tant que {client.user}')
    
    # Démarre la boucle seulement si elle n'est pas déjà en cours
    if not auto_bump.is_running():
        auto_bump.start()
        print(f"Tâche 'auto_bump' démarrée : envoi du rappel toutes les 2 heures.")
        
    print('-------------------')

# --- DÉMARRAGE DU PROGRAMME ---
if not TOKEN:
    print("\n[ERREUR FATALE] : La variable d'environnement DISCORD_TOKEN n'a pas été définie.")
else:
    try:
        client.run(TOKEN)
    except discord.errors.LoginFailure:
        print("\n[ERREUR FATALE] : Le jeton (TOKEN) du bot est invalide. Veuillez le vérifier.")
    except Exception as e:
        print(f"\n[ERREUR FATALE] : Le bot n'a pas pu démarrer. Erreur : {e}")