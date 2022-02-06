from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from jsonrpcclient.requests import request_uuid
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from datetime import datetime

import httpx

from app.jwt import create_token
from app.jwt import valid_email_from_db
from app.jwt import get_current_user_email
from app.jwt import create_refresh_token
from app.jwt import decode_token
from app.jwt import CREDENTIALS_EXCEPTION
from app.jwt import add_user_to_db
from app.utils import *

# Webserver definition

tags_metadata = [
    {
        "name": "auth",
        "description": "Operations for securing the whole API and managing user authentication",
    },
    {"name": "news_fetcher", "description": "Operations for retrieving RSS news"},
    {
        "name": "ml_processing",
        "description": "Operations for obtaining news textual summary exploiting Natural Language Processing",
    },
    {"name": "dummy", "description": "Just for testing"},
]

app = FastAPI(openapi_tags=tags_metadata)
app.add_middleware(SessionMiddleware, secret_key="!secret")

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = Config(".env")
oauth = OAuth(config)

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)


@app.get("/api")
async def index():
    return {"message": "Hello World!"}


# AUTH


@app.get("/api/login", tags=["auth"])
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/api/auth", tags=["auth"])
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise CREDENTIALS_EXCEPTION
    user_data = await oauth.google.parse_id_token(request, access_token)
    # TODO: Check if user is already in the REAL DB
    if valid_email_from_db(user_data["email"]):
        return JSONResponse(
            {
                "result": True,
                "access_token": create_token(user_data["email"]),
                "refresh_token": create_refresh_token(user_data["email"]),
            }
        )
    else:
        user_data["access_token"] = create_token(user_data["email"])
        user_data["refresh_token"] = create_refresh_token(user_data["email"])
        await add_user_to_db(user_data)
        return JSONResponse(user_data)


@app.get("/api/logout", tags=["auth"])
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")


@app.post("/api/refresh", tags=["auth"])
async def refresh(request: Request):
    try:
        # Only accept post requests
        if request.method == "POST":
            form = await request.json()
            if form.get("grant_type") == "refresh_token":
                token = form.get("refresh_token")
                payload = decode_token(token)
                # Check if token is not expired
                if datetime.utcfromtimestamp(payload.get("exp")) > datetime.utcnow():
                    email = payload.get("sub")
                    # Validate email
                    if valid_email_from_db(email):
                        # Create and return token
                        return JSONResponse(
                            {"result": True, "access_token": create_token(email)}
                        )

    except Exception:
        raise CREDENTIALS_EXCEPTION
    raise CREDENTIALS_EXCEPTION


# NEWS FETCHER


@app.get("/api/getnews", tags=["news_fetcher"])
async def call_fetcher():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_fetcher,
                json=request_uuid("retrive_information"),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )


# ML PROCESSING


@app.get("/api/summary", tags=["ml_processing"])
async def summary(current_email: str = Depends(get_current_user_email)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_analysis,
                json=request_uuid(
                    "summarize",
                    params=[
                        "Harry Potter is a series of seven fantasy novels written by British author J. K. Rowling."
                    ],
                ),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )


# DUMMY


@app.get("/api/dummy/login", tags=["dummy"])
async def dummy_login():
    return JSONResponse(
        {
            "result": "true",
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJscmF6b3ZpY0BnbWFpbC5jb20iLCJleHAiOjE2NDM0MDc5NDd9._h426jMZXWJ5zwclxtkg4A8xe7-GxJB-XgGa55EYfBQ",
            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJscmF6b3ZpY0BnbWFpbC5jb20iLCJleHAiOjE2NDU5OTkwNDd9.iZjQTbf004zjqTqxEkGWbDSncdmAyj3-K39uVuFfENs",
        }
    )


@app.get("/api/dummy/getnews", tags=["dummy"])
async def dummy_call_fetcher():
    res = {
        "jsonrpc": "2.0",
        "result": {
            "Blog title": "Repubblica.it > Homepage",
            "Blog link": "https://www.repubblica.it",
            "posts": [
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
                },
            ],
        },
        "id": 1,
    }

    return res


@app.get("/api/dummy/summary", tags=["dummy"])
async def dummy_summary():
    res = {
        "id": "c8b822b3-a40c-4472-aabf-2555f0ef073a",
        "jsonrpc": "2.0",
        "result": "Harry Potter is a series of seven fantasy novels written by British author J. K. Rowling. Since the release of the first novel, Harry Potter and the Philosopher's Stone, on 26 June 1997, the books have found immense popularity, positive reviews, and commercial success worldwide. They have attracted a wide adult audience as well as younger readers and are often considered cornerstones of modern young adult literature.",
    }

    return res


@app.post("/api/postUser", tags=["dummy"])
async def postUser():
    try:
        data = {
            "iss": "https://accounts.google.com",
            "azp": "32814020986-9u0gu68a62jh6o7i7drv5ltrpuf18emv.apps.googleusercontent.com",
            "aud": "32814020986-9u0gu68a62jh6o7i7drv5ltrpuf18emv.apps.googleusercontent.com",
            "sub": "100453178713727110711",
            "email": "lrazovic@gmail.com",
            "email_verified": "true",
            "at_hash": "ZAlXWOwZQ0a7NdC09HOn8g",
            "nonce": "H8CHfv8hV6RJy40F9r4P",
            "name": "Leonardo Razovic",
            "picture": "https://lh3.googleusercontent.com/a/AATXAJz6ZNHbViGfyqwaRiy-A3ikxAvc3njHFiPK9LQI=s96-c",
            "given_name": "Leonardo",
            "family_name": "Razovic",
            "locale": "en-GB",
            "iat": "1644142365",
            "exp": "1644145965",
        }
        data["access_token"] = create_token(data["email"])
        data["refresh_token"] = create_refresh_token(data["email"])
        await add_user_to_db(data)
        return JSONResponse(data)
    except Exception as e:
        print(e)
        return {"status": "error"}


############################################################################################################################################################
