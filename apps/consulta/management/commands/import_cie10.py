"""Carga el catálogo CIE-10 desde el CSV jerarquizado de verasativa/CIE-10.

Formato esperado (cabecera incluida)::

    code,code_0,code_1,code_2,code_3,code_4,description,level,source
    A00-B99,,,,,,Ciertas enfermedades infecciosas y parasitarias,0,icdcode.info
    I10,I00-I99,I10-I15,,,,Hipertensión esencial (primaria),2,icdcode.info

`code_0` es el capítulo, `code_1` el bloque y `level` la profundidad.
El comando es idempotente: crea los códigos nuevos y actualiza descripción,
nivel y jerarquía de los existentes.
"""

from __future__ import annotations

import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.consulta.models import CodigoCie10, normalizar_texto

DEFAULT_CSV = Path(settings.BASE_DIR) / "data" / "cie10" / "cie-10.csv"


class Command(BaseCommand):
    help = "Importa el catálogo CIE-10 desde un CSV jerarquizado (code, code_0..4, description, level)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            default=str(DEFAULT_CSV),
            help=f"Ruta del CSV (por defecto {DEFAULT_CSV}).",
        )
        parser.add_argument(
            "--truncate",
            action="store_true",
            help="Vacía el catálogo antes de cargar (no toca diagnósticos existentes).",
        )

    def handle(self, *args, **options):
        ruta = Path(options["csv"])
        if not ruta.exists():
            raise CommandError(
                f"No existe el CSV: {ruta}\n"
                "Descárgalo de https://github.com/verasativa/CIE-10 (cie-10.csv) "
                "o pasa --csv con la ruta correcta."
            )

        if options["truncate"]:
            borrados, _ = CodigoCie10.objects.all().delete()
            self.stdout.write(f"Catálogo vaciado ({borrados} filas).")

        with ruta.open(encoding="utf-8-sig", newline="") as fh:
            lector = csv.DictReader(fh)
            filas = list(lector)

        if not filas or "code" not in filas[0] or "description" not in filas[0]:
            raise CommandError("El CSV no tiene las columnas 'code' y 'description'.")

        existentes = {
            c.codigo: c for c in CodigoCie10.objects.all().only("codigo", "descripcion", "nivel")
        }
        nuevos: list[CodigoCie10] = []
        actualizados: list[CodigoCie10] = []
        sin_cambio = 0

        for fila in filas:
            codigo = (fila.get("code") or "").strip().upper()
            descripcion = " ".join((fila.get("description") or "").split())
            if not codigo or not descripcion:
                continue

            nivel = int(fila.get("level") or 2)
            capitulo = (fila.get("code_0") or "").strip()
            bloque = (fila.get("code_1") or "").strip()
            es_hoja = nivel >= 2

            actual = existentes.get(codigo)
            if actual is None:
                nuevos.append(
                    CodigoCie10(
                        codigo=codigo,
                        descripcion=descripcion,
                        nivel=nivel,
                        capitulo=capitulo,
                        bloque=bloque,
                        es_hoja=es_hoja,
                        busqueda=normalizar_texto(f"{codigo} {descripcion}"),
                    )
                )
                continue

            if (
                actual.descripcion == descripcion
                and actual.nivel == nivel
            ):
                sin_cambio += 1
                continue

            actual.descripcion = descripcion
            actual.nivel = nivel
            actual.capitulo = capitulo
            actual.bloque = bloque
            actual.es_hoja = es_hoja
            actual.busqueda = normalizar_texto(f"{codigo} {descripcion}")
            actualizados.append(actual)

        with transaction.atomic():
            if nuevos:
                CodigoCie10.objects.bulk_create(nuevos, batch_size=1000)
            if actualizados:
                CodigoCie10.objects.bulk_update(
                    actualizados,
                    ["descripcion", "nivel", "capitulo", "bloque", "es_hoja", "busqueda"],
                    batch_size=1000,
                )

        total = CodigoCie10.objects.count()
        hojas = CodigoCie10.objects.filter(es_hoja=True).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"CIE-10 importado: {len(nuevos)} nuevos, {len(actualizados)} actualizados, "
                f"{sin_cambio} sin cambios. Catálogo: {total} códigos ({hojas} consultables)."
            )
        )
