import re as _re
import streamlit as st
import pandas as pd
import random as rn

# ── Sayfa Ayarları ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sezar Şifrelemesi",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Karakter Seti ────────────────────────────────────────────────────────────
# Sıra: Rakamlar → Büyük Harfler → Özel Karakterler
ALFABE = (
    ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    + ["A", "B", "C", "Ç", "D", "E", "F", "G", "Ğ", "H", "I", "İ",
       "J", "K", "L", "M", "N", "O", "Ö", "P", "R", "S", "Ş", "T",
       "U", "Ü", "V", "Y", "Z"]
    + [" ", "!", "?", ".", ",", "-", "_", "@", "#", "$", "%", "&",
       "*", "(", ")", "+", "=", "/"]
)
# Toplam: 10 rakam + 29 büyük + 18 özel = 57 karakter

TR_KUCUK_BUYUK = {
    "a": "A", "b": "B", "c": "C", "ç": "Ç", "d": "D", "e": "E",
    "f": "F", "g": "G", "ğ": "Ğ", "h": "H", "ı": "I", "i": "İ",
    "j": "J", "k": "K", "l": "L", "m": "M", "n": "N", "o": "O",
    "ö": "Ö", "p": "P", "r": "R", "s": "S", "ş": "Ş", "t": "T",
    "u": "U", "ü": "Ü", "v": "V", "y": "Y", "z": "Z",
}
TR_BUYUK_KUCUK = {v: k for k, v in TR_KUCUK_BUYUK.items()}


def _normalize(harf: str) -> str:
    return TR_KUCUK_BUYUK.get(harf, harf.upper())


def sifrele(metin: str, anahtar: int) -> str:
    sonuc = []
    for harf in metin:
        norm = _normalize(harf)
        if norm in ALFABE:
            sonuc.append(ALFABE[(ALFABE.index(norm) - anahtar) % len(ALFABE)])
        else:
            sonuc.append(norm)
    return "".join(sonuc)


def coz_tek(metin: str, anahtar: int) -> str:
    sonuc = []
    for harf in metin:
        norm = _normalize(harf)
        if norm in ALFABE:
            sonuc.append(ALFABE[(ALFABE.index(norm) + anahtar) % len(ALFABE)])
        else:
            sonuc.append(norm)
    return "".join(sonuc)


def tum_cozumler(metin: str):
    return [(i, coz_tek(metin, i)) for i in range(len(ALFABE))]


_TR_HARF_RE = _re.compile(r'[A-ZÇĞIİÖŞÜ]+')


def _kucuk_yap(kelime: str) -> str:
    return "".join(TR_BUYUK_KUCUK.get(ch, ch.lower()) for ch in kelime)


def turkce_skor_wordfreq(metin: str) -> int:
    from wordfreq import word_frequency
    kelimeler = _TR_HARF_RE.findall(metin.upper())
    puan = 0
    for k in kelimeler:
        if len(k) >= 2 and word_frequency(_kucuk_yap(k), "tr") > 0:
            puan += 1
    return puan


# ── Karakter Seti Tablosu (önce hazırla, sayfada kullanılacak) ───────────────
_kategoriler = (
    ["Rakam"] * 10
    + ["Büyük Harf"] * 29
    + ["Özel Karakter"] * 18
)
_karakter_df = pd.DataFrame({
    "N": range(0, len(ALFABE)),
    "Karakter": ALFABE,
    "Kategori": _kategoriler,
})

# ── Oturum Durumu ─────────────────────────────────────────────────────────────
if "sayfa" not in st.session_state:
    st.session_state.sayfa = "sifrele"

# ── Üst Başlık ───────────────────────────────────────────────────────────────
with st.container():
    st.title("🔐 Sezar Şifrelemesi ile Kriptoloji")
    st.caption("2000 Yıllık Antik Şifreleme Yöntemi")

# ── Navigasyon Menüsü ────────────────────────────────────────────────────────
with st.container():
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        if st.button(
            "🔠 Sezar Şifreleme",
            width='stretch',
            type="primary" if st.session_state.sayfa == "sifrele" else "secondary",
        ):
            st.session_state.sayfa = "sifrele"
            st.rerun()

    with m2:
        if st.button(
            "🔓 Şifreyi Kır",
            width='stretch',
            type="primary" if st.session_state.sayfa == "kir" else "secondary",
        ):
            st.session_state.sayfa = "kir"
            st.rerun()

    with m3:
        if st.button(
            "💪 Kaba Kuvvet Analizi",
            width='stretch',
            type="primary" if st.session_state.sayfa == "analiz" else "secondary",
        ):
            st.session_state.sayfa = "analiz"
            st.rerun()

    with m4:
        if st.button(
            "🔬 Antik vs. Modern Yöntemler",
            width='stretch',
            type="primary" if st.session_state.sayfa == "hakkinda" else "secondary",
        ):
            st.session_state.sayfa = "hakkinda"
            st.rerun()

st.divider()

# ── 1. SEZAR ŞİFRELEME SAYFASI ───────────────────────────────────────────────
if st.session_state.sayfa == "sifrele":
        # ── Karakter Seti Tablosu ────────────────────────────────────────────────
    st.markdown("##### Karakter Setimiz  —  N değerleri 0'dan başlar")

    _n_per_row = 10
    _satirlar = []
    for _start in range(0, len(ALFABE), _n_per_row):
        _parca = ALFABE[_start : _start + _n_per_row]
        _satirlar.append({j: ch for j, ch in enumerate(_parca)})

    _df_matris = pd.DataFrame(_satirlar).fillna("")
    _df_matris.columns = range(_n_per_row)

    _n_rows = len(_satirlar)
    _row_px = 35
    _header_px = 38
    _toplam_yukseklik = _header_px + _n_rows * _row_px + 4

    _styled = _df_matris.style.set_table_styles([
        {
            "selector": "thead th",
            "props": [
                ("background-color", "#1e3a5f"),
                ("color", "white"),
                ("font-weight", "bold"),
            ],
        }
    ])

    st.dataframe(
        _styled,
        width='stretch',
        hide_index=True,
        height=_toplam_yukseklik,
    )

    st.write(
        "Şifrelemede kullandığımız **57 karakterlik** özel alfabe yukarıdaki tabloda gösterilmiştir. "
        "Her karakterin sıra numarası (N), şifreleme hesaplamalarında kullanılır."
    )

    st.divider()

    # ── Şifreleme Alanı ───────────────────────────────────────────────────────
    sol, sag = st.columns(2)

    with sol:
        st.markdown("##### ✏️ Metni Şifrele")

        # Otomatik büyük harf: input değiştiğinde normalize et
        if "sifrele_metin" in st.session_state:
            st.session_state["sifrele_metin"] = "".join(
                _normalize(c) for c in st.session_state["sifrele_metin"]
            )

        metin = st.text_area(
            "Şifrelenecek metin",
            height=180,
            placeholder="Şifrelenecek metni buraya yaz...",
            key="sifrele_metin",
            label_visibility="collapsed",
        )

        rastgele = st.checkbox("🎲 Rastgele anahtar seç", value=False)
        if rastgele:
            st.session_state["rastgele_anahtar"] = rn.randint(1, len(ALFABE) - 1)
            anahtar = st.session_state["rastgele_anahtar"]
        else:
            anahtar = st.session_state.get("manuel_anahtar", 3)

        btn_col, key_col = st.columns([1, 2])
        with btn_col:
            sifrele_tikla = st.button("🔒 Şifrele", type="primary", width='stretch')
        with key_col:
            if rastgele:
                st.info(f"Anahtar: **{anahtar}**")
            else:
                anahtar = st.slider(
                    "Anahtar (kaydırma miktarı)",
                    1, len(ALFABE) - 1,
                    st.session_state.get("manuel_anahtar", 3),
                    key="anahtar_slider",
                )
                st.session_state["manuel_anahtar"] = anahtar

        if sifrele_tikla:
            if rastgele:
                st.session_state["rastgele_anahtar"] = rn.randint(1, len(ALFABE) - 1)
                anahtar = st.session_state["rastgele_anahtar"]
            if metin.strip():
                st.session_state["sifreli_sonuc"] = sifrele(metin, anahtar)
                st.session_state["sifreli_anahtar"] = anahtar
                st.session_state["sifreli_metin_girdi"] = metin
            else:
                st.warning("Lütfen şifrelenecek metni gir.")

    with sag:
        st.markdown("##### 🔒 Şifrelenmiş Metin")
        sonuc = st.session_state.get("sifreli_sonuc", "")
        st.code(sonuc if sonuc else " ", language=None)

    # ── Adım Adım Açıklama ───────────────────────────────────────────────────
    girdi = st.session_state.get("sifreli_metin_girdi", "")
    kullanilan_anahtar = st.session_state.get("sifreli_anahtar", 3)
    if girdi:
        st.divider()
        st.markdown("##### 🔍 Şifreleme Nasıl Yapıldı? (İlk 12 karakter)")

        ornek_satir = []
        for harf in girdi[:12]:
            norm = _normalize(harf)
            if norm in ALFABE:
                eski_idx = ALFABE.index(norm)
                yeni_idx = (eski_idx - kullanilan_anahtar) % len(ALFABE)
                yeni = ALFABE[yeni_idx]
                ornek_satir.append({
                    "Orijinal": harf,
                    "N (Orijinal)": eski_idx,
                    "Formül": f"({eski_idx} − {kullanilan_anahtar}) mod {len(ALFABE)} = {yeni_idx}",
                    "N (Şifreli)": yeni_idx,
                    "Şifreli": yeni,
                })
            else:
                ornek_satir.append({
                    "Orijinal": harf,
                    "N (Orijinal)": "—",
                    "Formül": "Alfabe dışı → değişmez",
                    "N (Şifreli)": "—",
                    "Şifreli": harf,
                })

        st.dataframe(pd.DataFrame(ornek_satir), width='stretch', hide_index=True)
        st.write(f"**Formül:** `şifreli_N = (orijinal_N − anahtar) mod {len(ALFABE)}`")

# ── 2. ŞİFREYİ KIR SAYFASI ──────────────────────────────────────────────────
elif st.session_state.sayfa == "kir":
    st.subheader("Sezar Şifreyi Kırma (Kaba Kuvvet)")

    _skor_etiketi = "Türkçe Skoru"

    st.write(
        f"Bilgisayar **{len(ALFABE)} anahtarın tamamını** dener. "
        "Çözümler anahtar sırasıyla listelenir; **wordfreq** Türkçe frekans "
        "veritabanı ile hesaplanan skor her satırda gösterilir."
    )

    # En son şifrelenen metin değiştiyse kir_metin'i otomatik güncelle
    _son_sifreli = st.session_state.get("sifreli_sonuc", "")
    if _son_sifreli != st.session_state.get("_kir_sync_cache", None):
        st.session_state["kir_metin"] = _son_sifreli
        st.session_state["_kir_sync_cache"] = _son_sifreli

    # Kullanıcı elle girdiyse de uppercase yap
    if st.session_state.get("kir_metin"):
        st.session_state["kir_metin"] = "".join(_normalize(c) for c in st.session_state["kir_metin"])

    sifreli_giris = st.text_area(
        "Şifreli metin",
        height=140,
        key="kir_metin",
    )

    kir = st.button("🔓 Şifreyi Kır!", type="primary", width='stretch')

    if kir and sifreli_giris.strip():
        with st.spinner(f"{len(ALFABE)} olası anahtar deneniyor..."):
            sonuclar = tum_cozumler(sifreli_giris)
            puanli = [
                {"Anahtar": a, "Çözüm": c, _skor_etiketi: turkce_skor_wordfreq(c)}
                for a, c in sonuclar
            ]
            # Anahtar sıralı, skor sıralaması yok
            df = pd.DataFrame(puanli).sort_values("Anahtar", ascending=True).reset_index(drop=True)

        max_skor = int(df[_skor_etiketi].max())
        en_iyiler = df[df[_skor_etiketi] == max_skor].reset_index(drop=True)

        c1, c2, c3 = st.columns(3)
        anahtarlar_str = ", ".join(str(int(a)) for a in en_iyiler["Anahtar"])
        c1.metric("En Yüksek Skorlu Anahtar(lar)", anahtarlar_str)
        c2.metric(_skor_etiketi, max_skor)
        c3.metric("Toplam Deneme", len(ALFABE))

        _sonuc_metni = "\n\n".join(
            f"**🎯 Anahtar = {int(satir['Anahtar'])}** — {satir['Çözüm']}"
            for _, satir in en_iyiler.iterrows()
        )
        st.success(_sonuc_metni)

        st.markdown(f"##### 📊 Tüm {len(ALFABE)} Çözüm (Anahtar Sıralı)")
        st.dataframe(
            df,
            width='stretch',
            hide_index=True,
            column_config={
                "Anahtar": st.column_config.NumberColumn("Anahtar", width="small"),
                "Çözüm": st.column_config.TextColumn("Çözüm", width="large"),
                _skor_etiketi: st.column_config.ProgressColumn(
                    _skor_etiketi,
                    min_value=0,
                    max_value=max(int(df[_skor_etiketi].max()), 1),
                    format="%d",
                ),
            },
        )

        st.info(
            f"💡 **Sonuç:** Sezar şifresinin yalnızca {len(ALFABE)} olası anahtarı vardır. "
            "Modern bir bilgisayar bunu **milisaniyenin altında** kırar!"
        )

        st.divider()
        st.markdown(
            "**Türkçe Skoru Nasıl Hesaplanır?**\n\n"
            "Her anahtar için üretilen çözüm metninden yalnızca **harf dizileri** "
            "ayrıştırılır — noktalama ve rakamlar yok sayılır. "
            "Her harf dizisi **wordfreq** kütüphanesiyle Türkçe kelime frekans veritabanında aranır. "
            "wordfreq, milyarlarca gerçek metinden derlenen kelime sıklığı verilerini içerir; "
            "bir kelimenin Türkçe (`tr`) veri tabanında frekansı sıfırdan büyükse "
            "skora **+1** eklenir. "
            "Skor ne kadar yüksekse çözüm o kadar çok gerçek Türkçe kelime içeriyor demektir — "
            "en yüksek skorlu anahtar büyük olasılıkla doğru anahtardır."
        )
    elif kir:
        st.warning("Lütfen bir şifreli metin gir.")

# ── 3. KABA KUVVET ANALİZİ SAYFASI ──────────────────────────────────────────
elif st.session_state.sayfa == "analiz":
    import math as _math
    import plotly.graph_objects as _go

    st.subheader("Kaba Kuvvet ile Şifre Kırma Analizi")

    _HAVUZ_KATEGORILER = {
        "🔢 Rakamlar": 10,
        "🔠 Büyük Harfler (TR)": 29,
        "🔡 Küçük Harfler (TR)": 29,
        "🔣 Özel Karakterler": 18,
    }

    def _buyuk_sayi_tr(log10_n: float) -> str:
        if log10_n <= 0:
            return "0"
        if log10_n < 3:
            return f"{int(round(10**log10_n))}"
        _birimler = [
            (33, "desilyon"), (30, "nonilyon"), (27, "oktilyon"),
            (24, "septilyon"), (21, "sekstilyon"), (18, "kentilyon"),
            (15, "katrilyon"), (12, "trilyon"), (9, "milyar"),
            (6, "milyon"), (3, "bin"),
        ]
        for _exp, _isim in _birimler:
            if log10_n >= _exp:
                _katsayi = log10_n - _exp
                if _katsayi < 3:
                    return f"{10**_katsayi:.1f} {_isim}"
                break
        _ie = int(log10_n)
        _m = 10 ** (log10_n - _ie)
        return f"{_m:.1f} × 10^{_ie}"

    def _sure_hesapla(log10_saniye: float) -> str:
        if log10_saniye < -3:
            return "< 1 milisaniye"
        if log10_saniye < 0:
            return f"{10**(log10_saniye+3):.0f} milisaniye"
        if log10_saniye < _math.log10(60):
            return f"{10**log10_saniye:.0f} saniye"
        _log_yil = _math.log10(365.25 * 24 * 3600)
        if log10_saniye >= _log_yil + 9:
            return _buyuk_sayi_tr(log10_saniye - _log_yil) + " yıl"
        if log10_saniye > 15:
            _ty = 10 ** (log10_saniye - _log_yil)
            _y = int(_ty)
            _af = (_ty - _y) * 12
            _a = int(_af)
            _g = int((_af - _a) * 30)
            return f"{_y:,} yıl {_a} ay {_g} gün".replace(",", ".")
        _s = int(10 ** log10_saniye)
        _y = _s // (365 * 86400); _s -= _y * (365 * 86400)
        _a = _s // (30 * 86400);  _s -= _a * (30 * 86400)
        _g = _s // 86400;         _s -= _g * 86400
        _sa = _s // 3600;         _s -= _sa * 3600
        _dk = _s // 60;           _sn = _s % 60
        if _y > 0:
            return f"{_y:,} yıl {_a} ay {_g} gün".replace(",", ".")
        if _a > 0:
            return f"{_a} ay {_g} gün {_sa} saat"
        if _g > 0:
            return f"{_g} gün {_sa} saat {_dk} dakika"
        if _sa > 0:
            return f"{_sa} saat {_dk} dakika {_sn} saniye"
        if _dk > 0:
            return f"{_dk} dakika {_sn} saniye"
        return f"{_sn} saniye"

    # ── Şifre Test Kutusu ────────────────────────────────────────────────────
    _ps_sol, _ps_sag = st.columns([2, 5])
    with _ps_sol:
        st.markdown("##### 🔐 Şifreni Dene (Enter'a Bas)")
        _test_sifre = st.text_input(
            "Şifre",
            type="password",
            placeholder="Bir şifre yaz...",
            label_visibility="collapsed",
            key="ps_test_input",
        )
    with _ps_sag:
        st.markdown("##### ⏱️ Kırılma Süresi")
        if _test_sifre:
            _kats_var = {
                "🔢 Rakamlar": any(c.isdigit() for c in _test_sifre),
                "🔠 Büyük Harfler (TR)": any(
                    c.isupper() or c in TR_KUCUK_BUYUK.values() for c in _test_sifre
                ),
                "🔡 Küçük Harfler (TR)": any(
                    c.islower() or c in TR_KUCUK_BUYUK for c in _test_sifre
                ),
                "🔣 Özel Karakterler": any(
                    (not c.isalnum()) for c in _test_sifre
                ),
            }
            _ps_havuz = sum(
                _HAVUZ_KATEGORILER[k] for k, v in _kats_var.items() if v
            ) or 1
            _ps_uzunluk = len(_test_sifre)
            _ps_log_deneme = _ps_uzunluk * (
                _math.log10(_ps_havuz) if _ps_havuz > 1 else 0.0
            )
            _ps_log_saniye = _ps_log_deneme - 9
            _kullanilan = [k for k, v in _kats_var.items() if v]
            st.success(
                f"**{_sure_hesapla(_ps_log_saniye)}**  \n"
                f"Havuz: {_ps_havuz} karakter · Uzunluk: {_ps_uzunluk} · "
                f"Toplam deneme: {_buyuk_sayi_tr(_ps_log_deneme)}  \n"
                f"Tespit edilen kategoriler: {', '.join(_kullanilan)}"
            )
            st.caption("Varsayım: saniyede 1 milyar deneme yapan bir bilgisayar.")
        else:
            st.info("Sol kutuya bir şifre yaz; süre burada anında belirir.")

    st.divider()

    st.write(
        "Sağdan karakter kategorilerini seç ve şifre uzunluğunu değiştir. "
        "Aşağıdaki **şelale grafiği**, seçtiğin her kategorinin deneme sayısı'na "
        "yaptığı katkıyı ve toplam ihtimali gösterir."
    )

    _sol, _sag = st.columns([3, 1])

    with _sag:
        st.markdown("##### Karakter Havuzu")
        st.caption("Seç → şelalenin çubukları büyür")
        _secim = st.pills(
            "Kategoriler",
            list(_HAVUZ_KATEGORILER.keys()),
            selection_mode="multi",
            label_visibility="collapsed",
        )
        _havuz = sum(_HAVUZ_KATEGORILER[k] for k in (_secim or [])) or 1
        st.metric("Toplam Havuz", f"{_havuz} karakter")

        st.divider()

        st.markdown("##### Şifre Uzunluğu")
        st.caption("Artır → tüm çubuklar orantılı yükselir")
        _uzunluk = st.slider("Uzunluk", 1, 120, 8, label_visibility="collapsed")

    with _sol:
        _log10_h = _math.log10(_havuz) if _havuz > 1 else 0.0

        # Kanonik sıra: pills seçim sırasını korumayabildiği için sabit kategori sırası kullanılır
        _KANONIK_SIRA = list(_HAVUZ_KATEGORILER.keys())
        _secili_sirali = [k for k in _KANONIK_SIRA if k in (_secim or [])]

        st.markdown(f"##### 📈 Toplam Deneme Grafiği")
        st.caption(
            f"Şifre uzunluğu = **{_uzunluk}**. Her çubuk, o kategori havuza eklendiğinde "
            "deneme sayısı'nın **ne kadar yükseldiğini** gösterir. "
            "Yeşil son sütun toplam değerdir. Aynı kategoriler tek tek değil, "
            "birlikte eklendiğinde toplam etki çarpıcı biçimde büyür."
        )

        if not _secili_sirali:
            st.info("Sağdaki Karakter Havuzu'ndan en az bir kategori seç.")
        else:
            _kumulatif = 0
            _isimler = []
            _katkilar = []
            for _k in _secili_sirali:
                _onceki = _kumulatif
                _kumulatif += _HAVUZ_KATEGORILER[_k]
                _yeni_y = _math.log10(_kumulatif) * _uzunluk
                _eski_y = (_math.log10(_onceki) * _uzunluk) if _onceki > 0 else 0.0
                _isimler.append(_k)
                _katkilar.append(_yeni_y - _eski_y)

            _isimler.append("TOPLAM")
            _katkilar.append(0.0)
            _measure = ["relative"] * len(_secili_sirali) + ["total"]
            _toplam_log = sum(_katkilar)

            _fig = _go.Figure(_go.Waterfall(
                orientation="v",
                measure=_measure,
                x=_isimler,
                y=_katkilar,
                text=[f"+{v:.2f}" for v in _katkilar[:-1]] + [f"{_toplam_log:.2f}"],
                textposition="outside",
                connector={"line": {"color": "rgb(140,140,140)", "dash": "dot"}},
                increasing={"marker": {"color": "#2563eb"}},
                totals={"marker": {"color": "#16a34a"}},
            ))
            _fig.update_layout(
                yaxis_title="log₁₀(deneme sayısı) katkısı",
                xaxis_title=None,
                height=400,
                margin=dict(l=10, r=10, t=20, b=10),
                showlegend=False,
            )
            st.plotly_chart(_fig, width='stretch')

    st.divider()

    _log_deneme = _uzunluk * _log10_h
    _log_saniye = _log_deneme - 9

    _m1, _m2, _m3 = st.columns(3)
    _m1.metric("Havuz Büyüklüğü", f"{_havuz} karakter")
    _m2.metric("Toplam Deneme Sayısı", _buyuk_sayi_tr(_log_deneme))
    _m3.metric("Kırılma Süresi (1 milyar/sn)", _sure_hesapla(_log_saniye))


# ── 4. MODERN YÖNTEMLER SAYFASI ─────────────────────────────────────────────
elif st.session_state.sayfa == "hakkinda":
    st.subheader("Antik Çağdan Modern Kriptografiye")

    st.write(
        "Sezar şifresi sadece **57 anahtarla** milisaniyede kırılır. Peki bugün "
        "bankaların, WhatsApp'ın, internet sitelerinin kullandığı yöntemler "
        "neden bu kadar güçlü? Solda binlerce yıllık antik yöntemleri, sağda "
        "günümüzün modern yöntemlerini yan yana göreceksin."
    )

    st.divider()

    _antik_kol, _modern_kol = st.columns(2, gap="large")

    # ─────────────── SOL: ANTİK YÖNTEMLER ────────────────────────────────────
    with _antik_kol:
        st.markdown("### 🏛️ Antik Yöntemler")
        st.caption("Hepsi bugün bir bilgisayarla **kolayca kırılır** — tarihsel önemi vardır.")

        # Sezar
        st.markdown("#### 🔠 Sezar Şifresi (MÖ 1. yüzyıl)")
        st.write(
            "Julius Caesar'ın askeri haberleşmede kullandığı yöntem. Her harfi "
            "alfabede sabit sayıda **kaydırırsın**. Anahtar bu kaydırma sayısıdır."
        )
        st.markdown(
            "**Nasıl çalışır?**\n"
            "- Diyelim anahtar = 3.\n"
            "- A → D, B → E, C → F ... şeklinde kaydırırsın.\n"
            "- Çözmek için aynı miktarda ters yöne kaydırırsın.\n\n"
            "**Matematik dili:** `şifreli_harf = (orijinal_harf + anahtar) mod alfabe_boyutu`"
        )
        st.markdown(
            "**Kırılması:** Alfabede sadece **25–60 olası anahtar** vardır. "
            "Bilgisayar hepsini tek tek dener ve **milisaniyenin altında** doğrusunu bulur. "
            "(Bu projenin yaptığı tam olarak bu!)"
        )

        st.divider()

        # Vigenère
        st.markdown("#### 🔡 Vigenère Şifresi (1553)")
        st.write(
            "Sezar'ın geliştirilmiş hâli. Sabit bir sayı yerine **anahtar kelime** "
            "kullanılır. Her harf farklı miktarda kaydırılır — bu da frekans desenini bozar."
        )
        st.markdown(
            "**Nasıl çalışır?**\n"
            "- Anahtar kelime: `KEDI`. Mesaj: `MERHABA`.\n"
            "- 1. harf K kadar (10), 2. harf E kadar (4), 3. harf D kadar (3), 4. harf I kadar (8) kaydır.\n"
            "- Anahtar bittiğinde başa dön: 5. harf yine K kadar...\n\n"
            "**Matematik dili:** Sezar'ı uygula ama anahtar her harf için döngüsel olarak değişir."
        )
        st.markdown(
            "**Kırılması:** 300 yıl boyunca \"kırılamaz\" sanıldı. 1863'te Kasiski "
            "**tekrar eden harf gruplarını** sayarak anahtar uzunluğunu bulmayı keşfetti. "
            "Anahtar uzunluğunu bilince mesaj **birden çok küçük Sezar şifresine** "
            "ayrılır — her biri ayrı ayrı kırılır. Bilgisayarla **saniyeler** sürer."
        )

        st.divider()

        # Enigma
        st.markdown("#### ⚙️ Enigma (II. Dünya Savaşı, 1939-1945)")
        st.write(
            "Almanların kullandığı elektromekanik şifre makinesi. İçinde dönen "
            "**rotorlar** vardı; her harf yazıldığında rotorlar dönerdi, yani "
            "aynı harf bile her seferinde **farklı şekilde şifrelenirdi**."
        )
        st.markdown(
            "**Nasıl çalışır?**\n"
            "- 3 rotor + bağlantı panosu vardı.\n"
            "- Her tuşa basıldığında rotor 1 adım dönerdi (saat gibi).\n"
            "- Olası başlangıç ayarı sayısı yaklaşık **150 katrilyon (1,5 × 10²³)**.\n\n"
            "**Matematik dili:** Her harf için ayrı bir karıştırma fonksiyonu — "
            "ama fonksiyon her adımda değişir."
        )
        st.markdown(
            "**Kırılması:** Alan Turing ve ekibi Bletchley Park'ta **Bombe** adlı "
            "makineyi inşa etti. Almanların her mesaja \"Heil Hitler\" gibi tahmin "
            "edilebilir kelimeler koyması büyük zayıflıktı. **Günler içinde** "
            "günlük anahtarları kırdılar. Bu, bilgisayarın doğuşuna ve savaşın "
            "2 yıl erken bitmesine sebep oldu."
        )

        st.divider()

        # Antik kırılma tablosu
        st.markdown("##### ⏱️ Antik Yöntemlerin Kırılma Süreleri")
        st.caption("Saniyede 1 milyar deneme yapan bir bilgisayarla.")
        _antik_karsi = pd.DataFrame([
            {"Yöntem": "Sezar",    "Olası Anahtar": "≈ 60",                    "Kırılma": "< 1 milisaniye"},
            {"Yöntem": "Vigenère", "Olası Anahtar": "Anahtar uzunluğuna bağlı", "Kırılma": "Saniyeler"},
            {"Yöntem": "Enigma",   "Olası Anahtar": "≈ 150 katrilyon",          "Kırılma": "Saatler"},
        ])
        st.dataframe(_antik_karsi, width='stretch', hide_index=True)

    # ─────────────── SAĞ: MODERN YÖNTEMLER ───────────────────────────────────
    with _modern_kol:
        st.markdown("### 🔬 Modern Yöntemler")
        st.caption("Matematiksel zorluğa dayanır — bilgisayarlar bile yeterli kalmıyor.")

        # AES
        st.markdown("#### 🔒 AES (2001 — bugünün standardı)")
        st.write(
            "Bilgisayarların kullandığı şifreleme yönteminin adı. WiFi şifren, "
            "telefondaki fotoğraflar, banka uygulaması — hepsi bunu kullanır. "
            "Aynı anahtar hem şifreler hem çözer."
        )
        st.markdown(
            "**Nasıl çalışır?**\n"
            "- Mesaj **16 baytlık küçük bloklara** bölünür.\n"
            "- Her blok 10-14 **tur** boyunca karıştırılır:\n"
            "  - Harfler bir tabloya göre **değiştirilir** (karıştırma).\n"
            "  - Satırlar **kaydırılır**, sütunlar **harmanlanır** (yayılma).\n"
            "  - Her turda anahtarla **toplama yapılır** (gizleme).\n"
            "- Tek bir bit değiştirsen şifreli metnin **yarısı değişir**.\n\n"
            "**Anahtar boyutu:** 256 bit → toplam **2²⁵⁶ ≈ 10⁷⁷** olası anahtar."
        )
        st.markdown(
            "**Kırılması:** Saniyede 1 milyar anahtar deneyen bir bilgisayarla bile "
            "tüm anahtarları denemek **evrenin yaşının trilyonlarca katı** sürer. "
            "Evrendeki atom sayısı yaklaşık 10⁸⁰ — AES'in anahtar sayısı buna yakın! "
            "Bugüne kadar **pratik bir kırma yöntemi bulunamadı**."
        )

        st.divider()

        # RSA
        st.markdown("#### 🔑 RSA (1977 — iki anahtarlı sihir)")
        st.write(
            "Tek bir gizli anahtar yerine **iki ayrı anahtar** kullanır: "
            "**açık anahtar** (herkesle paylaşılır, şifreler) ve "
            "**özel anahtar** (sende kalır, sadece o çözebilir). "
            "Web sitelerindeki yeşil kilit (HTTPS) bunun sayesinde çalışır."
        )
        st.markdown(
            "**Nasıl çalışır?**\n"
            "- İki büyük **asal sayı** seç: `p` ve `q` (her biri yüzlerce basamak).\n"
            "- Bunları çarp: `N = p × q`. `N`'i herkese ver, `p` ve `q`'yu sakla.\n"
            "- Şifreleme/çözme `N` üzerinden üs alma ile yapılır.\n\n"
            "**Sihirli kısım:** İki büyük sayıyı çarpmak **kolay**, ama elindeki "
            "çarpımdan tekrar `p` ve `q`'yu bulmak **çok zor**. Örnek: "
            "`17 × 23 = 391` kolay. Ama sana sadece `391` versem `p` ve `q`'yu "
            "bulman uzun sürer. 600 basamaklı sayılarda bu **imkânsıza yakın**."
        )
        st.markdown(
            "**Kırılması:** 2048 bit'lik bir `N`'i asallarına ayırmak en hızlı "
            "bilgisayarlarla bile **milyarlarca yıl** alır. **Ama:** Geleceğin "
            "**kuantum bilgisayarları** bunu çok hızlı yapabilir; o yüzden "
            "bilim insanları şimdiden yeni \"kuantum-dayanıklı\" yöntemler "
            "geliştiriyor."
        )

        st.divider()

        # SHA-256
        st.markdown("#### #️⃣ SHA-256 (Hash — Dijital Parmak İzi)")
        st.write(
            "Bu bir şifreleme **değil**. Bir mesajı (uzun ya da kısa) alıp "
            "ondan **sabit boyutlu (256 bitlik) bir özet** üretir. Her mesajın "
            "kendine özgü bir parmak izi olur. Parolaların saklanmasında, "
            "Bitcoin'de, dosya bütünlüğü kontrolünde kullanılır."
        )
        st.markdown(
            "**Özellikleri:**\n"
            "- **Tek yönlü:** Mesajdan parmak izi üretmek **kolay**, parmak izinden "
            "mesajı geri bulmak **imkânsız**.\n"
            "- **Kelebek etkisi:** Mesajda 1 harf değişse bile parmak izinin "
            "**yarısı tamamen değişir**.\n"
            "- **Aynı Hash'in Denk Gelmesi:** İki farklı mesajın aynı parmak izini (hash) vermesi "
            "neredeyse imkânsız (≈ 2¹²⁸ deneme gerekir).\n"
        )
        st.code(
            'SHA256("merhaba")  → 7e6f...3b9a\n'
            'SHA256("merhabA")  → c4a1...e2f7   (tek harf değişti, sonuç tamamen farklı!)',
            language="text",
        )
        st.markdown(
            "**Kırılması:** Birinin aynı parmak izini veren başka bir mesaj "
            "bulması gerekir. Bunun olasılığı **2¹²⁸'de 1** — yani aynı anda "
            "milyarlarca kişi denese bile evrenin yaşı kadar zaman yetmez. "
            "**Bugüne kadar başarılmadı.**"
        )

        st.divider()

        # Modern kırılma tablosu
        st.markdown("##### ⏱️ Modern Yöntemlerin Kırılma Süreleri")
        st.caption("Saniyede 1 milyar deneme yapan bir bilgisayarla.")
        _modern_karsi = pd.DataFrame([
            {"Yöntem": "AES-128",  "Anahtar Uzayı": "2¹²⁸ ≈ 10³⁸", "Kırılma": "≈ 10²² yıl"},
            {"Yöntem": "AES-256",  "Anahtar Uzayı": "2²⁵⁶ ≈ 10⁷⁷", "Kırılma": "Evrenin yaşının trilyon katı"},
            {"Yöntem": "RSA-2048", "Anahtar Uzayı": "≈ 10⁶¹⁷",     "Kırılma": "Milyarlarca yıl"},
            {"Yöntem": "SHA-256",  "Anahtar Uzayı": "2¹²⁸ ≈ 10³⁸", "Kırılma": "≈ 10²² yıl (çakışma için)"},
        ])
        st.dataframe(_modern_karsi, width='stretch', hide_index=True)

    st.divider()

    st.success(
        "🎯 **Esas Mesele:** Antik yöntemler **gizli bir algoritmaya** güvenirdi — "
        "düşman algoritmayı öğrenince kırılırdı. Modern yöntemler ise tam tersi: "
        "**algoritma herkese açıktır**, güvenlik tek bir **matematiksel zorluğa** "
        "(asal çarpanlara ayırma, tüm anahtarları deneme) dayanır. "
        "Çünkü bu zorluk evrenin gücüyle bile çözülemeyecek kadar büyüktür."
    )
