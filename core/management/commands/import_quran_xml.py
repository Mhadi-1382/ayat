from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from django.db import transaction
from core.models import Surahs, Ayahs

class Command(BaseCommand):
    help = "Import Quran text (Arabic + Farsi) from XML files into database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--ar",
            default="core/data/quran-uthmani.xml",
            help="Path to Arabic Quran XML file"
        )
        parser.add_argument(
            "--fa",
            default="core/data/fa.gharaati.xml",
            help="Path to Farsi Quran translation XML file"
        )

    def handle(self, *args, **options):
        ar_path = options["ar"]
        fa_path = options["fa"]

        self.stdout.write(f"Loading Arabic Quran from: {ar_path}")
        try:
            tree_ar = ET.parse(ar_path)
            root_ar = tree_ar.getroot()
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Error: Arabic XML file not found at {ar_path}"))
            return
        except ET.ParseError:
            self.stderr.write(self.style.ERROR(f"Error: Could not parse Arabic XML file at {ar_path}"))
            return

        self.stdout.write(f"Loading Farsi Quran translation from: {fa_path}")
        try:
            tree_fa = ET.parse(fa_path)
            root_fa = tree_fa.getroot()
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Error: Farsi XML file not found at {fa_path}"))
            return
        except ET.ParseError:
            self.stderr.write(self.style.ERROR(f"Error: Could not parse Farsi XML file at {fa_path}"))
            return
    

        if len(root_ar.findall("sura")) != len(root_fa.findall("sura")):
            self.stdout.write(self.style.WARNING("Warning: Number of surahs in Arabic and Farsi XML files do not match."))

        with transaction.atomic():
            # Loop through surahs
            for sura_ar, sura_fa in zip(root_ar.findall("sura"), root_fa.findall("sura")):
                surah_id = int(sura_ar.get("id"))
                surah_name_ar = sura_ar.get("name_ar")
                surah_name_fa = sura_fa.get("name_fa") or surah_name_ar
                total_ayah_in_sura = len(sura_ar.findall("aya"))

                surah_obj, created = Surahs.objects.update_or_create(
                    id=surah_id,
                    defaults={
                        "name_ar": surah_name_ar,
                        "name_fa": surah_name_fa,
                        "total_ayah": total_ayah_in_sura,
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Surah: {surah_name_fa} ({surah_name_ar})"))
                else:
                    self.stdout.write(f"Updated Surah: {surah_name_fa} ({surah_name_ar})")

                # Loop through ayahs
                ayahs_ar = sura_ar.findall("aya")
                ayahs_fa = sura_fa.findall("aya")

                if len(ayahs_ar) != len(ayahs_fa):
                    self.stdout.write(self.style.WARNING(f"Warning: Number of ayahs in Surah {surah_name_fa} (Arabic: {len(ayahs_ar)}, Farsi: {len(ayahs_fa)}) do not match."))

                for aya_ar, aya_fa in zip(ayahs_ar, ayahs_fa):
                    ayah_number = int(aya_ar.get("index"))
                    text_ar = aya_ar.get("text")
                    text_fa = aya_fa.get("text")

                    Ayahs.objects.update_or_create(
                        surah_id=surah_obj,
                        ayah_number=ayah_number,
                        defaults={
                            "text_ar": text_ar,
                            "text_fa": text_fa,
                        }
                    )

        self.stdout.write(self.style.SUCCESS("Quran XML imported successfully!"))
