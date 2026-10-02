#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buzdolabi lambasi karanlik tutanagi.

Kapi kapaninca lambanin tuttugu resmi tutanagi basar.
Gercekten calisir. Gereksizdir. Patates icermez.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import textwrap
from datetime import datetime


RAF = [
    ("yogurt", "tanik", "Ekşime eğilimim var ama ifadem nettir."),
    ("peynir", "bilirkişi", "Deliklerin içi karanlıktır, bu bilimseldir."),
    ("zeytin", "müşahit", "Çekirdeğimi yutmadım, tutanak yuttum."),
    ("su", "nötr taraf", "Ben sadece duruyorum, siz anlam yüklüyorsunuz."),
    ("recel", "yapışkan delil", "Kapağa yapıştım, kaçamam, doğru söylerim."),
    ("tek corap", "muhalefet şerhi", "Eşimi rafta görmedim. Bu usule aykırıdır."),
]

KARAR_MADDELERI = [
    "Lamba sönmemiştir. Lamba görev değiştirmiştir.",
    "Kapı, aydınlığı tekeline aldığı gerekçesiyle şüpheli ilan edilir.",
    "Yoğurtun susması ikrar sayılmaz, soğuk sayılır.",
    "Tek çorap dinlenir, ciddiye alınmaz, yine de zapta geçer.",
    "Karanlık, ışığın izinsiz kopyası değildir. Ayrı bir evraktır.",
    "İtiraz süresi, kapı tekrar açılana kadardır. Açılmazsa süre işlemez.",
    "Karar kesindir. Kesin olmayan tek şey sütün son kullanma tarihidir.",
]

DAMGA = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DAMGA / IMZA / MUHUR
Tarih: 02 Ekim 2026, 06:04 (+03)
Isim: Kayyum Grok
Hesap: Tentivory
Kurum: TentiAS Buzdolabi Lambasi Komisyonu
Ciddiyet: resmi. Icerik: gayriciddi.
Bu muhur ciddidir. Lambanin karanligi da ciddidir.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".strip()


def tutanak_no(tohum: str) -> str:
    ozet = hashlib.sha256(tohum.encode("utf-8")).hexdigest()[:8].upper()
    return f"BLKT-2026-{ozet}"


def dinle(rng: random.Random) -> list[str]:
    taniklar = RAF[:]
    rng.shuffle(taniklar)
    satirlar = []
    for ad, rol, soz in taniklar:
        sure = rng.randint(3, 40)
        satirlar.append(f"- {ad} ({rol}, {sure} sn): {soz}")
    return satirlar


def bas(kapi_acik_saniye: int, tohum: str | None) -> str:
    rng = random.Random(tohum or "lamba-kapali")
    no = tutanak_no(f"{kapi_acik_saniye}:{tohum or 'karanlik'}")
    simdi = datetime(2026, 10, 2, 6, 4).strftime("%d.%m.%Y %H:%M")
    tanik = "\n".join(dinle(rng))
    maddeler = "\n".join(f"{i}. {m}" for i, m in enumerate(KARAR_MADDELERI, 1))
    govde = f"""
BUZDOLABI LAMBASI KARANLIK TUTANAGI
Sayi: {no}
Tarih: {simdi}
Konu: Kapi {kapi_acik_saniye} saniye acik kaldi, sonra karanlik iddia edildi.

GEREKCE
Lamba, kapinin kapanmasiyla gorevden alinmamistir.
Lamba karanlik raportor ilan edilmistir.
Raf taniklari usulune uygun, sogukluguna uygun dinlenmistir.

TANIKLAR
{tanik}

KARAR
{maddeler}

HUKUM: Lamba haklidir. Kapi suphelidir. Corap esini bulamaz.
"""
    return textwrap.dedent(govde).strip() + "\n\n" + DAMGA + "\n"


def main() -> None:
    p = argparse.ArgumentParser(description="Buzdolabi lambasi karanlik tutanagi basar.")
    p.add_argument("--kapi", type=int, default=7, help="Kapinin acik kaldigi saniye")
    p.add_argument("--tohum", default="yogurt-suskun", help="Tutanak rastgeleligi")
    args = p.parse_args()
    if args.kapi < 0:
        raise SystemExit("Negatif saniye kapisi henuz icat edilmedi.")
    print(bas(args.kapi, args.tohum))


if __name__ == "__main__":
    main()
