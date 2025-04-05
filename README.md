# ACW


# Projet Hackathon : Wallonia Contextual Assistant (WCA) - PoC

Bienvenue dans le dépôt du projet WCA pour le hackathon "Citizen of Wallonia" !

**Objectif de ce README :** Expliquer très simplement comment on va travailler tous ensemble sur ce code sans se marcher sur les pieds, même si vous n'avez jamais utilisé Git/GitHub.

## Le Principe de Base (Pour ne rien casser)

1.  La branche principale s'appelle `main`. **Personne ne travaille directement dessus.** Elle contient la version "stable" de notre projet.
2.  Pour chaque nouvelle tâche (ex: "ajouter le bouton X", "coder la fonction Y"), vous allez créer votre **propre copie temporaire** du projet, appelée une **branche**.
3.  Vous travaillez tranquillement sur votre branche, sans impacter les autres.
4.  Quand votre tâche est finie et testée, vous proposez que vos modifications soient ajoutées à la branche `main` via une "Pull Request" (PR). C'est une demande de fusion que le Tech Lead validera.

## Comment Travailler Ensemble (Le Workflow Essentiel)

Suivez ces étapes **dans l'ordre** pour chaque nouvelle tâche :

1.  **Récupérer le Projet (UNE SEULE FOIS AU DÉBUT) :**
    * Ouvrez un terminal (ou Git Bash sur Windows).
    * Allez dans le dossier où vous voulez mettre le projet.
    * Tapez : `git clone https://github.com/C1yded/ACW` (Le Tech Lead donnera l'URL)
    * Cela crée un dossier avec le projet sur votre PC.

2.  **Se Mettre à Jour (TOUJOURS AVANT DE COMMENCER UNE TÂCHE) :**
    * Ouvrez un terminal **DANS** le dossier du projet.
    * Assurez-vous d'être sur la branche principale : `git checkout main`
    * Récupérez les dernières modifications des autres : `git pull origin main`

3.  **Créer Votre Branche de Travail :**
    * Donnez un nom clair à votre branche (ex: `feature/ajout-bouton-simple`, `fix/bug-affichage`...).
    * Tapez : `git checkout -b nom-de-votre-branche`
    * Vous êtes maintenant sur votre espace de travail isolé !

4.  **Faire Votre Travail (Coder !) :**
    * Modifiez les fichiers nécessaires pour votre tâche dans votre éditeur de code.

5.  **Sauvegarder Vos Modifications (Régulièrement) :**
    * "Ajouter" les fichiers que vous avez modifiés pour dire à Git de les suivre : `git add .` (le point signifie "tous les fichiers modifiés dans ce dossier et sous-dossiers") ou `git add nom_du_fichier_specifique`.
    * "Valider" ces changements avec un message clair : `git commit -m "Un message qui explique BIEN ce que vous avez fait (ex: Ajout du bouton Simplifier sur l'UI)"`

6.  **Envoyer Votre Branche sur GitHub (Quand vous avez fini ou voulez partager) :**
    * Tapez : `git push origin nom-de-votre-branche`
    * La première fois, Git pourrait vous donner une commande légèrement différente à copier/coller, suivez ses instructions.

7.  **Demander l'Intégration (Pull Request - PR) :**
    * Allez sur la page GitHub du projet dans votre navigateur.
    * GitHub devrait détecter que vous avez "pushé" une nouvelle branche et proposer de créer une "Pull Request". Cliquez dessus.
    * Donnez un titre clair à votre PR, ajoutez une petite description si besoin.
    * Cliquez sur "Create Pull Request".

8.  **Attendre la Validation :**
    * Le Tech Lead va regarder votre code. Il peut demander des modifications ou le valider ("Merge").
    * Une fois validé ("Merged"), votre code fait partie de la branche `main` ! 🎉

9.  **Recommencer :** Pour une nouvelle tâche, retournez à l'étape 2 !

## Quelques Règles Simples

* **Toujours `git pull origin main`** avant de créer une nouvelle branche (étape 2).
* Faites des **petites branches** pour des **petites tâches**. C'est plus facile à gérer.
* Écrivez des **messages de commit clairs** (en français ou anglais, soyons cohérents).
* **Ne poussez JAMAIS directement sur `main`**. Toujours passer par une Pull Request.
* **Communiquez** avec l'équipe (sur Discord/Slack/autre) sur ce que vous faites pour éviter de travailler sur la même chose.

## En Cas de Problème ?

* Pas de panique !
* Si vous voyez des messages d'erreur étranges (surtout "Merge Conflict"), ne touchez à rien et appelez le Tech Lead. C'est normal quand on travaille à plusieurs, et ça se règle.

**Bon hackathon et bonne collaboration !**
