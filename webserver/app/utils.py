import os

if "DEV" in os.environ:
    endpoint_fetcher = "http://localhost:5002"
    endpoint_newspaper = "http://localhost:5004"
    endpoint_analysis = "http://localhost:5001"
    endpoint_persistence = "http://localhost:5003"
    enpdoint_token = "http://localhost"
    redirect_uri = "http://localhost:8080/token"
else:
    endpoint_fetcher = "http://fetcher:5002"
    endpoint_newspaper = "http://newspaper:5004"
    endpoint_analysis = "http://analysis:5001"
    endpoint_persistence = "http://persistence:5003"
    enpdoint_token = "172.17.0.1"
    redirect_uri = "http://webserver:3000/token"

redirect_uri = os.environ.get("redirect_uri") or "http://localhost:8080/token"

tags_metadata = [
    {
        "name": "news",
        "description": "Operations for managing news from RSS feeds"
    },
    {
        "name": "users",
        "description": "Operations for managing users of the system"
    },
    {
        "name": "tbd",
        "description": "Redundant operations, probably to be deleted"
    }
]

# Helper to read numbers using var envs
def cast_to_number(id: str):
    temp = os.environ.get(id)
    if temp is not None:
        try:
            return float(temp)
        except ValueError:
            return None
    return None


long_post = [
    {
        "title": "Covid, l'Aifa approva la pillola Merck&Co. Da domani in Italia",
        "link": "https://www.repubblica.it/salute/2022/01/03/news/covid_l_aifa_approva_la_pillola_merck-332518046/?rss",
        "author": "repubblicawww@repubblica.it (Redazione Repubblica.it)",
        "time_published": "Mon, 03 Jan 2022 14:17:58 +0100",
        "tags": ["salute"],
        "authors": ["Redazione Repubblica.it"],
        "summary": '<p><a href="https://www.repubblica.it/salute/2022/01/03/news/covid_l_aifa_approva_la_pillola_merck-332518046/?rssimage"> <img align="left" hspace="10" src="https://www.repstatic.it/content/nazionale/img/2022/01/03/135203341-77263d12-c61c-4641-8f44-53ce10407107.jpg" width="140" /></a>Presto sarà distribuita alle Regioni: quando, cosa c\'è da sapere</p>',
    },
    {
        "title": "Sumatra colpita dalle inondazioni: le impressionanti immagini dal drone",
        "link": "https://video.repubblica.it/mondo/indonesia-sumatra-colpita-dalle-inondazioni-le-impressionanti-immagini-dal-drone/405072/405782/?rss",
        "author": "repubblicawww@repubblica.it (Redazione Repubblica.it)",
        "time_published": "Mon, 03 Jan 2022 14:36:13 +0100",
        "tags": ["null"],
        "authors": ["Redazione Repubblica.it"],
        "summary": "",
    },
    {
        "title": 'Smart working nella Pa, Brunetta stoppa i sindacati: "Non si torna al lavoro da casa"',
        "link": "https://www.repubblica.it/economia/2022/01/03/news/smart_working_pa_la_replica_della_funzione_pubblica_ai_sindacati_gia_ora_possibile_grande_flessibilita_fino_al_49_-332518199/?rss",
        "author": "repubblicawww@repubblica.it (Redazione Repubblica.it)",
        "time_published": "Mon, 03 Jan 2022 14:17:45 +0100",
        "tags": ["economia"],
        "authors": ["Redazione Repubblica.it"],
        "summary": '<p><a href="https://www.repubblica.it/economia/2022/01/03/news/smart_working_pa_la_replica_della_funzione_pubblica_ai_sindacati_gia_ora_possibile_grande_flessibilita_fino_al_49_-332518199/?rssimage"> <img align="left" hspace="10" src="https://www.repstatic.it/content/nazionale/img/2022/01/03/143528940-fd7596e4-74b0-449f-8338-eb4f4d88ae34.jpg" width="140" /></a>Il dipartimento Funzione pubblica replica alle lettere delle sigle, che con l\'emergenza contagi chiedono di ripristinare l\'attività a distanza per tutti i dipendenti: "Il massimo livello di apertura è compatibile con il massimo livello di sicurezza, il lavoro agile è già...</p>',
    },
    {
        "title": "Sulla Msc Grandiosa focolaio Covid con 120 positivi, scattano le misure di prevenzione",
        "link": "https://genova.repubblica.it/cronaca/2022/01/03/news/sulla_msc_grandiosa_focolaio_covid_con_120_positivi_scattano_le_misure_di_prevenzione-332511642/?rss",
        "author": "repubblicawww@repubblica.it (Redazione Repubblica.it)",
        "time_published": "Mon, 03 Jan 2022 13:10:03 +0100",
        "tags": ["cronaca"],
        "authors": ["Redazione Repubblica.it"],
        "summary": '<p><a href="https://genova.repubblica.it/cronaca/2022/01/03/news/sulla_msc_grandiosa_focolaio_covid_con_120_positivi_scattano_le_misure_di_prevenzione-332511642/?rssimage"> <img align="left" hspace="10" src="https://www.repstatic.it/content/nazionale/img/2022/01/03/121901039-fb7dc8f3-77eb-4620-9f76-b76fa26b409a.jpg" width="140" /></a>La nave arrivata stamani al porto di Genova sta sbarcando i contagiati che saranno accompagnati in sicurezza nelle rispettive abitazioni</p>',
    },
    {
        "title": "La corsa di Omicron, contagi in crescita di oltre due volte e mezzo: in una settimana +163%",
        "link": "https://www.repubblica.it/cronaca/2022/01/03/news/i_dati_settimanali_omicron_fa_crescere_aumentare_i_contagi_di_oltre_due_volte_e_mezzo_163_-332467883/?rss",
        "author": "repubblicawww@repubblica.it (Redazione Repubblica.it)",
        "time_published": "Mon, 03 Jan 2022 10:39:11 +0100",
        "tags": ["cronaca"],
        "authors": ["Redazione Repubblica.it"],
        "summary": '<p><a href="https://www.repubblica.it/cronaca/2022/01/03/news/i_dati_settimanali_omicron_fa_crescere_aumentare_i_contagi_di_oltre_due_volte_e_mezzo_163_-332467883/?rssimage"> <img align="left" hspace="10" src="https://www.repstatic.it/content/nazionale/img/2022/01/03/090652948-f20d8e0f-8d2a-48d3-884e-6c141e6ea211.jpg" width="140" /></a>In Toscana, Abruzzo e Molise casi più che quadruplicati. Oltre un quarto dei ricoveri in più, tre Regioni e una Provincia rischiano di finire in arancione. Molto contenuto l\'aumento delle morti</p>',
    },
    {
        "title": 'Covid, De Luca: "Meglio rinviare la riapertura delle scuole"',
        "link": "https://napoli.repubblica.it/cronaca/2022/01/03/news/campania_scuola_covid_de_luca-332510628/?rss",
        "author": "repubblicawww@repubblica.it (Redazione Repubblica.it)",
        "time_published": "Mon, 03 Jan 2022 12:33:33 +0100",
        "tags": ["cronaca"],
        "authors": ["Redazione Repubblica.it"],
        "summary": '<p><a href="https://napoli.repubblica.it/cronaca/2022/01/03/news/campania_scuola_covid_de_luca-332510628/?rssimage"> <img align="left" hspace="10" src="https://www.repstatic.it/content/nazionale/img/2022/01/03/115714011-96f257e4-98d2-4465-90df-8c6653437f59.jpg" width="140" /></a>"Nel quadro attuale di diffusione del contagio fra i giovanissimi, mi parrebbe una misura equilibrata prendere 20/30 giorni di respiro..."</p>',
    },
    {
        "title": 'Da lunedì "confinato" nelle isole chi non è vaccinato, la protesta dei sindaci',
        "link": "https://firenze.repubblica.it/cronaca/2022/01/03/news/da_lunedi_confinato_nelle_isole_chi_non_e_vaccinato_la_proteta_dei_sindaci-332516808/?rss",
        "author": "repubblicawww@repubblica.it (Redazione Repubblica.it)",
        "time_published": "Mon, 03 Jan 2022 13:03:07 +0100",
        "tags": ["cronaca"],
        "authors": ["Redazione Repubblica.it"],
        "summary": '<p><a href="https://firenze.repubblica.it/cronaca/2022/01/03/news/da_lunedi_confinato_nelle_isole_chi_non_e_vaccinato_la_proteta_dei_sindaci-332516808/?rssimage"> <img align="left" hspace="10" src="https://www.repstatic.it/content/nazionale/img/2022/01/03/134938627-6ffb7245-67a4-4d6b-8bfd-135b1b171a80.jpg" width="140" /></a>"Chiediamo deroghe al Governo per il decreto legge che impone l\'obbligo di Super Green Pass per i trasporti, così si creano cittadini di Serie A e Serie B, a questo punto era meglio introdurre l\'obbligo vaccinale" dice Sergio Ortelli, sindaco del Giglio, vice presidente...</p>',
    },
    {
        "title": "Previsioni meteo, con la Befana torna l'inverno: in arrivo freddo e neve",
        "link": "https://www.repubblica.it/cronaca/2022/01/03/news/previsioni_meteo_befana_svolta_invernale_tornano_freddo_e_neve-332500097/?rss",
        "author": "repubblicawww@repubblica.it (Redazione Repubblica.it)",
        "time_published": "Mon, 03 Jan 2022 11:35:03 +0100",
        "tags": ["cronaca"],
        "authors": ["Redazione Repubblica.it"],
        "summary": '<p><a href="https://www.repubblica.it/cronaca/2022/01/03/news/previsioni_meteo_befana_svolta_invernale_tornano_freddo_e_neve-332500097/?rssimage"> <img align="left" hspace="10" src="https://www.repstatic.it/content/nazionale/img/2022/01/03/101322931-f0e57602-60ae-4504-8861-547a033c77d8.jpg" width="140" /></a>Fino a martedì 4 tempo ancora dominato dall\'Anticiclone. Poi dall\'Epifania il clima si raffredderà su tutte le regioni, la nebbia sarà un ricordo e torneranno le gelate notturne, anche intense, non solo al Nord ma anche su alcune città del Centro</p>',
    },
    {
        "title": "Stanotte col naso all'insu per le prime 'stelle cadenti' del 2022",
        "link": "https://www.repubblica.it/green-and-blue/2022/01/03/news/stanotte_col_naso_all_insu_per_le_prime_stelle_cadenti_del_2022-332519673/?rss",
        "author": "repubblicawww@repubblica.it (Redazione Repubblica.it)",
        "time_published": "Mon, 03 Jan 2022 14:26:35 +0100",
        "tags": ["green-and-blue"],
        "authors": ["Redazione Repubblica.it"],
        "summary": '<p><a href="https://www.repubblica.it/green-and-blue/2022/01/03/news/stanotte_col_naso_all_insu_per_le_prime_stelle_cadenti_del_2022-332519673/?rssimage"> <img align="left" hspace="10" src="https://www.repstatic.it/content/nazionale/img/2022/01/03/140314938-da1eb9f6-0b30-4eb7-907b-066bb70d4ad6.jpg" width="140" /></a>Da mezzanotte in poi è visibile lo sciame meteorico delle Quadrantidi, uno dei più importanti dell\'anno. Ecco come sarà il cielo di gennaio</p>',
    },
    {
        "title": "Sono 78 e tutti uomini: la guerra delle statue che infiamma Padova",
        "link": "https://www.repubblica.it/cronaca/2022/01/02/news/sono_78_e_tutti_uomini_la_guerra_delle_statue_che_infiamma_padova-332468530/?rss",
        "author": "repubblicawww@repubblica.it (Redazione Repubblica.it)",
        "time_published": "Sun, 02 Jan 2022 22:52:39 +0100",
        "tags": ["cronaca"],
        "authors": ["Redazione Repubblica.it"],
        "summary": '<p><a href="https://www.repubblica.it/cronaca/2022/01/02/news/sono_78_e_tutti_uomini_la_guerra_delle_statue_che_infiamma_padova-332468530/?rssimage"> <img align="left" hspace="10" src="https://www.repstatic.it/content/nazionale/img/2022/01/03/011833175-4645fd4b-1efd-4b67-9112-17d381640e34.jpg" width="140" /></a>La proposta in consiglio: “Onoriamo anche una donna in Prato della Valle”. Sì della Sovrintendenza. Lo storico si oppone: “Sono monumenti, non Lego”</p>',
    }
]

#XXX WIP
# def rssFeedDtoToDict(dto: RssFeedDto):
#     dct = dict()

#     dct["url"] = dto.url
#     dct["rank"] = dto.rank
#     dct["user_id"] = dto.user_id

#     return dct
