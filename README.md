# Room Equalization with REW and CamillaDSP on Apple Silicon


This guide is written in French. For an English version, here is the automatically translated version:

https://translate.google.com/translate?sl=fr&tl=en&u=https://github.com/phelluy/room_eq_mac_m1


## Introduction

Ce petit guide décrit mon expérience d'égalisation audio d'une pièce ("room audio equalization") sur mon Mac avec puce M1 Apple Silicon. J'ai regroupé diverses informations éparses sur le web et j'ai procédé avec pas mal d'essais et d'erreurs.

J'espère que cette expérience servira à d'autres...

Guide rédigé en juillet 2021, la technique évoluant vite, certaines informations données ci dessous peuvent devenir rapidement obsolètes.

## Ma configuration hi-fi

Ce n'est pas du matériel au top du top, mais je me suis bien amusé à le rassembler:

- Une paire d'enceintes bibliothèques Triangle LN01:

    https://www.lesnumeriques.com/enceintes-home-cinema/triangle-elara-ln01-p29365/test.html  
achetée d'occasion sur LeBonCoin, environ 150€.
- Un ampli chinois avec des tubes, acheté sur AliExpress environ 100€, et qui ne sonne pas trop mal:  
https://fr.aliexpress.com/item/1005001340180594.html?spm=a2g0o.search0304.0.0.c06c247dYZv3Lv&algo_pvid=76c9a6cc-3a75-4cfe-90b5-973a57b13e8d&algo_exp_id=76c9a6cc-3a75-4cfe-90b5-973a57b13e8d-36  
- cet ampli n'a pas de sortie low level pour caisson de basses. Je l'ai donc complété avec un convertisseur high level vers low level:  
https://www.amazon.fr/gp/product/B0191Z7SZE/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1
- Un caisson de basses Triangle Tales 340:  
https://www.trianglehifi.fr/products/caisson-de-grave-tales-340?variant=31727134015535  
Je l'ai eu en promo à 250€.
- Un micro calibré MiniDSP UMIK-1:  
https://www.amazon.fr/gp/product/B00N4Q25R8/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1  
à environ 100€. Le fichier de calibrage, unique pour chaque micro, doit être téléchargé sur le site du fabricant:
https://www.minidsp.com/products/acoustic-measurement/umik-1


Et j'ai aussi un MacBook Pro avec CPU M1.

J'ai installé tout cela dans une petite pièce d'environ 12 m². La pièce est mansardée sous les toits. Le système audio sonne déjà pas mal, mais il y a clairement des résonances indésirables dans les basses. C'est pourquoi je me suis lancé dans l'égalisation audio.

La procédure d'égalisation se fait en deux étapes: une étape de mesure et de calcul des filtres numériques; puis une étape d'intégration des filtres dans un logiciel de traitement numérique du signal ("Digital Signal Processing", DSP) en temps réel. Le DSP vient s'intercaler entre le logiciel de production du son, Deezer par exemple, et la carte son qui enverra le signal vers l'ampli.

## Mesures

Pour les mesures, j'ai utilisé le logiciel gratuit Room EQ Wizard, ou REW pour les intimes:  
https://www.roomeqwizard.com/

C'est un outil puissant, avec beaucoup de possibilités. Je n'en ai utilisé qu'une infime partie. Il y a des versions compilées pour la puce M1, mais il faut aller les télécharger sur le site avnirvana:

https://www.avnirvana.com/resources/categories/rew-room-eq-wizard-beta-downloads.1/

J'ai utilisé la version 5.20 de REW.

Procédure suivie, qui a fonctionné:

1) Brancher le micro, lancer REW. REW détecte le micro UMIK-1 et vous propose de l'utiliser pour les mesures (dire oui !). On vous propose ensuite de donner l'emplacement du fichier de calibrage, que vous avez récupéré au préalable sur le site de minidsp. Dans les préférences système du Mac, vous pouvez aussi tout de suite choisir comme périphérique de sortie audio la carte son qui va envoyer le son vers le système hi-fi à égaliser.
2) Aller dans l'onglet "Preferences" (en haut à droite). Normalement, les périphériques audio sont déjà les bons (vous avez déjà choisi le micro  et la carte son par défaut à l'étape 1). Vérifier tout ça en appuyant sur "Check Levels..." puis "Next". Un bruit est joué et des vumètres permettent de vérifier que le son est bien entendu par le micro. Ajuster le volume sonore pour que REW soit content, puis appuyer sur "Finish". Fermer la fenêtre.
3) Aller dans l'onglet "Measure". Choisir la plage de fréquences pour les mesures en remplissant les cases "Start Freq" et "End Freq". J'ai choisi la plage 30 Hz - 15000 Hz parce que le caisson Triangle ne descend pas en dessous de 30 Hz et parce que passé 50 ans je ne risque pas d'entendre des fréquences au-dessus de 15 kHz !
4) Appuyer sur le bouton "Check levels". Si le son est trop fort ou trop faible, ajuster le niveau jusqu'à ce que REW soit content.
5) Ensuite, appuyer sur "Start" pour démarrer la mesure. REW émet un son de fréquence variable puis la mesure apparaît dans la fenêtre principale de REW. Vous noterez que cette mesure est très bruitée, surtout dans les hautes fréquences. C'est normal, et c'est pour cela qu'il faut faire plusieurs mesures en déplaçant le micro dans la zone d'écoute (disons dans un rayon de 2 mètres autour de l'auditeur).
6) Refaire donc les étapes 3 à 5, par exemple 5 ou 6 fois en bougeant le micro.

Ça y est, vous avez fini les mesures. On passe maintenant à l'étape de calcul des filtres.

## Calcul des filtres

1) Vous êtes dans la fenêtre principale de REW et vous voyez vos mesures dans la partie gauche. Dans la partie droite, cliquer sur le bouton "All SPL". Puis cliquer sur le bouton "Averages the responses". Cette opération calcule une moyenne des mesures de la zone d'écoute. Décochez toutes les cases, pour faire disparaître les courbes de mesure, sauf la courbe "Average 1". Vous voyez ainsi la courbe de réponse en fréquence sur laquelle sera appliquée l'égalisation. Vous voyez aussi les modes de résonances de votre pièce et de votre système audio. Chez moi par exemple, les basses sont boursouflées et il y a deux pics vers 60 et 120 Hz.
2) Cliquer maintenant sur le bouton "EQ" en haut à droite. Dans "Equalizer", choisir "miniDSP 2x4 HD".
3) Dans "Target type", choisir "full range speaker". Cocher la case "Add room curve" et laisser les paramètres par défaut. Cliquer sur "Calculate target level from response".
4) Dans l'onglet "Filter tasks" commencer par indiquer la plage de fréquences pour l'égalisation ("Match range"), par exemple 30-15000 Hz, comme pour la mesure. Enfin cliquer sur "Match response to target". REW calcule les coefficients de filtre. Vous pouvez vérifier graphiquement l'effet obtenu. Il ne reste plus qu'à sauver les caractéristiques des filtres avec l'option "Export filter settings as text". Un exemple de fichier obtenu, `filter_example.txt` est inclus dans ce dépôt git.

## Activation de l'égalisation

### Carte son virtuelle

Pour activer l'égalisation sur Mac, il faut d'abord installer une carte son virtuelle. Deezer (par exemple) enverra son signal vers cette carte son. Le logiciel DSP récupérera le signal de la carte virtuelle pour l'envoyer vers la vraie carte.

J'ai installé la version deux canaux de l'outil blackhole:
https://github.com/ExistentialAudio/BlackHole
au moyen de brew, avec la commande:

``` brew install blackhole-2ch ```

Si vous ouvrez le panneau son des préférences système, vous voyez apparaître un nouveau périphérique de sortie et un nouveau périphérique d'entrée. Les deux sont dénommés "BlackHole 2ch".

### Installation de CamillaDSP

CamillaDSP est un logiciel écrit en RUST pour appliquer des filtres à un signal sonore. Il est développé par Henrik Enquist (merci à lui !), voir:  
https://github.com/HEnquist/camilladsp  
Henrik Enquist a aussi créé un dépôt GitHub pour une installation facile de CamillaDSP et de ses dépendances:
https://github.com/HEnquist/camilladsp-setupscripts  
Suivre les indications données. Il faut au préalable avoir installé Miniconda ou Anaconda:  
https://www.anaconda.com/products/individual

Quand j'ai lancé la script `install_mac_arm.sh`, j'ai eu une erreur, que j'ai supprimée en commentant la ligne
```source ~/opt/anaconda3/etc/profile.d/conda.sh```
de ce script (mettre un `#` devant).

Pour lancer camillaDSP suivre les instructions, en résumé il faut lancer le backend:  
```./camilladsp -p1234 -w```  
L'option `-p1234` signifie que le backend attend des instructions d'une page web. L'option `-w` signifie que le fichier de configuration sera fournie par la page web.
Dans une autre fenêtre de terminal, tapez:
```
cd camillagui
conda activate camillagui
python main.py
 ```
Ensuite connectez-vous à l'adresse http://localhost:5000
avec votre navigateur internet.

CamillaDSP est installé. Nous allons maintenant créer un fichier de configuration.

### Génération d'un fichier de config

Le script python `dataconvert.py` fourni dans ce dépôt  (écrit par `https://github.com/mhelluy`) permet d'inclure le fichier txt généré par REW dans un fichier yaml de configuration CamillaDSP. Taper la commande:
```
python dataconvert.py filter_example.txt
````
Cette commande ajoute les filtres dans le fichier `config_template.yml` et génère un fichier `filter_example.yaml`

#### Dernière étape !

Retourner dans le navigateur web à la page  `http://localhost:5000/gui/index.html`
Dans l'onglet "File" charger le fichier "filter_example.yaml" (au moyen de la commande "Upload").

Si le fichier de configuration contient des erreurs, un `!` apparaît dans l'onglet correspondant.
Corriger les éventuelles erreurs.

Dans l'onglet "Devices", vous devez choisir le bon "Playback Device": c'est la sortie qui va envoyer le son vers les enceintes. Dans mon cas, c'est le périphérique "BT HIFI AUDIO", mais cela dépend évidemment de votre système.

Appuyer ensuite sur le bouton "Apply to CDSP". Vous devriez voir le vumètre vert s'activer quand vous mettez en route de la musique. 

Ne pas oublier de sélectionner comme sortie sonore la carte virtuelle "BlackHole 2ch" dans les préférences système.

Dans les préférences système vous pouvez aussi basculer entre la carte son physique et la carte  "BlackHole 2ch" pour apprécier l'effet de l'égalisation.

J'ai eu un peu de mal à régler le volume sonore. Si le niveau est trop élevé, ça sature, et CamillaDSP lance des warnings. Si c'est trop faible, il faut augmenter le volume, mais plutôt sur l'ampli physique.

Une fois que tout est réglé, l'amélioration est significative. La musique sonne de façon beaucoup plus naturelle, sans résonance dans les graves.

Il reste à trouver une mise en place de tout le système qui soit un peu plus ergonomique. À suivre...





