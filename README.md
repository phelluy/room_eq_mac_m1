# Room Equalization HowTo with REW and Apple Silicon


This guide is written in French. For an English version, please send it to DeepL or Google Translate !

## Introduction

Ce petit guide décrit mon expérience d'égalisation audio d'une pièce (room audio equalization) sur mon Mac avec puce M1 Apple Silicon. J'ai regroupé diverses informations éparses sur le web et j'ai procédé avec pas mal d'essais et d'erreurs.

J'espère que cette petite expérience servira à d'autres...

Guide rédigé en juillet 2021, la techno évoluant vite, certianes informations donnéesci-dessous peuvent devenir rapidement obsolètes.

## Ma configuration Hi-fi

Ce n'est pas du matériel au top du top, mais je me suis bien amusé à le rassembler:

- Une paire d'enceintes bibliothèques Triangle LN01:<br>
    https://www.lesnumeriques.com/enceintes-home-cinema/triangle-elara-ln01-p29365/test.html <br>
achetée d'occasion sur LeBonCoin, environ 150€.
- Un ampli chinois avec des tubes, acheté sur AliExpress environ 100€, et qui ne sonne pas trop mal: <br>
https://fr.aliexpress.com/item/1005001340180594.html?spm=a2g0o.search0304.0.0.c06c247dYZv3Lv&algo_pvid=76c9a6cc-3a75-4cfe-90b5-973a57b13e8d&algo_exp_id=76c9a6cc-3a75-4cfe-90b5-973a57b13e8d-36 <br>
- cet ampli n'a pas de sortie low level pour caisson de basses. Je l'ai donc complété avec un convertisseur high level vers low level: <br>
https://www.amazon.fr/gp/product/B0191Z7SZE/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1 <br>
- Un caisson de basses Triangle Tales 340:<br>
https://www.trianglehifi.fr/products/caisson-de-grave-tales-340?variant=31727134015535 <br>
Je l'ai eu en promo à 250€.
- Un micro calibré MiniDSP UMIK-1: https://www.amazon.fr/gp/product/B00N4Q25R8/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1
à environ 100€. Le fichier de calibrage, unique pour chaque micro, doit être téléchargé sur le site du fabricant:
https://www.minidsp.com/products/acoustic-measurement/umik-1


Et j'ai aussi un MacBook Pro avec CPU M1.

J'ai installé tout cela dans une petite pièce d'environ 12 m². La pièce est mansardée sous les toits. Le système audio sonne déjà pas mal, mais il y a clairement des résonances indésirables dans les basses. C'est pourquoi je me suis lancé dans l'égalisation audio.

La procédure d'égalisation se fait en deux étapes: une étape de mesure et de calcul des filtres numériques; puis une étape d'intégration des filtres dans un logiciel de traitement numérique du signal (Digital Signal Processing, DSP) en temps réel. Le DSP vient s'intercaler entre le logiciel de production du son, Deezer par exemple, et la carte son qui enverra le signal vers l'ampli.

## Mesures

Pour les mesures, j'ai utilisé le logiciel gratuit Room EQ Wizard, REW pour les intimes:
https://www.roomeqwizard.com/

C'est un outil puissant, avec beaucoup de possibilités. Je n'en ai utilisé qu'une infime partie. Il y a des versions compilées pour la puce M1, mais il faut aller les télécharger sur le site avnirvana:

https://www.avnirvana.com/resources/categories/rew-room-eq-wizard-beta-downloads.1/

J'ai utilisé la version 5.20 de REW.

Procédure suivie, qui a fonctionné:

1) Brancher le micro, lancer REW. REW détecte le micro UMIK-1 et vous propose de l'utiliser pour les mesures (dire oui !). On vous propose ensuite de donner l'emplacement du fichier de calibrage, que vous avez récupéré au préalable sur le site de minidsp. Dans les préférences système du Mac, vous pouvez aussi tout de suite choisir comme périphérique de sortie audio la carte son qui va envoyer le son vers le système Hi-fi à égaliser.
2) Aller dans l'onglet "Preferences" (en haut à droite). Normalement, les périphériques audio sont déjà les bons (vous avez déjà choisi le micro  et la carte son par défaut à l'étape 1). Vérifier tout ça en appuyant sur "Check Levels..." puis "Next". Un bruit est joué et des vue-mètres permettent de vérfier que le son est bien entendu par le micro. Ajuster le volume sonore pour que REW soit content, puis appuyer sur "Finish". Fermer la fenètre.
3) Aller dans l'onglet "Measure". Choisir la plage de fréquences pour les mesures en remplissant les cases "Start Freq" et "End Freq". J'ai choisi la plage 30 Hz - 15000 Hz parce que le caisson Triangle ne descend pas en dessous de 30 Hz et parce que passé 50 ans je ne risque pas d'entendre des fréquences au dessus de 15 kHz !
4) Appuyer sur le bouton "Check levels". Si le son est trop fort ou trop faible, ajuster le niveau jusqu'à ce que REW soit content.
5) Ensuite appuyer sur "Start" pour démarrer la mesure. REW émet un son de fréquence variable puis la mesure apparaît dans la fenêtre principale de REW. Vous noterez que cette mesure est très bruitée, surtout dans les hautes fréquences. C'est normal, et c'est pour cela qu'il faut faire plusieurs mesures en déplaçant le micro dans la zone d'écoute (disons dans un rayon de 2 mètres autour de l'auditeur).
6) Refaire donc les étapes 3 à 5, par exemple 5 ou 6 fois en bougeant le micro.

Ça y est, vous avez fini les mesures. On passe maintenant à l'étape de calcul des filtres.

## Calcul des filtres

1) Vous êtes dans la fenêtre principale de REW et vous voyez vos mesures dans la partie gauche. Dans la partie droite, cliquer sur le bouton "All SPL". Puis cliquer sur le bouton "Averages the responses". Cette opération calcule une moyenne des mesures de la zone d'écoute. Décochez toutes les cases, pour faire disparaître les courbes de mesure, sauf la courbe "Average 1". Vous voyez ainsi la courbe de réponse en fréquence sur laquelle sera appliquée l'égalisation. Vous voyez aussi les modes de résonances de votre pièce et de votre système audio. Chez moi par exemple, les basses sont boursouflées et il y a deux pics vers 60 et 120 Hz.
2) Cliquer maintenant sur le bouton "EQ" en haut à droite. Dans "Equalizer", choisir "miniDSP 2x4 HD".
3) Dans "Target type", choisir "full range speaker". Cocher la case "Add room curve" et laisser les paramètres par défaut. Cliquer sur "Calculate target level from response".
4) Dans l'onglet "Filter tasks" commencer par indiquer la plage de fréquences pour l'égalisation ("Match range"), par exemple 30-15000 Hz, comme pour la mesure. Enfin cliquer sur "Match response to target". REW calcule les coefficients de filtre. Vous pouvez vérifier graphiquement l'effet obtenu. Il ne reste plus qu'à sauver les caractéristiques des filtres avec l'option "Export filter settings as text".

## Activation de l'égalisation

à suivre...