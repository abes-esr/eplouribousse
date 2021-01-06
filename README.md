More comfortable in english ? Go to README_en.md

# AppliWeb collaborative pour gérer le dédoublonnement des revues dans les bibliothèques.

Gagnez de l'espace en éliminant vos doublons, offrez une meilleure lisibilité de vos ressources en reconstituant pour chacune d'elles une collection unique la plus intègre possible résultant de l'agrégation des éléments épars disponibles dans vos bibliothèques.

# Méthode :

Pour une ressource donnée (Unité catalographique sans les filiations), l'application eplouribousse permet aux bibliothèques, chacune à son tour, d'indiquer ses éléments reliés contribuant à la résultante, puis lors d'un deuxième cycle d'instructions et selon la même logique, ses éléments non-reliés complémentaires.

L'ordre de traitement est significatif : La première bibliothèque est normalement celle détenant déjà la collection la plus importante (Celle qui revendique la conservation dans l'hypothèse où la collection est finalement regroupée). C'est la même logique d'importance qui doit prévaloir normalement pour la place revendiquée par les bibliothèques suivantes. Il peut arriver qu'une bibliothèque veuille soustraire sa collection à la reconstitution de la résultante (Le cas typique est celui d'une collection du dépôt légal) Le module de positionnement de l'application eplouribousse rend cette dérogation possible.

Les fiches obtenues décrivent les résultantes ; les éléments écartés s'en déduisent. Les parties contribuant à la collection résultante peuvent être regroupées ou pas, au choix. Les traitements physiques et mises à jour catalographiques sont à prévoir.

Voir une illustration : https://seafile.unistra.fr/f/163d60a568e2482092e3/

# Fonctionnalités :

01. édition des candidats pour chaque bibliothèque participante,
02. formulaire de positionnement (ou de dérogation),
03. édition des ressources dont l'instruction de la résultante peut débuter,
04. alerte quand son tour est venu de poursuivre l'instruction de la résultante,
05. formulaires d'instruction (ajout, suppression, modification, fin),
06. édition différenciée des résultantes (rapports soignés au format pdf),
07. contrôle de conformité à la fin de chaque cycle d'instruction,
08. prise en charge complète de la chaîne de traitement,
09. tableau de suivi d'activité,
10. recherche croisée par ressource et bibliothèque,
11. gestion des utilisateurs,
12. contrôles d'authentification,
13. paramétrage des motifs de dérogation,
14. administration des cas de fiches défectueuses,
15. prise en charge multilingue (français, anglais, allemand ; possibilité d'étendre à d'autres langues),
16. formulaires de contact de l'administrateur de l'instance et du développeur,
17. gestion autonome du mot de passe.

# Plus d'info :

Voir le manuel de l'appli dans le dossier Doc

Visionner les vidéos de présentation (à télécharger si vous n'arrivez pas à visionner complètement) : 
01. Hypothèses et définitions : https://seafile.unistra.fr/f/dd5b8a16b1a5440389e5/
02. Méthode : https://seafile.unistra.fr/f/590ba4359f3e4b73b60e/
03. Préparation de la base de données : https://seafile.unistra.fr/f/9581ffba08f24e849b08/
04. Exemple d'un traitement de bout en bout : https://seafile.unistra.fr/f/b87faa2857ee42bab57f/
05. Administration du site : https://seafile.unistra.fr/f/d3f6a23f94804dfabddd/
06. Crédits : https://seafile.unistra.fr/f/579d874730604579b073/

# Comment obtenir eplouribousse ?

Pour avoir un aperçu de l'application, commencez par visiter une instance réelle parmi les suivantes :
01. https://eplouribousse1.di.unistra.fr/
02. https://eplouribousse2.di.unistra.fr/
03. https://eplouribousse3.di.unistra.fr/

----------------

ça vous a plu ? Allez plus loin ; essayez eplouribousse sur un poste local équipé du serveur de développement de Django ; cela vous permettra de tester toutes les fonctionnalités (Les alertes mail seront éditées dans le terminal).

Pour les distributions Debian de Linux (Ubuntu, LinuxMint etc.), suivez les instructions pas à pas données dans Doc/guide.txt

----------------

Vous êtes convaincu et vous voulez mettre en oeuvre eplouribousse dans votre établissement ?
Nous conseillons d'abord de vous rapprocher de votre équipe informatique pour une installation de test.

Si vous souhaitez utiliser eplouribousse pour un projet ferme, il y a actuellement trois possibilités :
- Confier le déploiement à votre service informatique en indiquant l'adresse du présent site
- Confier le déploiement à un hébergeur en indiquant l'adresse du présent site
- Nous confier le déploiement (sous réserve d'accord)

Dans tous ces cas, veuillez nous informer de votre intérêt (contact ci-après)

# Instructions pour le déploiement :

- L'outil de déploiement ayant été codé en python 2.7, il conviendra d'abord de créer un environnement virtuel sous lequel on installera cette version de python,
- Le déploiement se fait avec l'outil pydiploy <https://pypi.org/project/pydiploy/> (installation avec la commande 'pip install pydiploy', dans l'environnement virtuel précédemment créé),
- L'usage de pydiploy implique la création d'un fabfile ad-hoc sur le modèle de ceux fournis dans le dépôt (exemple <https://github.com/GGre/eplouribounistra/blob/master/fabfile_eplouribousse1.py>),
- Il faut également prévoir l'installation de reportlab open source <https://pypi.org/project/reportlab/> (pour la génération de fichiers pdf).

# Crédits :

eplouribousse utilise des données sous licence ouverte etalab fournies par l'Agence bibliographique de l’Enseignement supérieur.

# Contact :

Indiqué en https://github.com/GGre/eplouribounistra/blob/master/contact.txt

