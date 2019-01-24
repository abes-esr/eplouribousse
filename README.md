eplouribousse est une application web conçue et réalisée par un bibliothécaire à l'attention des bibliothécaires pour la gestion du dédoublonnement des revues dans un ensemble de bibliothèques.

# Objectif :

eplouribousse est la forme franchouillarde de l'expression latine “e plvribvs (vnvm)” : “(Une) à partir de plusieurs.”

C'est précisément ce que nous souhaitons faire : Afin de rationaliser les collections et les espaces de stockage, nous pouvons raisonnablement décider de reconstituer une collection unique à partir des éléments épars disponibles dans l'ensemble des bibliothèques participant au projet, collection que l'on voudra la plus intègre possible tant en terme de couverture temporelle qu'en terme d'état physique. Nous la nommerons collection résultante ou plus simplement résultante.

eplouribousse est conçue pour gérer le dédoublonnement des revues (ou plus généralement les ressources continues) Ce faisant, nous savons que nous opérons à plus large échelle qu'en dédoublonnant des livres.

eplouribousse peut vous rendre service si votre ensemble de bibliothèques détient d'importantes collections de revues et que le taux de recouvrement entre les bibliothèques est important. Inutile d'attendre d'être confronté à des taux de saturation extrême pour commencer. Typiquement eplouribousse peut être mise en œuvre après une fusion d'universités ou au sein d'un réseau d'établissements adoptant une politique documentaire commune.
Que nous faut-il pour que ça marche ?

  - Un ensemble de bibliothèques, chacune identifiée par un identifiant unique.
  - Les rattachements dans un catalogue commun, chacun identifié par la paire (identifiant unique de la revue, identifiant unique de la bibliothèque)
  - Une revue est réputée candidate au dédoublonnement dès lors que son identifiant unique apparaît dans deux rattachements au moins.


# Comment nous procédons :

Pour une revue donnée, l'application eplouribousse permet aux bibliothèques, chacune à son tour, d'indiquer leurs éléments reliés contribuant à la résultante, puis lors d'un deuxième cycle d'instructions indiquer selon la même logique leurs éléments non-reliés complémentaires.

Nous voulons être efficaces ; nous ne cherchons pas à couper les cheveux en quatre : Relié ou non relié, oui ; mais plein cuir, demi-cuir, cartonné etc. Non, car soyez sûrs que vous n'en finirez pas.

Il peut arriver, même si cela est rare, qu'un segment non-relié remplace avantageusement un segment relié en mauvais état (Le cas typique est celui où la reliure a compromis l'intégrité du contenu) Ce cas est pris en compte dans l'application eplouribousse.

L'ordre de traitement est significatif : La première bibliothèque est normalement celle détenant déjà la collection la plus importante (Celle qui revendique la conservation dans l'hypothèse où la collection est finalement regroupée). C'est la même logique d'importance qui doit prévaloir normalement pour la place revendiquée par les bibliothèques suivantes. Il peut arriver qu'une bibliothèque veuille soustraire sa collection à la reconstitution de la résultante (Le cas typique est celui d'une collection du dépôt légal) Le module de positionnement de l'application eplouribousse rend cette dérogation possible.

On notera que les descriptions obtenues sont celles des collections résultantes ; elles ne renseignent aucunement sur les éléments écartés ; ceux-ci se déduisent de celles-là. Les éléments qui ne participent pas à la résultante peuvent être cédés ou pilonnés. Les parties contribuant à la collection résultante peuvent être regroupées ou pas, au choix.

Il faut naturellement prévoir les traitements physiques et mises à jour catalographiques.


# Qu'est-ce que fait eplouribousse ?

eplouribousse

1. calcule les candidats pour chacune des bibliothèque participantes,
2. permet aux bibliothèques de prendre rang pour le traitement (ou d'exclure leur collection),
3. fournit aux bibliothèques la liste des ressources pour lesquelles elles peuvent faire les instructions,
4. permet aux bibliothèques d'être averties lorsque leur tour est venu d'instruire la résultante,
5. fournit aux bibliothèques un formulaire d'instruction,
6. fournit aux bibliothèques la liste des ressources dont l'édition de la résultante est possible (instruction complète de la résultante),
7. fournit aux bibliothèques un formulaire d'édition personnalisé pour chacune des collections résultantes par lesquelles elles sont concernées,
8. fournit un module de contrôle à la fin de chaque cycle d'instruction,
9. gère l'ensemble de la chaîne de traitement,
10. fournit un tableau de bord permettant de suivre l'activité.
