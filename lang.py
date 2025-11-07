from converters import convert_to_cyrillic, convert_to_latin

LANGUAGES = {
    'uz_latin': {
        'select_language': "Iltimos, tilni tanlang:",
        'language_set': "Til muvaffaqiyatli o‘zgartirildi!",
        'welcome': "Botga xush kelibsiz! Firma STIR raqamini kiriting (9 raqam, masalan: 123456789):",
        'enter_cyrillic_text': "Kirill alifbosidagi matnni kiriting:",
        'enter_latin_text': "Lotin alifbosidagi matnni kiriting:",
        'translated_text': "Tarjima qilingan matn: {text}",
        'invalid_stir': "❌ Bu STIR bo'yicha firma topilmadi.",
        'select_tax_type': "📊 STIR: {stir}\nSoliq turini tanlang:",
        'select_month': "📅 {soliq_turi} uchun oyni tanlang:",
        'file_not_found': "❌ {oy} uchun fayl topilmadi.",
        'file_error': "❌ Faylni yuklashda xato yuz berdi: {error}",
        'yagona_file_not_found': "❌ {oy} uchun yagona soliq fayli topilmadi.",
        'yagona_error': "❌ Yagona soliq hisobotida xato: {error}",
        'qqs_file_not_found': "❌ {oy} uchun QQS fayli topilmadi.",
        'qqs_error': "❌ QQS hisobotida xato: {error}",
        'no_manual_report': "❌ {oy} uchun qo'lda kiritilgan hisobot topilmadi.",
        'back_options': "Quyidagi variantlardan birini tanlang:",
        'excel1_not_found': "📋 1-Excel faylni hisobotlarni yaratib qo‘ying iltimos, so‘ng 2-Excel faylni yuklang (.xlsx):",
        'excel1_uploaded': "✅ 1-Excel fayl yuklangan, endi 2-Excel faylni yuklang (.xlsx):",
        'firma_info': "📋 Firma xaqida malumot\n\n"
                      "🏢 STIR: {stir}\n"
                      "🏢 Firma nomi: {firma_nomi}\n"
                      "👤 Rahbar: {rahbar}\n"
                      "📊 Soliq turi: {soliq_turi}\n\n"
                      "📌 Soliq stavkalari:\n"
                      "🔹 Daromad soligi (DS): {ds_stavka}\n"
                      "🔹 Yagona soliq (YaS): {ys_stavka}\n"
                      "🔹 QQS (Qo‘shilgan qiymat soligi): {qqs_stavka}",
        'daromad_report': "📋 {firma_name} uchun {oy} hisoboti\n\n"
                          "👥 Xodimlar soni: {xodimlar_soni}\n"
                          "📋 Xodimlar:\n{xodimlar_data}\n\n"
                          "📅 Hisobot davri (oylik): {hisobot_davri_oylik} so‘m\n"
                          "💸 Jami oylik: {jami_oylik} so‘m\n"
                          "📊 Soliq: {soliq} so‘m",
        'yagona_report': (
            "📋 *YAGONA SOLIQ HISOBOTI – {oy} OYI*\n\n"
            "💼 *Firma nomi*: {firma_nomi}\n"
            "👤 *Raxbar*: {rahbar}\n"
            "📅 *Hisobot davri*: 2025-yil {oy}\n"
            "📌 *Hisobot turi*: Aylanma tushumdan hisoblangan yagona soliq\n\n"
            "🔁 *Aylanma tushum (yil boshidan olingan jami aylanma)*: {yil_boshidan_aylanma} so‘m\n\n"
            "🔁 *Aylanma tushum (oy davomida olingan jami aylanma)*: {shu_oy_aylanma} so‘m\n\n"
            "📊 *Qo‘llanilgan soliq stavkasi*: {soliq_turi_yagona} (amaldagi qonunchilikka asosan)\n\n"
            "📉 *Hisob-kitob formulasi Oy uchun*:\n"
            "Yagona soliq = Aylanma tushum × Soliq stavkasi\n"
            "📐 {shu_oy_aylanma} × {soliq_turi_yagona} = {yagona_soliq} so‘m\n\n"
            "💸 *Yakuniy natija – To‘lanishi lozim bo‘lgan yagona soliq miqdori*: ➡️ {yagona_soliq} so‘m\n\n"
            "📎 *Eslatma*:\n"
            "Ushbu hisob-kitob O‘zbekiston Respublikasining amaldagi soliq kodeksi asosida amalga oshirilgan bo‘lib, "
            "faqatgina yagona soliq to‘lovchilar (masalan, kichik tadbirkorlik subyektlari) uchun mo‘ljallangan.\n"
            "🕒 Hisobot topshirish muddati tugashidan oldin Davlat soliq xizmati organlariga taqdim etilishi zarur."
        ),
        'qqs_report': (
            "📋 *QQS HISOBOTI – {oy} OYI*\n\n"
            "💼 *Firma nomi*: {firma_nomi}\n"
            "👤 *Raxbar*: {rahbar}\n"
            "📅 *Hisobot davri*: 2025-yil {oy}\n"
            "📌 *Hisobot turi*: Qo‘shilgan qiymat solig‘i (QQS)\n\n"
            "🔁 *Savdo tushum (yil davomida amalga oshirilgan savdo hajmi)*: {yil_boshidan_qqs} so‘m\n\n"
            "🔁 *Savdo tushum (oy davomida amalga oshirilgan savdo hajmi)*: {shu_oy_qqs} so‘m\n\n"
            "📊 *QQS stavkasi (amaldagi stavka)*: {soliq_turi_qqs}\n\n"
            "📉 *Hisob-kitob formulasi*:\n"
            "QQS = Aylanma tushum × QQS stavkasi\n"
            "📐 {shu_oy_qqs} × {soliq_turi_qqs} = {qqs_soliq} so‘m\n\n"
            "💸 *Yakuniy natija – QQS to‘lov summasi*: ➡️ {qqs_soliq} so‘m\n\n"
            "📎 *Eslatma*:\n"
            "Qo‘shilgan qiymat solig‘i (QQS) to‘lovchilari umumiy aylanma tushumga qarab hisob-kitob qilishlari lozim. "
            "QQSni to‘lash va hisobotni topshirish belgilangan muddatda amalga oshirilmasa, jarimalar qo‘llaniladi.\n"
            "🧾 Ushbu ma’lumot Soliq Kodeksi (2024-yilgi tahriri) asosida shakllantirilgan."
        )
    },
    'uz_cyrillic': {
        'select_language': "Илтимос, тилни танланг:",
        'language_set': "Тил муваффақиятли ўзгартирилди!",
        'welcome': "Ботга хуш келибсиз! Фирма СТИР рақамини киритинг (9 рақам, масалан: 123456789):",
        'enter_cyrillic_text': "Кирилл алифбосидаги матнни киритинг:",
        'enter_latin_text': "Лотин алифбосидаги матнни киритинг:",
        'translated_text': "Таржима қилинган матн: {text}",
        'invalid_stir': "❌ Бу СТИР бўйича фирма топилмади.",
        'select_tax_type': "📊 СТИР: {stir}\nСолиқ турини танланг:",
        'select_month': "📅 {soliq_turi} учун ойни танланг:",
        'file_not_found': "❌ {oy} учун файл топилмади.",
        'file_error': "❌ Файлни юклашда хато юз берди: {error}",
        'yagona_file_not_found': "❌ {oy} учун ягона солиқ файли топилмади.",
        'yagona_error': "❌ Ягона солиқ ҳисоботида хато: {error}",
        'qqs_file_not_found': "❌ {oy} учун ҚҚС файли топилмади.",
        'qqs_error': "❌ ҚҚС ҳисоботида хато: {error}",
        'no_manual_report': "❌ {oy} учун қўлда киритилган ҳисобот топилмади.",
        'back_options': "Қуйидаги вариантлардан бирини танланг:",
        'excel1_not_found': "📋 1-Excel файлни ҳисоботларни яратиб қўйинг илтимос, сўнг 2-Excel файлни юкланг (.xlsx):",
        'excel1_uploaded': "✅ 1-Excel файл юкланган, энди 2-Excel файлни юкланг (.xlsx):",
        'firma_info': "📋 Фирма ҳақида маълумот\n\n"
                      "🏢 СТИР: {stir}\n"
                      "🏢 Фирма номи: {firma_nomi}\n"
                      "👤 Раҳбар: {rahbar}\n"
                      "📊 Солиқ тури: {soliq_turi}\n\n"
                      "📌 Солиқ ставкалари:\n"
                      "🔹 Даромад солиғи (ДС): {ds_stavka}\n"
                      "🔹 Ягона солиқ (ЯС): {ys_stavka}\n"
                      "🔹 ҚҚС (Қўшилган қиймат солиғи): {qqs_stavka}",
        'daromad_report': "📋 {firma_name} учун {oy} ҳисоботи\n\n"
                          "👥 Ходимлар сони: {xodimlar_soni}\n"
                          "📋 Ходимлар:\n{xodimlar_data}\n\n"
                          "📅 Ҳисобот даври (ойлик): {hisobot_davri_oylik} сўм\n"
                          "💸 Жами ойлик: {jami_oylik} сўм\n"
                          "📊 Солиқ: {soliq} сўм",
        'yagona_report': (
            "📋 *ЯГОНА СОЛИҚ ҲИСОБОТИ – {oy} ОЙИ*\n\n"
            "💼 *Фирма номи*: {firma_nomi}\n"
            "👤 *Раҳбар*: {rahbar}\n"
            "📅 *Ҳисобот даври*: 2025-йил {oy}\n"
            "📌 *Ҳисобот тури*: Айланма тушумдан ҳисобланган ягона солиқ\n\n"
            "🔁 *Айланма тушум (йил бошидан олинган жами айланма)*: {yil_boshidan_aylanma} сўм\n\n"
            "🔁 *Айланма тушум (ой давомида олинган жами айланма)*: {shu_oy_aylanma} сўм\n\n"
            "📊 *Қўлланилган солiq ставкаси*: {soliq_turi_yagona} (амалдаги қонунчиликка асосан)\n\n"
            "📉 *Ҳисоб-китоб формуласи Ой учун*:\n"
            "Ягона солiq = Айланма тушум × Солиқ ставкаси\n"
            "📐 {shu_oy_aylanma} × {soliq_turi_yagona} = {yagona_soliq} сўм\n\n"
            "💸 *Якуний натижа – Тўланиши лозим бўлган ягона солiq миқдори*: ➡️ {yagona_soliq} сўм\n\n"
            "📎 *Эслатма*:\n"
            "Ушбу ҳисоб-китоб Ўзбекистон Республикасининг амалдаги солiq кодекси асосида амалга оширилган бўлиб, "
            "фақатгина ягона солiq тўловчилар (масалан, кичик тадбиркорлик субъектлари) учун мўлжалланган.\n"
            "🕒 Ҳисобот топшириш муддати тугашидан олдин Давлат солiq хизмати органларига тақдим этилиши зарур."
        ),
        'qqs_report': (
            "📋 *ҚҚС ҲИСОБОТИ – {oy} ОЙИ*\n\n"
            "💼 *Фирма номи*: {firma_nomi}\n"
            "👤 *Раҳбар*: {rahbar}\n"
            "📅 *Ҳисобот даври*: 2025-йил {oy}\n"
            "📌 *Ҳисобот тури*: Қўшилган қиймат солиғи (ҚҚС)\n\n"
            "🔁 *Савдо тушум (йил давомида амалга оширилган савдо ҳажми)*: {yil_boshidan_qqs} сўм\n\n"
            "🔁 *Савдо тушум (ой давомида амалга оширилган савдо ҳажми)*: {shu_oy_qqs} сўм\n\n"
            "📊 *ҚҚС ставкаси (амалдаги ставка)*: {soliq_turi_qqs}\n\n"
            "📉 *Ҳисоб-китоб формуласи*:\n"
            "ҚҚС = Айланма тушум × ҚҚС ставкаси\n"
            "📐 {shu_oy_qqs} × {soliq_turi_qqs} = {qqs_soliq} сўм\n\n"
            "💸 *Якуний натижа – ҚҚС тўлов суммаси*: ➡️ {qqs_soliq} сўм\n\n"
            "📎 *Эслатма*:\n"
            "Қўшилган қиймат солиғи (ҚҚС) тўловчилари умумий айланма тушумга қараб ҳисоб-китоб қилишлари лозим. "
            "ҚҚСни тўлаш ва ҳисоботни топшириш белгиланган муддатда амалга оширилмаса, жарималар қўлланилади.\n"
            "🧾 Ушбу ма’лумот Солиқ Кодекси (2024-йилги таҳрири) асосида шакллантирилган."
        )
    }
}

def get_text(lang, key, **kwargs):
    text = LANGUAGES.get(lang, LANGUAGES['uz_latin']).get(key, "Matn topilmadi")
    return text.format(**kwargs) if kwargs else text

def get_month_name(lang, oy):
    months = {
        'uz_latin': {
            'yanvar': 'Yanvar', 'fevral': 'Fevral', 'mart': 'Mart',
            'aprel': 'Aprel', 'may': 'May', 'iyun': 'Iyun', 'iyul': 'Iyul'
        },
        'uz_cyrillic': {
            'yanvar': 'Январ', 'fevral': 'Феврал', 'mart': 'Март',
            'aprel': 'Апрел', 'may': 'Май', 'iyun': 'Июн', 'iyul': 'Июл'
        }
    }
    return months.get(lang, months['uz_latin']).get(oy, oy)

def translate_text(text, lang):
    if lang == 'uz_cyrillic':
        return convert_to_cyrillic(text)
    elif lang == 'uz_latin':
        return convert_to_latin(text)
    return text