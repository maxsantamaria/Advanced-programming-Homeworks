- Las personas primero entran a la cola y ahí deciden si se quedan o si se cambian. Estos cambios no cuentan para las estadísticas de cambiarse de cola, sino que era para simplificar el algoritmo y aprovechar la función. Solamente se cuenta como rechazo o cambio de cola si es que llegó un funcionario y el movimiento para la cola hizo que algunos se quisieran ir (función actualizar_cola). Si ya se cambiaron a todas sus opciones, van al Quick Devil
- Se asume que cuando una persona termina de ser atendida y paga, se come instanteamente el producto, asi que se toma en ese instante la putrefaccion y calidad
- Se considera que en ir a comprar snack igual se demoran el tiempo T desde la universidad
- Tiempo que se demoran carabineros en fiscalizar no influye en tiempo maximo de espera
- Para calcular la calidad promedio se tomo el valor de la calidad de los productos al ser comprados (los que no se compraban no se consideraban porque no iban a parar a nuestros queridos clientes)
- Para estadísticas se asume descompuesto como putrefacción > 0.9
- El día en que el vendedor se escapa por no tener permiso no cuenta como parte de los dias susto que no estará
- El dinero confiscado por los carabineros se obtiene multiplicando el stock por el promedio de los precios de cada producto del vendedor

HACER:
- Diferencias funcionarios y alumnos
- Enfermarse(Calidad) y sacar de lista de preferencias ese puesto de venta
- Cambiar probabilidad de comprar snack al llegar
- Recalcular precios al mes
- Carabineros, dias susto
- Bancarrota
- Estadísticas (falta la 1, 3, 15)
- Hacer Quick Devil -> precios productos (si comprador no tiene plata no almuerza)