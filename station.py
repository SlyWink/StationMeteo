from types import SimpleNamespace as ns
from math import cos, sin, pi

def r(d):
  return d/2

def m(x):
  return x - 0.01


visserie = ns()

visserie.tige = ns()
visserie.tige.diametre = 5
visserie.tige.longueur_courte = 240
visserie.tige.longueur_longue = 260

visserie.rondelle = ns()
visserie.rondelle.diametre_exterieur = 14
visserie.rondelle.diametre_interieur = visserie.tige.diametre + 0.5
visserie.rondelle.epaisseur = 1

visserie.ecrou = ns()
visserie.ecrou.diametre_exterieur = 11
visserie.ecrou.diametre_interieur = visserie.tige.diametre + 0.5
visserie.ecrou.epaisseur = 5

lux = ns()

lux.tube = ns()
lux.tube.diametre_exterieur = 16
lux.tube.diametre_interieur = 13
lux.tube.longueur = 415

lux.butee = ns()
lux.butee.hauteur = 12
lux.butee.diametre = lux.tube.diametre_interieur - 0.5
lux.butee.profondeur_trou_vis = 10 
lux.butee.diametre_trou_vis = 3

lux.dome = ns()
lux.dome.fleche = 20
lux.dome.corde = 50
lux.dome.epaisseur = 5

lux.capteur = ns()
lux.capteur.diametre_pour_dome = lux.dome.corde + 2
lux.capteur.hauteur_bordure = 3
lux.capteur.hauteur_platine = 3
lux.capteur.largeur_bordure = 2
lux.capteur.hauteur_manchon = 20
lux.capteur.diametre_trou_fils = 5
lux.capteur.diametre_trou_tube = lux.tube.diametre_exterieur + 0.5
lux.capteur.longueur_rainure = r(lux.capteur.diametre_pour_dome) - lux.dome.epaisseur - 5

lux.pcb = ns()
lux.pcb.longueur = 18.8
lux.pcb.largeur = 13.5
lux.pcb.ecart_entre_trous = 9
lux.pcb.diametre_trous = 3
lux.pcb_ecart_trous_haut = 2.7
lux.pcb.epaisseur_min = 1
lux.pcb.epaisseur_max = 5

lux.manchon = ns()
lux.manchon.diametre_exterieur = lux.tube.diametre_exterieur + 20
lux.manchon.diametre_trou_tube = lux.tube.diametre_exterieur + 0.5
lux.manchon.hauteur = 10

coupelle = ns()
coupelle.nombre = 10
coupelle.diametre_base = 186
coupelle.diametre_haut = 220
coupelle.diametre_vide = 189
coupelle.epaisseur = 1
coupelle.hauteur_bord = 28
coupelle.diametre_trou_tige = visserie.tige.diametre + 0.5
coupelle.distance_trou_tige = r(coupelle.diametre_base) - 15
coupelle.diametre_trou_tube = lux.tube.diametre_exterieur + 0.5
#coupelle.distance_trou_tube = r(coupelle.diametre_base) - 40
coupelle.distance_trou_tube = r(coupelle.diametre_base - lux.tube.diametre_exterieur) - 30


def Coupelle(vide=False, tube=False):
  res = (cq
    .Workplane("YX")
      .cylinder(coupelle.hauteur_bord, r(coupelle.diametre_haut), centered=(1,1,0))
      .edges(">Z")
        .chamfer(m(coupelle.hauteur_bord), r(coupelle.diametre_haut - coupelle.diametre_base))
      .faces("<Z")
        .shell(coupelle.epaisseur)
      .faces(">Z")
          .pushPoints([
            (coupelle.distance_trou_tige, 0), (0, coupelle.distance_trou_tige, 0),
            (-coupelle.distance_trou_tige, 0), (0, -coupelle.distance_trou_tige) ])
          .hole(coupelle.diametre_trou_tige)
  )

  if (vide):
    res = (res
      .faces(">Z")
        .workplane()
          .hole(coupelle.diametre_vide)
    )
  else:
    if tube:
      res = (res
        .faces(">Z")
          .pushPoints([ (coupelle.distance_trou_tube * cos(pi/4), coupelle.distance_trou_tube * sin(pi/4)) ])
          .hole(coupelle.diametre_trou_tube)
     )

  return res


def Tige(longue=False):
  res = (cq
    .Workplane("XY")
      .cylinder(
        visserie.tige.longueur_longue if longue else visserie.tige.longueur_courte, r(visserie.tige.diametre), centered=(1,1,0))
  )
  return res


def Tube():
  res = (cq
    .Workplane("XY")
      .cylinder(lux.tube.longueur, r(lux.tube.diametre_exterieur), centered=(1,1,0))
      .faces(">Z")
        .hole(lux.tube.diametre_interieur)
  )
  return res


def Rondelle():
  res = (cq
    .Workplane("XY")
      .cylinder(visserie.rondelle.epaisseur, r(visserie.rondelle.diametre_exterieur), centered=(1,1,0))
      .faces(">Z")
        .hole(visserie.rondelle.diametre_interieur)
  )
  return res


def Ecrou():
  res = (cq
    .Workplane("XY")
    .sketch()
       .regularPolygon(r(visserie.ecrou.diametre_exterieur), 6)
       .circle(r(visserie.ecrou.diametre_interieur), mode='s')
       .finalize()
    .extrude(visserie.ecrou.epaisseur)
  )
  return res


def Capteur():
#  longueur_rainure = r(lux.capteur.diametre_pour_dome) - 10
  diametre_maxi = lux.capteur.diametre_pour_dome + 2 * lux.capteur.largeur_bordure
  diametre_mini = lux.tube.diametre_exterieur
  dessus_platine = lux.capteur.hauteur_manchon + lux.capteur.hauteur_platine
  hauteur_totale = lux.capteur.hauteur_bordure + dessus_platine
  largeur_chanfrein = r(diametre_maxi - diametre_mini)
  hauteur_chanfrein = lux.capteur.hauteur_manchon

  passage = (cq
    .Workplane("ZX")
      .cylinder(lux.capteur.longueur_rainure, r(lux.capteur.diametre_trou_fils), centered=(1,1,0))
      .faces(">Y")
        .fillet(r(lux.capteur.diametre_trou_fils) - 0.01)
      .translate((0, 0, dessus_platine))
  )

  res = (cq
    .Workplane("XY")
      .cylinder(hauteur_totale, r(diametre_maxi), centered=(1,1,0))
      .faces("<Z")
        .chamfer(hauteur_chanfrein, largeur_chanfrein)
      .faces(">Z")
        .hole(lux.capteur.diametre_trou_fils)
      .faces(">Z")
        .hole(lux.capteur.diametre_pour_dome, lux.capteur.hauteur_bordure)
      .faces("<Z")
        .workplane(invert=False)
        .hole(lux.capteur.diametre_trou_tube, lux.capteur.hauteur_manchon)
      .edges(cq.NearestToPointSelector((0, diametre_maxi + 1, hauteur_chanfrein + 1)))
        .fillet(2)
  )

  res = (res
    .cut(passage)
    .edges(
      cq.selectors.SumSelector(
        cq.NearestToPointSelector(
          (1, r(lux.capteur.diametre_trou_fils), dessus_platine -r(lux.capteur.diametre_trou_fils) + 0.1)),
        cq.NearestToPointSelector(
          (-1, r(lux.capteur.diametre_trou_fils), dessus_platine -r(lux.capteur.diametre_trou_fils) + 0.1))
      )
    ).fillet(0.5)
  )

  return res


def Butee():
  res = (cq
    .Workplane("XY")
      .cylinder(lux.butee.hauteur, r(lux.butee.diametre),centered=(1,1,0))
      .faces(">Z")
        .fillet(3)
      .faces("<Z")
      .workplane(invert=False)
        .hole(lux.butee.diametre_trou_vis, lux.butee.profondeur_trou_vis)
  )
  return res


def Manchon():
  res = (cq
    .Workplane("XY")
      .cylinder(lux.manchon.hauteur, r(lux.manchon.diametre_exterieur), centered=(1,1,0))
      .faces(">Z")
        .chamfer(lux.manchon.hauteur -0.1, r(lux.manchon.diametre_exterieur - lux.manchon.diametre_trou_tube))
      .faces(">Z")
        .hole(lux.manchon.diametre_trou_tube)
  )
  return res


def Dome():
  res = (cq
    .Workplane("XZ")
      .line(r(lux.dome.corde), 0)
      .ellipseArc(r(lux.dome.corde), lux.dome.fleche, 0,90)
      .close()
      .revolve()
      .faces("<Z")
        .shell(-lux.dome.epaisseur)
  )
  return res


def Pcb():
#lux.pcb.ecart_entre_trous = 9
#lux.pcb.diametre_trous = 3
#lux.pcb_ecart_trous_haut = 2.7

  res = (cq
    .Workplane("XY")
    .box(lux.pcb.largeur, lux.pcb.longueur, lux.pcb.epaisseur_min)
    .faces(">Z")
    .sketch()
       .rect(lux.pcb.ecart_entre_trous, lux.pcb.longueur - 2 * lux.pcb_ecart_trous_haut)
       .vertices(">Y")
#       .moveTo()
       .circle(r(lux.pcb.diametre_trous), mode='s')
       .finalize()
    .extrude(lux.pcb.epaisseur_min)
  )
  return res


def Assemble():

  ass = cq.Assembly()
  intervalle = (
    (visserie.tige.longueur_courte - (visserie.ecrou.epaisseur + visserie.rondelle.epaisseur) * 2) / (coupelle.nombre - 1)
  )

  for i in range(coupelle.nombre):
    ass.add(
      Coupelle(vide=(i > 0 and i < coupelle.nombre - 1), tube=(i == coupelle.nombre - 1)),
      loc=cq.Location((0, 0 , i * intervalle)),
#      color=cq.Color("Brown")
      color=cq.Color(0.55,0.27,0.07,0.7)
    )

    for j in range(4):
      ass.add(
        Rondelle(),
        loc=cq.Location(
          (coupelle.distance_trou_tige * cos(j * pi / 2),
           coupelle.distance_trou_tige * sin(j * pi / 2),
             i * intervalle)),
        color=cq.Color("LightGray")
      )
      ass.add(
        Ecrou(),
        loc=cq.Location(
          (coupelle.distance_trou_tige * cos(j * pi / 2),
           coupelle.distance_trou_tige * sin(j * pi / 2),
             visserie.rondelle.epaisseur + i * intervalle)),
        color=cq.Color("LightGray")
      )
      ass.add(
        Rondelle(),
        loc=cq.Location(
          (coupelle.distance_trou_tige * cos(j * pi / 2),
           coupelle.distance_trou_tige * sin(j * pi / 2),
             i * intervalle - coupelle.epaisseur - visserie.rondelle.epaisseur)),
        color=cq.Color("LightGray")
      )
      ass.add(
        Ecrou(),
        loc=cq.Location(
          (coupelle.distance_trou_tige * cos(j * pi / 2),
           coupelle.distance_trou_tige * sin(j * pi / 2),
             i * intervalle - coupelle.epaisseur - visserie.rondelle.epaisseur - visserie.ecrou.epaisseur)),
        color=cq.Color("LightGray")
      )

  for i in range(4):
    ass.add(
      Tige(i % 2 == 0),
      loc=cq.Location(
        (coupelle.distance_trou_tige * cos(i * pi / 2),
         coupelle.distance_trou_tige * sin(i * pi / 2),
         -coupelle.epaisseur -visserie.ecrou.epaisseur - visserie.rondelle.epaisseur)),
      color=cq.Color("LightGray")
    )

  ass.add(
    Tube(),
    loc=cq.Location(
      (coupelle.distance_trou_tube * cos(pi / 4), coupelle.distance_trou_tube * sin(pi / 4), 0)),
    color=cq.Color(0.18, 0.31, 0.31, 0.7)
    )

  ass.add(
    Capteur(),
    loc=cq.Location(
      (coupelle.distance_trou_tube * cos(pi / 4), coupelle.distance_trou_tube * sin(pi / 4), lux.tube.longueur - lux.capteur.hauteur_manchon)),
    color=cq.Color("Green")
    )

  ass.add(
    Dome(),
    loc=cq.Location(
      (coupelle.distance_trou_tube * cos(pi / 4), coupelle.distance_trou_tube * sin(pi / 4), lux.tube.longueur + lux.capteur.hauteur_platine)),
    color=cq.Color(0.52, 0.76, 0.91, 0.7)
    )

  ass.add(
    Butee(),
    loc=cq.Location(
      (coupelle.distance_trou_tube * cos(pi / 4), coupelle.distance_trou_tube * sin(pi / 4), 0)),
    color=cq.Color("Green")
    )

  ass.add(
    Manchon(),
    loc=cq.Location(
      (coupelle.distance_trou_tube * cos(pi / 4), coupelle.distance_trou_tube * sin(pi / 4), (coupelle.nombre - 1) * intervalle)),
    color=cq.Color("Green")
    )


  return ass



#show_object(Assemble())
#show_object(Coupelle())
#obj = Tige(True)
#show_object(Tube())
#show_object(Rondelle())
#show_object(Ecrou())
#show_object(Butee())
#show_object(Manchon())
#show_object(Dome())
#show_object(Dome2())
#show_object(Pcb())
debug(Pcb())