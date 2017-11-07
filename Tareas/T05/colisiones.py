def check_collision(objeto1, objeto2):  # true if collides, false if not
    lim_izq1 = objeto1.x
    lim_der1 = objeto1.x + objeto1.image.width()
    lim_sup1 = objeto1.y
    lim_inf1 = objeto1.y + objeto1.image.height()
    lim_izq2 = objeto2.x
    lim_der2 = objeto2.x + objeto2.image.width()
    lim_sup2 = objeto2.y
    lim_inf2 = objeto2.y + objeto2.image.height()

    if (lim_izq1 <= lim_izq2 <= lim_der1 or lim_izq1 <= lim_der2 <= lim_der1) \
            and (lim_sup1 <= lim_sup2 <= lim_inf1 or
                 lim_sup1 <= lim_inf2 <= lim_inf1):
        return True
    else:
        return False


def check_collision_with_label(objeto1, label):  # true if collides, false inot
    lim_izq1 = objeto1.x
    lim_der1 = objeto1.x + objeto1.image.width()
    lim_sup1 = objeto1.y
    lim_inf1 = objeto1.y + objeto1.image.height()
    lim_izq2 = label.x()
    lim_der2 = label.x() + label.width()
    lim_sup2 = label.y()
    lim_inf2 = label.y() + label.height()

    if (lim_izq1 <= lim_izq2 <= lim_der1 or lim_izq1 <= lim_der2 <= lim_der1) \
            and (lim_sup1 <= lim_sup2 <= lim_inf1 or
                 lim_sup1 <= lim_inf2 <= lim_inf1):
        return True
    else:
        return False


def check_click_on_label(mouse, label):
    if label.x() <= mouse.x() <= label.x() + label.width() and \
            label.y() <= mouse.y() <= label.y() + label.height():
        return True
    else:
        return False
