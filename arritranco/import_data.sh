#!/bin/bash

FILES="inmuebles.json hardware.json inventario.json backup.tiposdefichero.json backup.planificacion.json backup.patron.json redes.json"
for f in $FILES; do
    echo -n "Comprobando $f ..."
    if [ -f $f ]; then
        echo  " OK"
    else
        echo " ERROR"
    fi
done

echo "Importando datos ... "
python manage.py import_from_old ./inmuebles.json hardware.json inventario.json backup.tiposdefichero.json backup.planificacion.json backup.patron.json redes.json
