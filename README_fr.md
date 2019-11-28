# AppliWeb collaborative pour gérer le dédoublonnement des revues dans les bibliothèques.

Gagnez de l'espace en éliminant vos doublons, offrez une meilleure lisibilité de vos ressources en reconstituant pour chacune d'elles une collection unique la plus intègre possible résultant de l'agrégation des éléments épars disponibles dans vos bibliothèques.

# Méthode :

Pour une ressource donnée (Unité catalographique sans les filiations), l'application eplouribousse permet aux bibliothèques, chacune à son tour, d'indiquer ses éléments reliés contribuant à la résultante, puis lors d'un deuxième cycle d'instructions et selon la même logique, ses éléments non-reliés complémentaires.

L'ordre de traitement est significatif : La première bibliothèque est normalement celle détenant déjà la collection la plus importante (Celle qui revendique la conservation dans l'hypothèse où la collection est finalement regroupée). C'est la même logique d'importance qui doit prévaloir normalement pour la place revendiquée par les bibliothèques suivantes. Il peut arriver qu'une bibliothèque veuille soustraire sa collection à la reconstitution de la résultante (Le cas typique est celui d'une collection du dépôt légal) Le module de positionnement de l'application eplouribousse rend cette dérogation possible.

Les fiches obtenues décrivent les résultantes ; les éléments écartés s'en déduisent. Les parties contribuant à la collection résultante peuvent être regroupées ou pas, au choix. Les traitements physiques et mises à jour catalographiques sont à prévoir.

# Fonctionnalités :

01. édition des candidats pour chaque bibliothèque participante,
02. formulaire de positionnement (ou de dérogation),
03. édition des ressources dont l'instruction de la résultante peut débuter,
04. alerte quand son tour est venu de poursuivre l'instruction de la résultante,
05. formulaires d'instruction (ajout, suppression, fin),
06. édition différenciée des résultantes (rapports soignés au format pdf),
07. contrôle de conformité à la fin de chaque cycle d'instruction,
08. prise en charge complète de la chaîne de traitement,
09. tableau de suivi d'activité,
10. gestion des utilisateurs et groupes,
11. contrôles d'authentification,
12. paramétrage des motifs de dérogation,
13. administration des cas de fiches défectueuses,
14. prise en charge multilingue (français, anglais, allemand ; possibilité d'étendre à d'autres langues)

# Plus d'info :

Voir le manuel de l'appli en https://seafile.unistra.fr/f/a998b238a22b4c13baf5/

# Comment obtenir eplouribousse ?

Commencez par visiter une instance réelle : https://eplouribousse.di.unistra.fr/
Cela vous donnera un aperçu de l'application.

Si vous voulez aller plus loin, essayez eplouribousse sur un poste local équipé du serveur de développement de Django ; cela vous permettra de tester toutes les fonctionnalités (à l'exception des alertes mail qui ne sont qu'une commodité)
Pour cela, clonez le dépôt https://github.com/GGre/eplouribounistra dans un répertoire de votre choix, puis téléchargez le specimen de base de données (url) et placez-la dans le répertoire qui contient le fichier manage.py
(Un petit coup d'oeil sur la structure de la base vous permettra d'élaborer la vôtre)
Pour ce test, nous avons trois bibliothèques : John travaille pour la bibliothèque Swallow, Susan pour la bibliothèque Magpie, Petra pour la bibliothèque Raven, Carla est le vérificateur et vous, vous êtes Joyce l'administrateur.
Testez !

Vous êtes convaincu et vous voulez mettre en oeuvre eplouribousse dans votre établissement ?
Nous conseillons d'abord de vous rapprocher de votre équipe informatique pour une installation de test.

Si vous souhaitez utiliser eplouribousse pour un projet ferme, il y a trois possibilités :
- Confier le déploiement à votre service informatique en indiquant l'adresse du présent site
- Confier le déploiement à un hébergeur en indiquant l'adresse du présent site
- Nous confier le déploiement (après accord et convention)

Dans tous ces cas, veuillez nous informer de votre intérêt (contact ci-après)

# Contact :

Indiqué en https://github.com/GGre/eplouribounistra/blob/master/Version.txt

