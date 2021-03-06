import threading
import discord
from discord import client
from discord.ext import commands
import random
from discord import Embed
from discord import FFmpegPCMAudio
import asyncio
import translate
from translate import Translator
from googleapiclient.discovery import build
from google.oauth2 import service_account
import gspread
import timeit
from threading import Thread, Timer
import time

#holds API keys for the google service accounts
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']

#Initializing the Spreadsheet
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = gspread.authorize(creds)

maptest = client.open("Map Game VI Database").worksheet("Territories")

SAMPLE_SPREADSHEET_ID = '1EodY2Cs1t1UfarRwF80pIcLLGsD2OfdiyIImRD02g8g'

TRIVIA_ID = '1IjU6hFOiexP4ZFYUuawvCqSc8b6uyu7cS4S5Rz6KLsA'

service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()

streaks = client.open("Trivia Streaks").worksheet("Streaks")

france = ["French", "France", "french", "france"]

andrew= ["schlafly", "Schlafly"]

random_fact_list = ["France's longest continuous border is with Brazil.", "The political left is usually signalled with red, but in the U.S. the parties got it flipped. https://tenor.com/view/ugh-donald-trump-head-shake-eye-roll-unbelievable-gif-14330090", "India and Bangladesh used to have an enclave within an enclave within an enclave. It has since been resolved.", "The 2021 Peruvian Presidential election second round involved both a communist and the daughter of the deposed dictator of the country.", "SCUBA and RADAR were originally acronyms."]

dares = ['Text the 3rd person in your phone "I know what you did".', "Blast Locationships - Cordae for 5 seconds.", "Instead of swearing, use derivatives of 'pog' for the next 24 hours.", "Confess to the 7th person on your dms of your most recent lie.", "Reccomend Mickey Mouse Clubhouse to the 2nd person on ur dms list.", "Make a rap about the most recent political argument on the server and send it here.", "End all of your messages with an emoji for the next 5 minutes.", "Blast Mining Away for 15 seconds out loud.", "Don't listen to Machine Gun Kelly or any form of his songs or any features for a week."]

truths = ['placeholder truth']

mgk = ["mgk", "Mgk", "Machine Gun Kelly", "Machine gun kelly", "machine gun kelly"]

ooc = ['https://cdn.discordapp.com/attachments/783881442622308382/870707941932671086/image0.jpg',
        'https://cdn.discordapp.com/attachments/850408868919509004/860955116752470026/image0.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/857340084088733706/unknown.png',
        'https://cdn.discordapp.com/attachments/800039486339678250/870709835723853975/unknown.png',
        'https://cdn.discordapp.com/attachments/800039486339678250/870710600429363261/unknown.png',
        'https://cdn.discordapp.com/attachments/800039486339678250/870710970887057408/unknown.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/869385234460848169/image0.png',
        'https://cdn.discordapp.com/attachments/800039486339678250/870711752910852127/unknown.png',
        'https://cdn.discordapp.com/attachments/795023687501611018/870715907612225557/IMG_3493.jpg',
        'https://cdn.discordapp.com/attachments/870073339224420393/870718276542541864/Liam_likes_very_special_things_there_I_guess.png',
        'https://cdn.discordapp.com/attachments/870073339224420393/870718173249425448/image0.png',
        'https://cdn.discordapp.com/attachments/870073339224420393/870718632735416370/LIAMWHATAREYOUHIDING.png',
        'https://cdn.discordapp.com/attachments/870073339224420393/870718627140206602/image0.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/870719250275401768/Liamconfessed.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/870720464434131005/ZEKEHASBEENLIKED.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/870721555607453707/unknown.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/870722287815516250/image0.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/870723769604378634/image0.png',
        'https://cdn.discordapp.com/attachments/795023687501611018/871863915267620884/unknown.png',
        'https://cdn.discordapp.com/attachments/795023687501611018/871866601627066408/unknown.png',
        'https://cdn.discordapp.com/attachments/862025232336289810/869263494388793404/image0.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/875148978864402463/unknown.png',
        'https://cdn.discordapp.com/attachments/850408868919509004/875372858992382062/unknown.png'
        ]

oocname = ["Do you have an explanation for this one...", "Oh no...", "Caught in 4K."]

ooctext = ["When you try your best but you don't succeed...", "Work smarter not harder buckaroo.", "Better luck next time..."]

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s":1, "m":60, "h":3600, "d":3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

nerd1_score_list = []
nerd2_score_list = []

class Fun(commands.Cog, description='These commands are random commands used for purely fun purposes.'):

    """These commands are purely for fun."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['trans'])
    async def translate(self, ctx, *, sentence):
        translator = Translator(to_lang="es")
        translation = translator.translate(sentence)
        await ctx.send(translation.capitalize())
    
    @commands.command(aliases=['transenglish'])
    async def translateenglish(self, ctx, * sentence):
        translator = Translator(to_lang="en", from_lang="es")
        translation = translator.translate(sentence)
        await ctx.send(translation.capitalize())
    
    @commands.command(aliases=['rand'], description = "Current randomizers are US states, countries, empires in the Map Game, territories in the Map Game, Wars, Number, US Senators and US Representatives.")
    async def random(self, ctx, *, randomized_item:str):

        if randomized_item.lower() == 'state' or randomized_item.lower() == 'states':
            states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
            choice = random.choice(states)
            await ctx.send(choice)
        
        if randomized_item.lower() == 'country' or randomized_item.lower() == 'nation':
            countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Republic of the Congo', 'Democratic Republic of the Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'North Korea', 'South Korea', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar (Burma)', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russian Federation', 'Rwanda', 'St Kitts & Nevis', 'St Lucia', 'Saint Vincent & the Grenadines', 'Samoa', 'San Marino', 'Sao Tome & Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad & Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
            choice = random.choice(countries)
            await ctx.send(choice)

        if randomized_item.lower() == 'territory':
            territories = []
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Territories!A1:Q1400").execute()
            values = result.get('values')

            for owner_pair in values:
                territories.append(owner_pair[1])

            choice = random.choice(territories)
            await ctx.send(choice)
        
        if randomized_item.lower() == 'number':
            number = random.randint(1,10)
            await ctx.send(str(number))
        
        if randomized_item.lower() == 'empire':
            empire_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="General Stats!A1:Q150").execute()
            empire_values = empire_result.get('values')

            empires = []

            for owner_pair in empire_values:
                empires.append(owner_pair[1])

            choice = random.choice(empires)
            await ctx.send(choice)

        #I dare anyone to try to find the Thirty Years War without Ctrl F
        if randomized_item.lower() == 'war':
            wars =['(you are very unlucky to roll this) Never gonna give you up...', 'War in Darfur','Iraq War','Sinaloa Cartel-Gulf Cartel conflict','War in North-West Pakistan','Central African Republic Bush War','Iran???PJAK conflict Kurdish separatism in Iran','Conflict in the Niger Delta','Houthi insurgency in Yemen','Kivu conflict','Sistan and Baluchestan insurgency Part of the Balochistan conflict','Paraguayan People s Army insurgency','Chadian Civil War (2005???10)','2005 Bangladesh India border clash','Mount Elgon insurgency','Fatah???Hamas conflict','Bakassi conflict','2006 Lebanon War','Operation Astute','Eelam War IV','Iraqi Civil War Part of the Iraq War','Mexican Drug War','War in Somalia (2006???09) Part of the Somali Civil War','Operation Enduring Freedom ??? Trans Sahara','Hamas  takeover of Gaza','2007 Lebanon conflict','Tuareg rebellion (2007???09)part of the Tuareg rebellion','War in Ingushetia','2008 invasion of Anjouan','2008 conflict in Lebanon','2008 Bangladesh India border clash','2008 Kufra conflict','Cambodian???Thai border dispute','Djiboutian???Eritrean border conflict','Russo-Georgian War','Gaza War','Sudanese nomadic conflicts','Insurgency in the North Caucasus','Boko Haram insurgency','2009 Peruvian political crisis','2009 Boko Haram uprising Boko Haram insurgency','South Yemen insurgency','Somali Civil War (2009???present)Part of the Somali Civil War','Operation Scorched Earth Part of the Houthi insurgency in Yemen','Dongo conflict','2010 South Kyrgyzstan ethnic clashes','2010 Kingston unrest','Tajikistan insurgency','2010???2011 Ivorian crisis Second Ivorian Civil War','Libyan Civil War (2011)','Sinai insurgency','Syrian Civil War','Sudanese conflict in South Kordofan and Blue Nile','Shia insurgency in Bahrain','Syrian Civil War spillover in Lebanon Part of the Syrian Civil War','Ethnic violence in South Sudan (2011???present) Part of the Sudanese nomadic conflicts','Operation Linda Nchi Part of the Somali Civil War (2009???present)','Factional violence in Libya (2011???14)','Iraqi insurgency (2011???2013)Part of the Iraq War','Northern Mali conflict','Heglig Crisis','2012 Abyan offensivePart of the Al-Qaeda insurgency in Yemen','M23 rebellion','Baragoi clashes','Central African Republic conflict (2012???present)','South Sudanese Civil War Part of the ethnic violence in South Sudan (2011???present)','Lahad Datu standoff','Batwa???Luba clashes','Zamboanga City crisis','RENAMO insurgency (2013???2019)','Houthi takeover in YemenPart of the Houthi insurgency in Yemen and the Yemeni Crisis','2014 Israel???Gaza conflict Part of the Gaza???Israel conflict','2014 Aswan tribal clashes','Iraqi Civil War (2014???2017)','Second Libyan Civil War','Russo-Ukrainian War','International military intervention against ISIL','Yemeni Civil War (2015???present)','ISIL insurgency in Tunisia','Kurdish???Turkish conflict (2015???present)Part of the Kurdish???Turkish conflict (1978???present)','2016 Niger Delta conflictPart of the Conflict in the Niger Delta','2016 Armenian???Azerbaijani clashes','The Pool War','Northern Rakhine State clashesPart of the Rohingya insurgency in Western Myanmar and the Internal conflict in Myanmar','2016 Kasese clashes','Kamwina Nsapu rebellion','Insurgency in Northern Chad','2017 Afghanistan???Pakistan border skirmishPart of the Afghanistan???Pakistan skirmishes','2017???2020 Qatif unrestPart of the Qatif conflict','Marawi crisisPart of the Moro conflict and the Military intervention against ISIL','2017 Iraqi???Kurdish conflictPart of the Iraqi Civil War','Anglophone Crisis','Insurgency in Cabo Delgado','Iraqi insurgency (2017???present)','War in Catatumbo','Gaza???Israel clashes (November 2018)','2018 Armenian???Azerbaijani clashes','2019 India???Pakistan standoffPart of the 2019 India-Pakistan skirmishes','Gaza???Israel clashes (May 2019)','2019???20 Persian Gulf crisis','Metekel conflict','Gaza???Israel clashes (November 2019)','2020 China???India skirmishes','Western Togoland Rebellion','Second Nagorno-Karabakh war','Tigray War','2020???2021 Western Saharan clashes','Afar???Somali clashes','2020???21 Sudanese???Ethiopian clashes','Insurgency in Southeastern Nigeria','Kyrgyzstan???Tajikistan conflict','2021 Israel???Palestine crisis','2021 Armenia???Azerbaijan border crisis','Gulf War','1990???1998 Indonesian military operations in Aceh','DHKP/C insurgency in Turkey','Rwandan Civil War','Tuareg rebellion (1990???1995)','1990 Mindanao crisis','Operation Traira','Ten-Day War','1991???1992 South Ossetia War','Djiboutian Civil War','Croatian War of Independence','Sierra Leone Civil War','Algerian Civil War','Somali Civil War','Georgian Civil War','1991 uprisings in Iraq','Bosnian War','1992 Venezuelan coup d ??tat attempts','East Prigorodny Conflict','Civil war in Afghanistan (1992???1996)','War of Transnistria','War in Abkhazia (1992???1993)','Civil war in Tajikistan','Chechen Civil War [ru]','Burundian Civil War','Republic of the Congo Civil War (1993???1994)','Ethnic conflict in Nagaland','1993 Russian constitutional crisis','Iraqi Kurdish Civil War',' Armenian-Azerbaijani border conflict','Part of the Nagorno-Karabakh conflict ','Chiapas conflict',' 1994 Zapatista Uprising','Part of the Chiapas conflict ','1994 Bophuthatswana crisis','Yemeni Civil War (1994)','First Chechen War','Caprivi conflict','Cenepa War','Insurgency in Ogaden','Second Afar Insurgency','Hanish Islands conflict','ADF insurgency','Nepalese Civil War','Civil war in Afghanistan (1996???2001)','First Congo War','Albanian Rebellion of 1997','Republic of the Congo Civil War (1997???1999)','1997 clashes in Cambodia','1998 Monrovia clashes','War in Abkhazia (1998)','Kosovo War','Eritrean???Ethiopian War','Second Congo War','Guinea-Bissau Civil War','1998 Saudi-Yemeni border conflict[4][5][6]','Al-Qaeda insurgency in Yemen','Batken Conflict','Kargil WarPart of the Indo-Pakistani Wars','1999 East Timorese crisis','Insurgency in the Pre??evo Valley','Maluku sectarian conflict','Second Liberian Civil War','Ituri conflict','War of Dagestan','Second Chechen War',' Six-Day War (2000)','Part of the Second Congo War ','Second Intifada','2000???2006 Shebaa Farms conflict','2001 Bangladesh-India border clashes','Kurdistan Islamist conflict','Insurgency in the Republic of Macedonia','War on Terror','Perejil Island crisis','2002???2003 conflict in the Pool Department','Operation Enduring Freedom ??? Philippines','Operation Enduring Freedom ??? Horn of Africa','First Ivorian Civil War',' Taliban insurgency','Part of the War in Afghanistan (2001???present), War in Afghanistan (1978-present) and War on Terrorism ','Crusader insurgency','1945 Khuzestan revolt[1]','Chinese Civil War (Second Phase)','Indonesian National Revolution','War in Vietnam (1945???46)','Iran crisis of 1946','1945 Hazara Rebellion','Greek Civil War','Hukbalahap rebellion (post-WWII)','Autumn Uprising of 1946','Corfu Channel incident','Punnapra-Vayalar uprising','First Indochina War','Paraguayan Civil War (1947)','1947 Poonch Rebellion','Integration of Junagadh','Romanian anti-communist resistance movement','Indo-Pakistani War of 1947','Malagasy Uprising',' 1947???48 Civil War in Mandatory Palestine','Part of the 1948 Palestine war ','Safi Rebellion[2][3]','Costa Rican Civil War','Internal conflict in Burma','Inter-Korean border skirmishes','Al-Wathbah uprising','Jeju uprising','La Violencia',' 1948 Arab???Israeli War','Part of the Arab???Israeli conflict ','Malayan Emergency','Operation Polo',' Madiun Affair','Part of the Indonesian National Revolution ','Yeosu???Suncheon rebellion','Pre-Korean War insurgency[4]','1949 Hazara Rebellion',' Palestinian Fedayeen insurgency','Part of the Israeli???Palestinian conflict ','Palace Rebellion','Campaign to Suppress Bandits in Central and Southern China',' Darul Islam Insurgency','Part of the Indonesian National Revolution ','Afghanistan???Pakistan skirmishes','','Name of conflict','','Invasion of Hamasa and Buraimi','Kuomintang Islamic insurgency',' APRA coup d ??tat','Part of the Indonesian National Revolution ',' Makassar Uprising','Part of the Indonesian National Revolution ','La Revoluci??n del 50 [es]','Battle of Chamdo','Utuado Uprising','San Juan Nationalist revolt','Jayuya Uprising',' Korean War','Part of the Korean conflict ','Manhattan Rebellion','Reprisal operations','1952 Hazara Rebellion[8]','Egyptian revolution of 1952','Invasion of Hamasa','Mau Mau Uprising','Air battle over Merkl??n','Uprising in Plze?? (1953)','1953 East German Uprising','1953 Iranian coup d ??tat','Cuban Revolution','Xinjiang conflict','1954 Paraguayan coup d ??tat','Kengir uprising','First Taiwan Strait Crisis','Annexation of Dadra and Nagar Haveli','Second Taiwan Strait Crisis','Jebel Akhdar War','Algerian War','Preventive Strike of Marechal Lott [pt]','Afghan tribal revolt of 1955[9][2]','Calderonista Invasion of Costa Rica','Cyprus Emergency','Cameroonian Independence War','Upper Yafa uprisings[10]','First Sudanese Civil War','Vietnam War','Pozna?? Uprising','Hungarian Revolution of 1956','Suez Crisis','Qu???nh L??u Uprising','Ifni War','PRRI and Permesta rebellion','Anti-taxation uprising in Afghanistan[13]','1958 Lebanon crisis','14 July Revolution',' North Vietnamese invasion of Laos','Part of the Vietnam War and the Laotian Civil War ','Mexico???Guatemala conflict','1959 Mosul uprising','Spirit Soldier rebellion (1959)','1959 Tibetan uprising','Laotian Civil War','Escambray Rebellion','Pashtun Revolt in Kandahar[14]',' Upper Yafa disturbances[15]','(Further info: House of commons debate) ','Cuban invasion of Panama[16]','1959 Viqueque rebellion','Cuban invasion of the Dominican Republic[17]','Basque conflict','1960 Ethiopian coup attempt','Bajaur Campaign','1960???61 campaign at the China???Burma border','Congo Crisis','Katanga insurgency','Guatemalan Civil War','South Thailand insurgency','Nicaraguan Revolution','First Iraqi???Kurdish War','Bay of Pigs Invasion','Bizerte crisis',' French military rebellion in Algeria[18][19]','Part of the Algerian War ','Operation Trikora','Eritrean War of Independence','Indian annexation of Goa',' Angolan War of Independence','Part of the Portuguese Colonial War ','1961 revolt in Somalia','Rebellion of the Pilots','Tuareg rebellion (1962???64)','North Yemen Civil War','El Carupanazo','El Porte??azo','Sino-Indian War','Brunei revolt','Communist insurgency in Sarawak','Dhofar Rebellion','1963 Argentine Navy revolt','1963 Cuban invasion of Venezuela[20]','Sand War','Ramadan Revolution','Ar-Rashid revolt','November 1963 Iraqi coup d ??tat','1963 Syrian coup d ??tat','Indonesia???Malaysia confrontation','Shifta War','Bale revolt',' Guinea-Bissau War of Independence','Part of the Portuguese Colonial War ','Aden Emergency','1964 Brazilian coup d ??tat','1964 Ethiopian???Somali Border War',' Simba rebellion','Part of the Congo Crisis ','Rhodesian Bush War','FULRO insurgency against Vietnam','Colombian conflict (1964???present)',' Mozambican War of Independence','Part of the Portuguese Colonial War ','Insurgency in Northeast India','Zanzibar Revolution','30 September Movement','Dominican Civil War','American occupation of the Dominican Republic (1965???66)',' Indo-Pakistani War of 1965','Indo-Pakistani Wars ','Communist insurgency in Thailand','Chadian Civil War (1965???79)','Guerrilha do Capara?? [pt]','Crisis in French Somaliland[21]',' Stanleyville mutinies','Part of the Congo Crisis ','??ancahuaz?? Guerrilla War',' Korean DMZ Conflict','Part of the Korean conflict ','South African Border War','Invasion of Machurucuto','1967 China-India border conflicts','Six-Day War','1967 Kurdish revolt in Iran','Araguaia Guerrilla War','Cambodian Civil War','Nigerian Civil War','War of Attrition','Naxalite???Maoist insurgency','Communist insurgency in Malaysia (1968???89)','The Troubles','Years of Lead (Italy)','Warsaw Pact invasion of Czechoslovakia','1969 Somali coup d ??tat','Civil conflict in the Philippines','1969 Libyan coup d etat','Communist rebellion in the Philippines','Moro insurgency in the Philippines','Football War','Al-Wadiah War','Rupununi Uprising','Sino-Soviet border conflict','1969 Greensboro uprising','Papua conflict','','Name of conflict','','Black September in Jordan','Reggio revolt','Corrective Movement (Syria)','Dirty War (Mexico)','1971 Ugandan coup d ??tat',' Bangladesh Liberation War','Indo-Pakistani wars and conflicts ','1971 Janatha Vimukthi Peramuna Insurrection',' Indo-Pakistani War of 1971','Bangladesh Liberation War and the Indo-Pakistani wars and conflicts ','Abu Musa and the Greater and Lesser Tunbs conflict','1972 invasion of Uganda[43]','First Eritrean Civil War','1972???1975 Bangladesh insurgency','1973 Samita border skirmish','Yom Kippur War','1973 Chilean coup d etat','Armed resistance in Chile (1973???90)','Oromo Conflict','Turkish invasion of Cyprus','Arube uprising','Battle of the Paracel Islands','Ethiopian Civil War','Second Iraqi???Kurdish War','1974???75 Shatt al-Arab clashes','Islamist uprising in the Panjshir Valley','1975 China-India border skirmish','Angolan Civil War','Cabinda War',' Western Sahara War','Part of the Western Sahara conflict ','PUK insurgency','Lebanese Civil War','Cambodian???Vietnamese War','Insurgency in Laos','Indonesian invasion of East Timor','Rebellion of the Lost [pt]','Dirty War','Insurgency in Aceh','Political violence in Turkey (1976???80)','Safar uprising[48]','Mozambican Civil War','Libyan???Egyptian War','Ethio-Somali War','Chittagong Hill Tracts conflict','Shaba I','Shaba II','1978 South Lebanon conflict','Uganda???Tanzania War','Chadian???Libyan conflict','Kurdish???Turkish conflict','NDF Rebellion','Grand Mosque seizure','1979 Herat uprising','Yemenite War of 1979','Iranian Revolution','1979 Khuzestan uprising','Sino-Vietnamese War','Sino-Vietnamese conflicts 1979???90','Islamist uprising in Syria','1979 Kurdish rebellion in Iran','Al-Ansar insurgency','1979???1980 Shia uprising in Iraq','Soviet???Afghan War','Salvadoran Civil War','Second Eritrean Civil War','Internal conflict in Peru','Gwangju Uprising','Nojeh coup plot','Coconut War','Maoist insurgency in Turkey','Iran???Iraq War','Paquisha War','Ugandan Bush War','1981 Entumbane uprising','1981 Gambian coup d ??tat attempt','Casamance conflict','1982 Amol uprising','Falklands War','Ndogboyosoi War','1982 Lebanon War','Security Zone conflict','1982 Ethiopian???Somali Border War','Chadian???Nigerian War','Second Sudanese Civil War','Sri Lankan Civil War',' Kurdish rebellion of 1983','Part of the Iran???Iraq War ','Invasion of Grenada','Siachen conflict','Agacher Strip War','South Yemen Civil War','1986 United States bombing of Libya','Surinamese Interior War','Ciskei-Transkei conflict','Singing Revolution','First Intifada','1987???89 JVP insurrection','1987 Sino-Indian skirmish','Lord s Resistance Army insurgency','1988 Maldives coup d ??tat','First Nagorno-Karabakh War','Bougainville Civil War','1989 Paraguayan coup d ??tat','1989 Philippine coup attempt',' Civil war in Afghanistan (1989???92)','part of the war in afghanistan(1978???present) ','Mauritania???Senegal Border War','KDPI insurgency (1989???96)',' Insurgency in Jammu and Kashmir','Part of the Kashmir conflict ','Romanian Revolution','United States invasion of Panama','First Liberian Civil War','1900???1905 phase of the Mat Salleh Rebellion','Somaliland Campaign','War of the Golden Stool','Zande resistance[1]','Muhammad Umar Khan s rebellion[2]','Bastaard uprising of 1900[3]','1900 Hamawand revolt[4]','1900 Sudan revolt[5]','French conquest of Borno[5]','Unrest in Java[6]','1900???1903 uprising in southwest Madagascar[7]','Shoubak revolt of 1900','Sharjah conquest of Ras Al Khaimah','Russian invasion of Manchuria','Huizhou Uprising','Mahsud Waziri blockade','Kuwaiti???Rashidi war','Risings among the Agar Dinka[1]','Bastaard uprising of 1901[8]','Subjugation of Jambi[6]','French conquest of the Dendi Kingdom[9]','Revoluci??n Libertadora [es]','Anglo-Aro War','Battle of Holy Apostles Monastery','1901 Mapondera Rebellion','Holy Man s Rebellion','Kala-i-Mor railway worker s revolt[10]','1902 Sudan revolt[5]','Merauke uprising[6]','Kuanhama Rebellion of 1902-1904[11]','Bailundo Revolt of 1902','Venezuelan crisis of 1902???03','Kabul Khel expedition[12]','Expeditions against the Bantin[6] (Location: Kalimantan)','Korintji expeditions[6] (Location: Sumatra)','Campaigns against Dayak[6] (Location: Kalimantan)','Italian???Ottoman crisis of 1902[13]','Great Ming Uprising','1903 Tegale uprising[1]','1903 uprising in Bukhara[14]','Risings among the Atwot Dinka[1]','Rijal al-Ma rebellion[15]','Kavango uprising[8]','Actions on Yapen[6]','Resistance in Minangkabau[6]','Mentawei islands campaign[6]','Military actions in Flores and Solor[6]','Kerinci Expedition','Battle of Jo-Laban[16][17]','Theriso revolt','May Coup (Serbia)','Ilinden???Preobrazhenie Uprising','British expedition to Tibet','British conquest of the Sokoto Caliphate[18]','British conquest of the Kano Emirate','Saudi???Rashidi WarPart of the Unification of Saudi Arabia','Uprising of Namas in Maltah??he[8]','Bondelswarts uprising of 1904[8]','Adam Wad Muhammad s uprising[1]','Mahsud expedition of 1904[19]','1904 Ondonga uprising[8]','1904 Nama uprising[8]','1904 Sudan revolt[5]','Campaign in the Gajo and Alas islands[6]Part of the Aceh War','Dutch intervention in Bali (1904)[6]','Resistance on Tidore[6]','Sulawesi expeditions[6]','1904???1905 uprising in Madagascar','Portuguese campaign against the Ovambo(See Battle of Mufilo)','Vaccine Revolt','Revolution of 1904','1904 Sasun uprising','Herero Wars','Russo-Japanese War','Yemeni Rebellion of 1904Part of the Yemeni???Ottoman Conflicts','Macedonian Struggle','Ping-liu-li Uprising','Military actions in Onin[6]','Ottoman incursion into Persia[20]','Military actions Sumba and Sumbawa[6]','Persian Constitutional Revolution','Argentine Revolution of 1905','Shoubak Revolt of 1905','????d?? insurrection (1905)','Kurdish rebellion of 1905[30]','1905 Tibetan Rebellion','1905 Russian Revolution','Maji Maji Rebellion','Yemeni Expedition of 1905Part of the Yemeni???Ottoman Conflicts','South Sulawesi expedition','Taba Crisis of 1906','Resistance in Lombok[6]','Actions against fighters from Jambi in Indragiri[6] (Location: Sumatra)','Ottoman invasion of Persia (1906)','Sokoto Uprising of 1906[31]','1906 Mesopotamia uprising','Dutch intervention in Bali (1906)','Bambatha Rebellion','Campaign against the Mahafaly[32]','Asir rebellion[33]','Dersim uprising of 1907[34]Part of the Dersim uprisings [tr]','Huanggang Uprising','Huizhou Qin??hu Uprising','Anqing Uprising','Qinzhou Uprising','Zhennanguan Uprising','Bitlis uprising (1907)',' Dembos War of 1907-1910[31]','More info: Revoltas e Campanhas nos Dembos (1872-1919)(In Portuguese) ','Anti-Foreign Revolt[11]','Mutair revolt[35]','1907 Romanian Peasants  Revolt','Honduran-Nicaraguan War','Beipu uprising','1907 Diyarbak??r uprising[36]','Zakka Khel raids on towns and villages in the British Raj','Qin-lian Uprising','Hekou Uprising','Mapaoying Uprising','Bondelswarts rebellion of 1908[8]','Wad Hubaba Revolt','Lobi and Dyula revolt in Mali[5]','Mossi rebellions in Kouddigou and Fada N gourma[5]','Annam uprising[37]','Mohmand Expedition of 1908[38]Part of the instability on the North-West Frontier','Bazar Valley campaign','Kurdish uprising of 1908[34]Part of the Dersim uprisings [tr]','Buraida rebellion[39]','Battle of Marrakech','Mau uprising [de]','Young Turk Revolution','Hamawand rebellion','Dutch intervention in Bali (1908)','Actions in the Toba and Batak islands[6]','Actions in West-Kalimantan[6]','Dutch???Venezuelan crisis of 1908','Nyasaland resistance[5]','Battle of Nias[6]','Actions on the Halmahera, Seram, Papua and Mentawei islands[6]','Kurdish uprising of 1909[34]Part of the Dersim uprisings [tr]','Estrada s rebellion','Kola??in Affair (1909)','Zaraniq rebellion','Crazy Snake Rebellion','Second Melillan campaign','Hauran Druze Rebellion','Ouaddai War','Gengxu New Army Uprising','1910 uprising in Bukhara[40]','Portuguese conquest of the Angoche Sultanate[41]','Uprising of Cape Nguni[8]','Xiong Mi Chang s rebellion[42]','Actions on Ajer HItam and near Timor[6]','Actions in Langkat[6] (Location: Sumatra)','Portuguese conquest of the Kasanje Kingdom[43]','Mon??gasque Revolution','Battle of Hadia [ar]','Karak Revolt','Albanian Revolt of 1910','5 October 1910 revolution','Chinese expedition to Tibet (1910)','Sokehs Rebellion','Mexican Revolution',' Border War (1910???19)','Part of the Mexican Revolution ','Revolts at Moush[30]','Revolts at Khuyt[30]','1911 Kenya revolt[5]','Belitung miner s revolt[6]','Kurdish uprising of 1911[34]Part of the Dersim uprisings [tr]','Revolt of Salar-al-Daulah','Revolt of Mohammad Ali Shah Qajar[44]',' Magonista rebellion of 1911','Part of the Mexican Revolution ','1911 Paraguayan Civil War',' Russian Invasion of Tabriz','Part of the Persian Constitutional Revolution ','Albanian Revolt of 1911','Second Guangzhou Uprising','Dominican Civil War (1911???12)','French conquest of Morocco','Italo-Turkish War','East Timorese Rebellion',' Xinhai Revolution','1911 Revolution ','War of the Generals','1912 Kordofan uprising[1]','Turkoman Revolt of 1912???1913','Ecuadorian Civil War of 1912???1914','Sirte revolt[45]','Khost rebellion (1912)','First Balkan War','Albanian Revolt of 1912','Contestado War',' United States occupation of Nicaragua','Part of the Banana Wars ','Royalist attack on Chaves',' Negro Rebellion','Part of the Banana Wars ','1913 uprising in Bukhara[40]','Oyango Dande rebellion[5]','Kurdish revolt of 1913[46]','1913 Euphrates rebellion','Muscat rebellion[47]','Sino???Mongolian War of 1913???1915 [fi]','Urtatagai conflict (1913)','Atmene uprising [ru]','Conquest of al-HasaPart of the Unification of Saudi Arabia','Second Balkan War',' Tikve?? Uprising','Part of the Second Balkan War ','Ohrid???Debar Uprising','Second Revolution','Bai Lang Rebellion','1914 Kenya revolt[5]','North Java peasant revolt[6]',' Kolongongo War[48]','More info: The Mbunda Kingdom in Angola','(Section   Kolongongo war  ) ','First Yemeni???Asiri war[49]',' Dersim uprising of 1914[34]','Part of the Dersim uprisings [tr] ','Bitlis uprising','Uprising in Barzan[50]','Kongo revolt of 1914[51][52]','Operations in the TochiPart of the instability on the North-West Frontier','Revolt of Juazeiro [pt]','Zaian War','Dominican Civil War of 1914','Haitian Civil War[54]','Blayong s uprising[55]','Peasant Revolt in Albania','Truku War','World War I',' United States occupation of Veracruz','Part of the Banana Wars ','Bluff War','Ovambo Uprising','Maritz Rebellion','1915 Rehoboth Basters rebellion[8]','Betsileo uprising[7]','Sadiavahe rebellion[56]','Imerina uprising[7]','Kru Coast Rebellion[57]','Botan revolt[46]','Tapani incident','Turkoman Revolt of 1915[58]','Battle of Kanzaan (1915) [ar]','Battle of JarrabPart of the Unification of Saudi Arabia and World War I','Chilembwe uprising','Bussa rebellion','1915 Singapore Mutiny','Kelantan rebellion','Rundum revolt','Volta-Bani War',' National Protection War','Anti-Monarchy War ',' Senussi Campaign','Part of World War I ',' United States occupation of Haiti','Part of the Banana Wars ','Jambi rebellion[59]','Operations against the Mohmands, Bunerwals and Swatis in 1915Part of the instability on the North-West Frontier','Kalat Operations (1915-16)','Yarahmadzai uprising','Dersim uprising of 1916Part of the Dersim uprisings [tr]','1916 Kumyk uprising','Mohmand blockadePart of the instability on the North-West Frontier','Cuban Civil War(See Sugar Intervention)','Kaocen Revolt','1916 Cochinchina uprising','Battle of Segale','Noemvriana','Central Asian revolt of 1916','Easter Rising',' United States occupation of the Dominican Republic (1916???24)','Part of the Banana Wars ',' Arab Revolt','Part of World War I ',' Basmachi movement','Part of World War I and Russian Civil War ','Uukwanyama rebellion[8]','1917 Uganda rebellion[5]','Kurdish uprisings of 1917','February Revolution','July Days','Operations against the Mahsuds (1917)','Manchu Restoration','Th??i Nguy??n uprising','Polubotkivtsi Uprising','Toplica insurrection','1917 Kanak revolt [fr]','Kornilov Affair','Green Corn Rebellion',' October Revolution','Part of Russian Civil War ',' Kerensky???Krasnov uprising','Part of Russian Civil War ','Russian Civil War','Constitutional Protection Movement',' Ukrainian War of Independence','Part of World War I and Russian Civil War ','Ngolok rebellions (1917???49)',' Operations against the Marri and Khetran tribes (1918)[63]','Part of the instability on the North-West Frontier ','Adubi War','Simko Shikak revolt (1918???22)',' Judenburg mutiny','Part of World War I ',' Cattaro Mutiny','Part of World War I ',' Aster Revolution','Part of World War I ',' Radomir Rebellion','Part of World War I ',' Left SR uprising','Part of the Russian Civil War ','Finnish Civil War','Georgian???Armenian War','Polish???Czechoslovak border conflicts','Internal conflict in the Banat Republic','Serbian incursion into the Banat Republic','Viena expedition','First Pechenga expedition','Austro-Slovene conflict in Carinthia','German Revolution of 1918???19','Greater Poland Uprising (1918???19)','Hungarian???Czechoslovak War',' Polish???Ukrainian War','Part of the Ukrainian War of Independence ',' Georgian???Ossetian conflict (1918???20)','Part of the Russian Civil War ',' Sochi conflict','Part of the Russian Civil War ',' Armenian???Azerbaijani War','Part of the Russian Civil War ',' Estonian War of Independence','Part of the Russian Civil War ',' Latvian War of Independence','Part of the Russian Civil War ',' Lithuanian???Soviet War','Part of the Lithuanian Wars of Independence ',' Al-Khurma dispute','Part of the Unification of Saudi Arabia ','War of the Insane','Revolt of the Ingrian Finns',' Franco-Turkish War','Part of the Turkish War of Independence ','Second Yemeni???Asiri War[49]','Toli-Toli incident[6]','Garut incident[6]','Punjab Rebellion[64] (See: Amritsar Massacre)Part of the instability on the North-West Frontier','Black Sea mutiny','1919 Royalist uprising in Northern Portugal','Christmas Uprising',' Spartacist uprising','Part of the German Revolution of 1918???19 ',' Lithuanian War of Independence (War against the Bermontians)','Part of the Lithuanian Wars of Independence ','Sejny Uprising','First Barzanji Revolt',' Polish???Czechoslovak War','Part of the Polish???Czechoslovak border conflicts ','Khotyn Uprising','Hungarian???Romanian war of 1919','Turkish War of Independence','Third Anglo-Afghan War','Waziristan campaign (1919???1920)','Impresa di Fiume','Italo-Yugoslav War','First Honduran Civil War [es]','Polish???Soviet War',' First Silesian Uprising','Part of the Silesian Uprisings ','Aunus expedition','Alawite Revolt of 1919','Irish War of Independence','Kuwait???Najd War',' Greco-Turkish War (1919???1922)','Part of the Turkish War of Independence ','Revolts during the Turkish War of Independence','Franco-Syrian War','1920 uprising in Afghanistan[65]','Misurata-Warfalla War[66]','Husino rebellion','1920 Iraqi Revolt','Vlora War','1920???1922 Jabal al-Gharbi civil war',' Polish???Lithuanian War','Part of the Lithuanian Wars of Independence ','Kapp Putsch','Ruhr Uprising',' Second Silesian Uprising','Part of the Silesian Uprisings ','1920 Georgian coup attempt','May Uprising',' Turkish???Armenian War','Part of the Turkish War of Independence ','Zhili???Anhui WarPart of the Warlord Era','Second Pechenga expedition','Guangdong???Guangxi WarPart of the Warlord Era',' Dagestan Uprising','Part of the Russian Civil War ','Rif War','1920 Upper Asir conflict[49]','1921 Khorosan rebellion[67]','Kurdish uprising of Autumn 1921[46]','Waziristan campaign (1921???1924)','Anti-fascist uprising in Albona',' Red Army invasion of Georgia','Part of the Russian Civil War ',' Kronstadt rebellion','Part of the Russian Civil War ',' February Uprising','Part of the Russian Civil War ','Coto War',' Battle of Mountainous Armenia','Part of the Russian Civil War ','March Action',' Third Silesian Uprising','Part of the Silesian Uprisings ',' Mongolian Revolution of 1921','Part of Russian Civil War ','Charles I of Austria s attempts to retake the throne of Hungary','Uprising in West Hungary','Malabar rebellion','1921 Persian coup d etat','Conquest of Ha il',' East Karelian Uprising and Soviet???Finnish conflict 1921???22','Part of Russian Civil War ','Rand Rebellion','Kura Rebellion','Ikhwan attack on Najran[68]','18 of the Copacabana Fort revolt','1922 bombardment of Yemen[69]','Ikhwan raids on Transjordan','Bondelswarts Rebellion','San rebellion[8]','1922 Uukwambi revolt[8]','First Zhili???Fengtian WarPart of the Warlord Era','Rampa Rebellion of 1922','11 September 1922 Revolution','Irish Civil War','Paraguayan Civil War (1922)','Sheikh Khazal rebellionPart of the Arab separatism in Khuzestan','Second Barzanji Revolt','Tenente revolts','Aden Protectorate Insurgency[69]','Alizai rebellion of 1923','Corfu incident','Guna revolution [es]','De la Huerta Rebellion [es][71][72]','June Uprising','Leonardopoulos???Gargalidis coup d ??tat attempt','Adwan Rebellion','Posey War','Hamburg Uprising','Beer Hall Putsch','Klaip??da Revolt','September Uprising','Pacification of Libya','Arab separatism in Khuzestan','Chechen uprising of 1924[73]','Turkoman Rebellion in Eastern Iran[74]','Paulista Revolt of 1924','Beytussebab rebellion','Zazejskie uprising [ru]','Second Honduran Civil War [es]','Khost rebellion (1924???1925)','1924???1928 Saqqawist insurgency in AfghanistanEscalated into the Afghan Civil War','Vaalgras revolt[8]','August Uprising','Tungus uprising [ru]','June Revolution','1924 Estonian coup d ??tat attempt','Tatarbunary Uprising','Saudi conquest of Hejaz','Nestorian rebellion','Second Zhili???Fengtian WarPart of the Warlord Era','Third Yemeni???Asiri War[49]','First Asiri Civil War[49]','1925 Rehoboth Basters rebellion[8]','Incident at Petrich','Sheikh Said rebellion','Pink s War','Ra??kotan and Raman pacifying operations[78]','Sason rebellion[78]','Zaraniq rebellion (1925???1929)','Great Syrian Revolt','Anti-Fengtian WarPart of the Warlord Era','Urtatagai conflict','Second Asiri Civil war[49]','Asiri tribal revolts of 1926[49]','Tarimese Civil War[79]','1926 Simko Shikak revolt','Nicaraguan civil war (1926-1927)','Northern ExpeditionPart of the Warlord Era','Cristero War','1926 Communist Revolt in Indonesia','1927 Nuer uprising[1]','Ararat rebellion','Ikhwan Revolt','1927 Kurdish rebellions[78]','Ikhwan raid on BusayyaPart of the Ikhwan revolt','Chinese Civil War','Persian conquest of West Baluchistan[80][81][82][83]','Hamed bin Rafda s rebellion [ar]','Haji Abdul Rahman Limbong s rebellion','Afghan Civil War (1928???1929)','Kongo-Wara rebellion','Kazakh revolts (1929-1931)  [ru]','Escobar Rebellion','1929 Basmachi border raids on the Soviet Union','Chiang-Gui WarPart of the Warlord Era','Afghan campaign of the Red Army (1929)','Sino-Soviet conflict (1929)','Alakat Uprising [ru]','1929 Kurdish rebellions[78]','Anti-Saqqawist campaigns in Kuhdaman and Herat','Women s War','Antananarivo uprising[7]','Persian tribal uprisings of 1929','Nejd Civil War[85]','Port Berg?? rebellion[7]','Shinwari rebellion','1930 Kurdish rebellions[78]','Afridi Redshirt Rebellion','Kuhistan rebellion (February???April 1930)','Uprising of the Ngh???-T??nh Soviets','Hnov uprising [ru]','Tugsbuyant uprising [ru]','Muromtsevsky uprising [ru]','Khorinskoe uprising [ru]','Kuhistan rebellion (July 1930)','Yen Bai mutiny',' Central Plains War','Part of the Warlord Era ','Chittagong armoury raid','Gugsa Wale s Rebellion','Nghe-Tinh Revolt','Saya San Rebellion','Afghan campaign of the Red Army (1930)','Sino-Tibetan War','Brazilian Revolution of 1930','Wushe Rebellion','Idrisid Emirate Rebellion [ar]','1931 Saudi???Yemeni border skirmish','Flour Revolt [pt]','Uranian peasant uprising [ru]','1931 Cyprus Revolt','Jafar Sultan revolt','Norte Grande insurrection','Chilean naval mutiny of 1931','Najran conflict','Japanese invasion of Manchuria','Ahmed Barzani revolt','Kumul Rebellion','Uukwambi uprising[8]','Annexation of Jimma[87]','Lesko uprising','Constitutionalist Revolution','Ecuadorian Civil War','January 28 Incident','Chechen uprising of 1932 [ru]','Two-Liu War[88][89]Part of the Warlord Era','1932 armed uprising in Mongolia','Kirghiz rebellion','1932 Salvadoran peasant uprising','Sanjurjada','Leticia Incident','Chaco War','Darre Khel revolt','Emu War','Soviet???Japanese border conflicts','1933 Mohmand revolt in Afghanistan[90]','Crazy Fakir s rebellion','Actions in Inner Mongolia (1933???1936)','Boworadet Rebellion','Kazym rebellion','Anarchist uprising in Spain (1933)','De Zeven Provinci??n Mutiny','Second Cristero War [es]','Asturian Revolution','Mandalada [ru]','Soviet invasion of Xinjiang','Austrian Civil War','July Putsch','Events of 6 October','1934 Khamba Rebellion','Saudi???Yemeni War','Narrenrevolte [de]','Mohmand campaign of 1935','May 2 uprising','1935 Yazidi revolt','Goharshad Mosque rebellion','1935 Greek coup d ??tat attempt','1935???36 Iraqi Shia revolts','Brazilian uprising of 1935','Second Italo-Ethiopian War','1936 Iraqi coup d ??tat','Scythe Cross rebellion','1936 Naval Revolt (Portugal)','February 26 Incident','1936???1939 Arab revolt in Palestine','Spanish Civil War','Waziristan campaign (1936???1939)','Katawz rebellion[91]','Afghan tribal revolts of 1937[90]','Islamic rebellion in Xinjiang (1937)','Dieu Python movement','Dersim Rebellion',' Second Sino-Japanese War','Part of World War II ','Brazilian Integralist uprising of 1938 [pt]','Afghan tribal revolts of 1938[91][92]','1938 Greek coup d ??tat attempt','Sudeten German uprising','Hungarian Invasion of the Carpatho-Ukraine','Slovak???Hungarian War','Maquis insurgency','Italian invasion of Albania','World War II','1939 Ondonga uprising[8]',' Winter War','Part of World War II ','1940???1944 insurgency in ChechnyaPart of World War II and the Chechen???Russian conflict',' Czortk??w uprising','Part of World War II ',' Soviet occupation of the Baltic states (1940)','Part of World War II ',' Soviet occupation of Bessarabia and Northern Bukovina','Part of World War II ',' Franco-Thai War','Part of World War II ','Legionnaires  Rebellion','Ecuadorian???Peruvian War',' Anglo-Iraqi War','Part of World War II ',' Continuation War','Part of World War II ','Hama Rashid revolt',' June 1941 uprising in eastern Herzegovina','Part of World War II ',' Uprising in Serbia (1941)','Part of World War II ','Hukbalahap Rebellion','1943 Khuzestan revolt[95]','1943 Barzani revolt',' Italian Civil War','Part of World War II ','Woyane rebellion',' Jesselton revolt','Part of World War II ','Ukrainian Insurgent Army insurgency','Palm Sunday Coup','1944???1945 Insurgency in Balochistan','Afghan tribal revolts of 1944???1947',' Lapland War','Part of World War II ','Anti-communist resistance in Poland (1944-1946)','Jewish insurgency in Palestine','Luluabourg and Jadotville Mutiny[96]','1944 Kivu Uprising','Ili Rebellion','Goryani Insurgency','Guerrilla war in the Baltic states','Temne War[1]','First Barbary War','War of the Oranges','Fourth quarter of the Haitian Revolution','Stecklikrieg','Tedbury s War','Souliote War (1803)','Irish Rebellion of 1803','Second Anglo-Maratha War','Burmese???Siamese War (1803???05)','First Kandyan War','Napoleonic Wars',' War of the Third Coalition','Part of the Napoleonic Wars ','Padri War','1804 Mtiuleti rebellion','Battle of Suriname',' Battle of Sitka','Part of the Russian colonization of the Americas ',' First Serbian Uprising','Part of the Serbian Revolution ',' Uprising against the Dahije','Part of the First Serbian Uprising ','Castle Hill convict rebellion','Fulani War',' Russo-Persian War (1804???1813)','Part of the Russo-Persian Wars ',' Egyptian Revolution','Part of the Napoleonic Wars ','Janissaries  Revolt',' Franco-Swedish War','Part of the Napoleonic Wars ','Haitian invasion of Santo Domingo',' War of the Fourth Coalition','Part of the Napoleonic Wars ',' Russo-Turkish War (1806???1812)','Part of the Napoleonic Wars ','British invasions of the R??o de la Plata','Ashanti???Fante War','War of Christophe s Secession','Vellore Mutiny',' Anglo-Turkish War (1807???1809)','Part of the Napoleonic Wars ','Alexandria expedition of 1807','Tican s rebellion','Froberg mutiny','Brazilian slave revolt of 1807','Janissaries  Revolt',' Gunboat War','Part of the Napoleonic Wars ',' Anglo-Russian War (1807???1812)','Part of the Napoleonic Wars ','Basi Revolt',' Peninsular War','Part of the Napoleonic Wars ','Mtetwa Empire Expansion','New Zealand Musket Wars','Ottoman coups of 1807???08','Rum Rebellion','Finnish War',' Spanish reconquest of Santo Domingo','Part of the Napoleonic Wars ',' Dano-Swedish War of 1808???09','Part of the Napoleonic Wars ','Travancore Rebellion','Gurkha-Sikh War','Persian Gulf campaign of 1809','Coup of 1809',' War of the Fifth Coalition','Part of the Napoleonic Wars ','1809 Gottscheer Rebellion',' Tyrol Rebellion','Part of the Napoleonic Wars ',' Quito Revolution','Part of the Spanish American wars of independence ','Burmese???Siamese War (1809???1812)',' Bolivian War of Independence','Part of the Spanish American wars of independence ',' Argentine War of Independence','Part of the Spanish American wars of independence ',' Tecumseh s War','Part of the War of 1812 ','US occupation of West Florida','Punjab War',' Chilean War of Independence','Part of the Spanish American wars of independence ','Conquest of Hawaii','Amadu s Jihad',' Mexican War of Independence','Part of the Spanish American wars of independence ','Cambodian rebellion (1811???12)','Battle of Khakeekera','1811 German Coast uprising','Invasion of Java (1811)','Tonquin incident','Fourth Xhosa War','Ga???Fante War','Arakanese Uprising[5]',' Battle of Las Piedras','Part of the Spanish American wars of independence ','Cambodian Rebellion','Gwanseo Peasant War (1811???1812)','Paraguayan Revolt','Wahhabi War',' Venezuelan War of Independence','Part of the Spanish American wars of independence ',' Peruvian War of Independence','Part of the Spanish American wars of independence ','Battle of Shela','Aponte conspiracy',' French invasion of Russia','Part of the Napoleonic Wars ',' War of the Sixth Coalition','Part of the Napoleonic Wars ','War of 1812','Pemmican War','Eight Trigrams uprising of 1813','Afghan-Sikh Wars','Creek War','Peoria War','Brazilian slave revolt of 1814',' Swedish???Norwegian War','Part of the Napoleonic Wars ','Anglo-Nepalese War','Ashanti???Akim???Akwapim War',' Had??i Prodan s Revolt','Part of the Serbian Revolution ','Argentine Civil Wars','Slachter s Nek Rebellion','Second Barbary War','Second Kandyan War',' Hundred Days','War of the Seventh Coalition ',' Neapolitan War','Part of the Hundred Days ','Temne-Susu War[6]',' Spanish reconquest of New Granada','Part of the Spanish American wars of independence ',' Second Serbian Uprising','Part of the Serbian Revolution ','Bussa s Rebellion','Portuguese conquest of the Banda Oriental','Afaqi Khoja revolts','Pernambucan Revolt','Pentrich rising','Third Anglo-Maratha War',' First Seminole War','Part of the Seminole Wars ','Uva Rebellion','Ndwandwe???Zulu War','Burmese invasions of Assam','Caucasian War','Fifth Xhosa War','Zulu wars of conquest',' Bol??var s campaign to liberate New Granada','Part of the Venezuelan War of Independence ','Chuguev uprising','','Name of conflict','','Revolution of 1820','Cambodian rebellion (1820)','Ali Pasha s Revolt',' Ecuadorian War of Independence','Part of the Spanish American wars of independence ','Trienio Liberal','Texas???Indian wars','Siamese invasion of Kedah','Ijebu and Ife war against Owu','Wallachian uprising (1821)','Ni?? Rebellion (1821)','Ottoman???Persian War (1821???23)','Greek War of Independence','Padri War','Spanish attempts to reconquer Mexico','Comanche???Mexico Wars','1821 Alghero revolt[7]','Casa Mata Plan Revolution','War of Independence of Brazil','Haitian occupation of Santo Domingo','Hundred Thousand Sons of Saint Louis','Ochomogo War','Demerara rebellion of 1823','Expedition to the West Coast of Borneo','Revolt of Quer??taro','First Anglo-Ashanti War','First Greek civil war','Chumash revolt of 1824','Bathurst War','Confederation of the Equator Revolt','First Bone War','April Revolt','Second Greek civil war','First Anglo-Burmese War','Uprising in the Yamal tundra [ru]','Second Bone War','Aegean Sea Anti-Piracy Operations of the United States','Decembrist revolt','Cisplatine War','Java War','Franco-Trarzan War of 1825','Kurdish revolt of 1826???1837[8]','First Central American Civil War',' Russo-Persian War (1826???28)','Part of the Russo-Persian Wars ','Chernigov Regiment revolt','Siamese-Lao War','1827 Honduran coup d ??tat','Winnebago War','1828 Peruvian intervention in Bolivia [es]','Gran Colombia???Peru War','Irish and German Mercenary Soldiers  Revolt','Liberal Wars','Russo-Turkish War (1828???29)','Black War','Chilean Civil War of 1829???30','Anglo-Khasi War','','Name of conflict','','Frei??mtersturm','Algerian resistance to French rule [ar]',' July Revolution','French Revolution of 1830 ','November Uprising','Belgian Revolution','French conquest of Algeria','Port Phillip District Wars','Dutch expedition on the west coast of Sumatra','Merthyr Rising','Turner s Rebellion','Siamese???Vietnamese War (1831???34)','Baptist War','Naning War','Egyptian???Ottoman War (1831???33)','Yagan Resistance','Bosnian Uprising (1831???32)','Black Hawk War','June Rebellion','Desert Campaign (1833???34)','L?? V??n Kh??i revolt','Albanian Revolts of 1833???39','First Carlist War','Peruvian civil war of 1834','Coorg War','Priest Jovica s Rebellion','Peasants  Revolt of 1834 (Palestine)','Battle of Pinjarra','Sixth Xhosa War','1835???58 revolt in Ottoman Tripolitania','Revolution of the Reforms [es]','Salaverry-Santa Cruz War','League War','Mal?? Revolt','Zacatecas Rebellion','Texas Revolution',' Second Seminole War','Part of the Seminole Wars ','Ragamuffin War','Cabanagem','Posavina rebellion (1836)','Belogradchik rebellion (1836)','Berkovitsa rebellion (1836)','Pirot rebellion','War of the Confederation','Siege of Herat (1838)Afghan-Persian War','Revolt of 1837 (New Mexico)','Sabinada',' Lower Canada Rebellion','Part of the Rebellions of 1837 ',' Upper Canada Rebellion','Part of the Rebellions of 1837 ','Dutch???Ahanta War','Kenesary s Kazakh uprising[9]','Muhammad Ali s Yemeni ExpeditonPart of the Yemeni???Ottoman Conflicts','Battle of Blood River','Mormon War','Balaiada','Pastry War','Newport Rising','Z??riputsch','Egyptian???Ottoman War (1839???41)','Khivan campaign of 1839','War of the Supremes','First Anglo-Afghan War','First Opium War','Albanian Revolt of 1847','Uruguayan Civil War','Cambodian rebellion (1840)','Eumerella Wars','','Name of conflict','','Ni?? Rebellion (1841)','1841 rebellion in Guria','Siamese???Vietnamese War (1841???45)','Sino-Sikh War','Kurdish revolt of 1842???1847[8]','Shoorcha rebellion','Russian Conquest of Bukhara','Mier expedition','Peruvian civil war of 1843???1844','Albanian Revolt of 1843???44',' Wairau Affray','Part of the New Zealand Wars ','Battle of One Tree Hill','Dominican War of Independence','Franco-Moroccan War','Franco-Tahitian War','Albanian Revolt of 1845','First Anglo-Sikh War',' Flagstaff War','Northern War','Part of the New Zealand Wars ','Peasant uprising of 1846 [es]','Revolution of Maria da Fonte',' Hutt Valley Campaign','Part of the New Zealand Wars ','Krak??w uprising','Galician slaughter','Dutch intervention in Northern Bali (1846)','Revolt of the Faiti??es','Patuleia','Seventh Xhosa War',' Second Carlist War','War of the Madrugadores ','Mexican???American War',' Wanganui Campaign','Part of the New Zealand Wars ','Sonderbund War','Sierra Gorda Rebellion','Cayuse War','Caste War of Yucat??n','Operations against the Baizai (1847)[10]','Venezuelan Civil War of 1848???1849 [es]','Revolutions of 1848 in the Italian states','Greater Poland Uprising (1848)','French Revolution of 1848','Revolutions of 1848 in the German states',' Baden Revolution','Part of the Revolutions of 1848 in the German states ',' May Uprising in Dresden','Part of the Revolutions of 1848 in the German states ',' Palatine uprising','Part of the Revolutions of 1848 in the German states ','Revolutions of 1848 in the Habsburg areas','Wallachian Revolution of 1848','Sicilian revolution of independence of 1848','Dutch intervention in Northern Bali (1848)','Matale rebellion','First Italian War of Independence','Second Anglo-Sikh War','Hungarian War of Independence','Serb Uprising of 1848???49','Praieira revolt','Slovak Uprising of 1848???49',' First Schleswig War','The Three Years  War ','Dutch intervention in Bali (1849)','Yemeni Expedition of 1849Part of the Yemeni???Ottoman Conflicts','Burmese???Siamese War (1849???55)','Apache Wars','Operations against the Baizai (1849)','','Name of conflict','','Soninke-Marabout War (1850???1856)','1851 Chilean Revolution','Taiping Rebellion','Eighth Xhosa War','1851 French coup d ??tat',' Platine War','War against Oribe and Rosas ','Palembang Highlands Expeditions','California Indian Wars','Nian Rebellion','Kautokeino rebellion','Second Anglo-Burmese War','Montenegrin???Ottoman War (1852???53)','Herzegovina Uprising (1852???62)','Rebellion of Barquisimeto [es]','Crimean War','1854 Macedonian rebellion','Expedition against the Chinese in Montrado','Epirus Revolt of 1854','Revolution of Ayutla','Expedition against the Chinese in Montrado','Miao Rebellion (1854???73)','French conquest of Senegal','Red Turban Rebellion (1854???56)','Bleeding Kansas','Kurdish revolt of 1855[8]','First Fiji Expedition','Nepalese???Tibetan War','Santhal rebellion','Yakima War','Rogue River Wars','Battle of Ash Hollow','Puget Sound War',' Third Seminole War','part of the Seminole Wars ','Nias Expedition','Punti-Hakka Clan Wars','Peruvian civil war of 1856???1858','Filibuster War','Khost rebellion (1856???1857)','Campaign of 1856???57',' Second Opium War','Arrow War ','Anglo-Persian War',' Panthay Rebellion','Du Wenxiu Rebellion ','1857 Cheyenne Expedition',' Indian Rebellion of 1857','India s First War of Independence ','Utah War','Ecuadorian???Peruvian War (1857???1860)','Reform War','Cibaenian Revolution','Pahang Civil War','March Revolution (Venezuela) [es]','Mahtra War','Coeur d Alene War','Fraser Canyon War','Pecija s First Revolt','Cochinchina Campaign','Indigo revolt','Second Fiji Expedition','Second Italian War of Independence','Revolution of 1859','Pig War','Hispano-Moroccan War (1859???60)','Banjarmasin War','Federal War','1859 Perugia uprising','','Name of conflict','','Expedition of the Thousand','Portugal???Angoche conflict[13]','1860 Mount Lebanon civil war','Paiute War',' First Taranaki War','Second Maori War','Part of New Zealand Wars ','Colombian Civil War (1860???62)','Barasa???Ubaidat War','Occupation of Araucan??a','American Civil War',' French intervention in Mexico','Also known as Franco-Mexican War ','Dakota War of 1862',' Dungan Revolt (1862???77)','Muslim Rebellion ','Ecuadorian???Colombian War',' Battle of Shimonoseki Straits','Part of the Japanese Civil War ',' Bombardment of Kagoshima','Anglo-Satsuma War','Part of the Japanese Civil War ',' Shimonoseki Campaign','Part of the Japanese Civil War ','Ambela Campaign',' Invasion of Waikato','Part of New Zealand Wars ','Second Anglo-Ashanti War','Dominican Restoration War','January Uprising','Colorado War',' Second Taranaki War','Part of New Zealand Wars ',' Kinmon Incident and First Ch??sh?? expedition','Part of the Japanese Civil War ',' Second Schleswig War','Second Danish-German War ',' Battle of Dybb??l','Part of Second Schleswig War ',' Tauranga Campaign','Part of the New Zealand Wars ','Uruguayan War','Mejba Revolt',' Mito Rebellion','Kanto insurrection','Part of the Japanese Civil War ','Bhutan War','Conquest of Tashkent [ru]','Chincha Islands War','Snake War','Pasoemah Expedition','Paraguayan War','Peruvian civil war of 1865','Saudi Civil War','Black Hawk War (1865???72)','Powder River Expedition (1865)','Morant Bay rebellion','Hualapai War','Seqiti War',' East Cape War','Part of the New Zealand Wars ','Russo-Bukharan Wars','Haw wars',' Second Ch??sh?? expedition','Summer War ',' Austro-Prussian War','Seven Weeks War','German Civil War ',' Third Italian War of Independence','Part of the Austro-Prussian War ','Red Cloud s War','Baikal Insurrection','Cretan Revolt (1866???69)',' French campaign against Korea (1866)','Byeongin Western invasion ','1867 Macedonian rebellion','Peruvian civil war of 1867','La Genuina [es]','Blue revolution (Venezuela) [es]','Andaman Islands Expedition','Comanche Campaign','Qatari???Bahraini War',' Klang War','Selangor Civil War ','Six Years  War','Glorious Revolution (Spain)','Grito de Lares',' Titokowaru s War','Part of the New Zealand Wars ',' Boshin War','War of the Year of the Dragon','Part of the Japanese Civil War ','British Expedition to Abyssinia',' Te Kooti s War','Part of the New Zealand Wars ',' Ten Years  War','Great War ','Haitian Revolution of 1869','1869 uprising in Krivo??ije','Red River Rebellion','','Name of conflict','','Kirk???Holden war','Al-Hasa Expedition[14][15]','Aday uprising (1870) [ru]','Franco-Prussian War','Revolution of the Lances','Sheep Wars','Kalkadoon Wars','French Civil War of 1871','United States expedition to Korea','Nukapu Expedition','Dembos War (1872???1873)[16]','Yemeni Expedition of 1872Part of the Yemeni???Ottoman Conflicts','Third Carlist War',' Modoc War','Lava Beds War ','Khivan campaign of 1873','Aceh War','Revolt of the Muckers','Pabna Peasant Uprisings','Third Anglo-Ashanti War','Colfax County War','Cantonal Revolution','Brooks???Baxter War','Saga Rebellion','Japanese invasion of Taiwan (1874)','Red River War','Ethiopian???Egyptian War','Ganghwa Island incident','Las Cuevas War','Perak War','Mason County War','Shinpuren Rebellion','Razlovtsi insurrection','April Uprising','Akizuki Rebellion','Hagi Rebellion','Colombian Civil War of 1876',' Great Sioux War of 1876','Black Hills War ','Qing reconquest of Xinjiang',' Montenegrin???Ottoman War (1876???78)','Part of the Great Eastern Crisis ','Angoche Civil War[17]','Nez Perce War','Satsuma Rebellion','San Elizario Salt War','Ninth Xhosa War','Russo-Turkish War (1877???78)','Cheyenne War','Bannock War','Kanak Revolt','Lincoln County War','Kumanovo Uprising','Epirus Revolt of 1878','1878 Greek Macedonian rebellion','Kresna???Razlog Uprising','Second Anglo-Afghan War','Conquest of the Desert','Nauruan Civil War','Little War (Cuba)','Jementah Civil War','Anglo-Zulu War','War of the Pacific','Sheepeater Indian War','Victorio s War','','Name of conflict','','Basuto Gun War','Brsjak Revolt','Kurdish revolt of 1880???1881[8]','First Boer War','Mapuche uprising of 1881','French occupation of Tunisia','Mahdist War','Mandingo Wars','Pleasant Valley War','Ekumeku Movement','Timok Rebellion','First Madagascar expedition','Tonkin Campaign','Peruvian civil war of 1884???1885','Chichibu Incident','Sino-French War','Mandor Rebellion','Vose Uprising [ru]','North-West Rebellion','Serbo-Bulgarian War','Third Anglo-Burmese War','Jambi Uprising','Samoan Civil War','Karonga War','Hawaiian rebellions (1887???95)','1888???1893 Uprisings of Hazaras','Sikkim Expedition','Abushiri Revolt','Ammiyya','Johnson County War','','Name of conflict','','Qu aiti???Kathiri conflict over Mukalla[18]','1890s Hamawand revolts[19]','Edi Expedition','Revolution of the Park','First Franco-Dahomean War','Castaic Range War','Colorado Range War','Ghost Dance War','Battle of Mulayda','Yemeni Rebellion of 1891Part of the Yemeni???Ottoman Conflicts','Hunza-Nagar Campaign','Anglo-Manipur War','Chilean Civil War of 1891','Garza Revolution','Semantan War','Bafut Wars','Second Hazara Uprising','Second Franco-Dahomean War','Congo Arab war','Third Hazara Uprising','Battle of Al Wajbah','Franco-Siamese War','Macedonian Struggle','Conquest of the Bornu Empire','First Melillan campaign','First Matabele War','Revolta da Armada','Federalist Riograndense Revolution','Peruvian civil war of 1894???1895','1894 Sasun rebellion','Revolution of the 44','Donghak Peasant Revolution','First Sino-Japanese War','Second Madagascar expedition','Jandamarra Guerilla War','Mat Salleh Rebellion','Japanese invasion of Taiwan (1895)','Dungan revolt (1895???96)','Zeitun Rebellion (1895???96)','Menalamba rebellion','Fourth Anglo-Ashanti War','First Italo-Ethiopian War','Cuban War of Independence','1896???1897 Greek Macedonian rebellion','Defense of Van (1896)','Khaua-Mbandjeru Rebellion',' Anglo-Zanzibar War','The shortest war in history ','War of Canudos','Batetela Rebellion','Second Matabele War','Philippine Revolution',' Greco-Turkish War (1897)','The Thirty Days  War ','Intentona de Yauco','Benin Expedition of 1897','Tirah Campaign','1898 Baloch uprising','Abushiri revolt','Andijan uprising of 1898','Spanish???American War','Negros Revolution','Federal Revolution of 1899','Second Samoan Civil War','1898 Baloch uprising','Voulet-Chanoine Mission','Rabih War','Fulbe war [Wikidata](See Battle of Maroua???Miskin)','Boxer Rebellion','Second Boer War','Thousand Days  War','Philippine???American War','Acre War',' Second Muscovite???Lithuanian War','Muscovite???Lithuanian Wars ','Battle of Hemmingstedt','Dano-Swedish War (1501???1512)Part of the Dano-Swedish Wars','Persian???Uzbek wars','Guelders Wars','War of the Succession of Landshut','Portuguese???Mamluk naval war',' Third Muscovite???Lithuanian War','Muscovite???Lithuanian Wars ',' War of the League of Cambrai','Part of the Italian Wars and Anglo-French War (1512???14) ',' Battle of Diu','Part of the Portuguese battles in the Indian Ocean, Portuguese???Mamluk naval war and Ottoman???Portuguese confrontations ','Ottoman Civil War','Prince of Anhua rebellion','Hvar rebellion',' Portuguese conquest of Goa','Ottoman???Portuguese confrontations ','Friulian revolt of 1511','??ahkulu rebellion','Spanish???Ta??no War of San Juan???Borik??n','Malayan???Portuguese war','Bengal Sultanate???Kingdom of Mrauk U War',' Fourth Muscovite???Lithuanian War','Muscovite???Lithuanian Wars ','Spanish conquest of Iberian Navarre','Poor Conrad Rebellion','Gy??rgy D??zsa Rebellion','Battle of Chaldiran','Slovene Peasant Revolt','Arumer Zwarte Hoop',' Ottoman???Mamluk War (1516???17)','Part of the Ottoman???Mamluk wars ','Texcoco Civil War','Tr???n Cao rebellion','Prince of Ning rebellion',' Polish???Teutonic War (1519???1521)','Polish???Teutonic wars ','Spanish conquest of the Aztec Empire','Revolt of the Brotherhoods','Hildesheim Diocesan Feud','Celali rebellions','Revolt of the Comuneros','First Battle of Tam??o',' Swedish War of Liberation','Part of the Swedish War of Secession ',' Italian War of 1521???1526','Part of the Italian Wars ','Musso War','First Civil War (Kazakh Khanate)','Knights  Revolt','Second Battle of Tam??o','Siege of Rhodes (1522)','Franconian War','German Peasants  War','Dalecarlian rebellions','Amicable Grant Revolt',' War of the League of Cognac','Part of the Italian Wars ','Battle of Moh??cs','Sinhalese???Portuguese War','Spanish conquest of Yucat??n',' Hungarian campaign of 1527???1528','Part of the Ottoman???Habsburg wars ','Ethiopian???Adal war','Westrogothian rebellion','First War of Kappel','Suleiman I s campaign of 1529','Siege of Vienna','Inca Civil War',' Little War in Hungary','Part of the Ottoman???Habsburg wars ','Second War of Kappel','Spanish conquest of the Inca Empire',' Ottoman???Safavid War (1532???1555)','Part of the Ottoman???Persian wars ',' Yaqui Wars','Part of the Mexican Indian Wars and the American Indian Wars ','L?????M???c War','Silken Thomas rebellion','M??nster rebellion','Count s Feud',' Fifth Muscovite???Lithuanian War','Part of the Muscovite???Lithuanian Wars ','Toungoo???Hanthawaddy War','Iguape War','Pilgrimage of Grace','Italian War of 1536???1538','Bigod s rebellion','Conquistador Civil War in Peru','Yemeni Expedition of 1538Part of the Yemeni???Ottoman conflicts','Toungoo???Ava War','Ottoman???Portuguese conflicts (1538???1559)','Revolt of Ghent (1539???1540)','Peasant s Rebellion in Telemark','Mixt??n War','Dacke War',' Italian War of 1542???1546','Part of the Italian Wars ',' Rough Wooing','Part of the Anglo-Scottish Wars ','Koch???Ahom conflicts','Toungoo???Mrauk-U War','Schmalkaldic War','Burmese???Siamese War (1547???1549)','Jiajing wokou raids','Revolt of the Pitauds','Prayer Book Rebellion','Buckinghamshire and Oxfordshire rising of 1549','Kett s Rebellion','Chichimeca War','Italian War of 1551???1559','Second Margrave War','Tuggurt Expedition','Siege of Kazan','Kazan rebellion of 1552???1556','Wyatt s rebellion','Russo-Swedish War (1554???1557)','Saukrieg','France Antarctique','Ottoman conquest of Habesh','Ottoman???Portuguese conflicts (1538???1559)','Shane O Neill s rebellion','Livonian War','Portuguese conquest of the Jaffna kingdom','French Wars of Religion','Burmese???Siamese War (1563???1564)','Northern Seven Years  War','Mariovo and Prilep rebellion','Mughal conquest of Garha','Philippine revolts against Spain','Burmese???Siamese War (1568???1569)','Rebellion of the Alpujarras (Morisco Revolt)','Marian civil war','Eighty Years  War','First Desmond Rebellion','Rising of the North','War of the League of the Indies','Ottoman???Venetian War (1570???1573)','Ishiyama Hongan-ji War','Russo-Crimean War (1571)','Mughal invasion of Bengal','Croatian???Slovene Peasant Revolt','Danzig rebellion','Castilian War','Battle of Alc??cer Quibir (also known as  Battle of Three Kings  or  The Battle of Alcazar )','Ottoman???Safavid War (1578???1590)','Tensh?? Iga War','Second Desmond Rebellion','War of the Portuguese Succession','Ottoman???Portuguese conflicts (1586???1589)','Conquest of the Khanate of Sibir','Cologne War','Burmese???Siamese War (1584???1593)','Anglo-Spanish War (1585???1604)','War of the Polish Succession (1587???88)','Beylerbeyi event','Russo-Swedish War (1590???1595)','Portuguese invasion of Jaffna kingdom (1591)','Kosi??ski uprising','Rappenkrieg (Basel)','Siamese???Cambodian War (1591???1594)','Long Turkish War','Japanese invasions of Korea','Strasbourg Bishops  War','Cambodian???Spanish War','Moldavian Magnate Wars','Nalyvaiko Uprising','Burmese???Siamese War (1593???1600)','Nine Years  War (Ireland)','Himara Revolt','Oxfordshire rising of 1596','Serb uprising of 1596???1597','Cudgel War','War against Sigismund','','Name of conflict','','Battle of Sekigahara','Thessaly rebellion (1600)','Franco-Savoyard War (1600???1601)','Navajo Wars','Polish???Swedish War (1600???1611)','Acaxee Rebellion','Dutch???Portuguese War','Ottoman???Safavid War (1603???1618)','Polish???Muscovite War (1605???1618)','Bolotnikov rebellion','Zebrzydowski rebellion','War of the J??lich Succession','Invasion of Ryukyu','First Anglo-Powhatan War','Ingrian War','Epirus revolt of 1611','Kalmar War','Rappenkrieg','Equinoctial France War','Burmese???Siamese War (1609???1622)','Siege of Osaka','Mataram conquest of Surabaya','Uskok War','Ahom???Mughal conflicts','Tepehu??n Revolt','Polish???Swedish War (1617???1618)',' Spanish conquest of Pet??n','Part of the Spanish conquest of Guatemala and the Spanish conquest of Yucat??n ','B??ndner Wirren','Thirty Years  War','Qing conquest of the Ming','Ahom???Mughal conflicts','Polish???Ottoman War (1620???1621)','Dutch conquest of the Banda Islands','Polish???Swedish War (1621???1625)','Mughal???Sikh War (1621???35)','War of the Vicu??as and Basques','Second Anglo-Powhatan War','Ottoman???Safavid War (1623???1639)','Anglo-Spanish War (1625???1630)','Zhmaylo uprising','Relief of Genoa','Polish???Swedish War (1626???1629)','Peasants  War in Upper Austria','Later Jin invasion of Joseon','Tr???nh???Nguy???n War',' War of the Mantuan Succession','Part of the Thirty Years  War ','Fedorovych uprising','Yemeni Expedition of the 1630sPart of the Yemeni???Ottoman Conflicts','Smolensk War','Polish???Ottoman War (1633???1634)','Pequot War','Sulyma uprising','Acadian Civil War','Franco-Spanish War (1635???1659)','Qing invasion of Joseon','Pavlyuk uprising','Shimabara Rebellion','Ostryanyn uprising','Revolt of the va-nu-pieds',' First Bishops  War','Part of the Wars of the Three Kingdoms ',' Second Bishops  War','Part of the Wars of the Three Kingdoms ','Catalan Revolt','Portuguese Restoration War','Beaver Wars',' Irish Confederate Wars','Part of the Wars of the Three Kingdoms ','First War of Castro',' First English Civil War','Part of the Wars of the Three Kingdoms ','Cambodian???Dutch War',' Torstenson War','Part of the Thirty Years  War ','Kieft s War','Third Anglo-Powhatan War','Char Bouba war',' Scotland in the Wars of the Three Kingdoms','Part of the Wars of the Three Kingdoms ','Cretan War (1645???1669)','Atmeydan?? incident','Moscow uprising of 1648','Khmelnytsky Uprising','First Fronde',' Second English Civil War','Part of the Wars of the Three Kingdoms ',' Third English Civil War','Part of the Wars of the Three Kingdoms ','Mughal???Safavid War',' Cromwellian conquest of Ireland','Part of the Wars of the Three Kingdoms ','Second War of Castro','Second Fronde','D??sseldorf Cow War','Kostka-Napierski uprising','Keian Uprising','Three Hundred and Thirty Five Years  War','Guo Huaiyi rebellion','First Anglo-Dutch War','Russian???Manchu border conflicts','Swiss peasant war of 1653','Morning Star rebellion','First Swedish War on Bremen','Russo-Polish War (1654???1667)','Anglo-Spanish War (1654???1660)','Peach Tree War','Vara??din rebellion (1665???1666)','Second Northern War','Savoyard???Waldensian wars','????nar incident',' Russo-Swedish War (1656???1658)','Part of the Second Northern War ',' Dano-Swedish War (1657???1658)','Part of the Second Northern War ',' Dano-Swedish War (1658???1660)','Part of the Second Northern War ','Druze power struggle (1658???1667)','Bakhtrioni uprising','Brunei Civil War','Siege of Fort Zeelandia','Copper Riot','Bashkir rebellion (1662???1664)','Burmese???Siamese War (1662???1664)','Austro-Turkish War (1663???1664)','Lubomirski s rebellion','Second Anglo-Dutch War','Kongo Civil War','Second Swedish War on Bremen','Polish???Cossack???Tatar War (1666???1671)','War of Devolution','Stepan Razin rebellion','Angelets','Solovetsky Monastery uprising','Shakushain s revolt','Second Genoese???Savoyard War','Polish???Ottoman War (1672???1676)','Franco-Dutch War',' Third Anglo-Dutch War','Part of the Franco-Dutch War ','Revolt of the Three Feudatories','Trunajaya rebellion','Revolt of the papier timbr??',' Scanian War','Part of the Franco-Dutch War ','King Philip s War','Revolutions of Tunis','Russo-Turkish War (1676???1681)','Dzungar conquest of Altishahr','Tibet???Ladakh???Mughal War','Pueblo Revolt','Mughal???Maratha Wars','Great Turkish War',' Polish???Ottoman War (1683???1699)','Part of the Great Turkish War ','War of the Reunions',' Morean War','Part of the Great Turkish War ','Monmouth Rebellion','Second Tarnovo Uprising','Child s War','Russo-Turkish War (1686???1700)','Siamese???English War','Revolt of the Barretinas','Crimean campaigns','Dzungar???Qing Wars','Chiprovtsi uprising','Nine Years  War','Karposh s rebellion',' King William s War','Part of the Nine Years  War ',' Williamite War in Ireland','Part of the Nine Years  War ','Scottish Jacobite rising','Second Brotherhood','Komenda Wars','Azov campaigns','Streltsy uprising','Arena Massacre','Darien scheme','','Name of Conflict','','Great Northern War','Battle of Dartsedo','War of the Spanish Succession',' Queen Anne s War','Part of the War of the Spanish Succession ','Camisard Rebellion','Ottoman invasion of western Georgia (1703)','Naqib al-Ashraf revolt','R??k??czi s War of Independence','Kurid??a s Rebellion','Civil war in Poland (1704???1706) Part of the Great North War','First Javanese War of Succession','Bashkir Uprising (1704???1711)','Bavarian People s Uprising','Mughal war of succession (1707)','Bulavin Rebellion','War of the Emboabas','Comacchio war [de]','Hotaki???Safavid War','Pruth River Campaign','Cary s Rebellion','1711 Karamanli coup','Battle of Ain Dara','Tuscarora War','1712 Huilliche rebellion','New York Slave Revolt of 1712','Toggenburg War','First Fox War',' War of the Catalans','Part of the War of the Spanish Succession ','Ottoman???Venetian War (1714???18)','Yamasee War',' Jacobite rising of 1715','Also called   The Fifteen   ','1717 Omani invasion of Bahrain','War of the Quadruple Alliance','Second Javanese War of Succession','Chinese expedition to Tibet (1720)','Attingal Outbreak','Revolt of the Comuneros (Paraguay)','Chickasaw Wars','Father Rale s War','Russo-Persian War (1722???1723)','Ottoman???Hotaki War (1722???1727)','Saltpeter Wars','Appeal War','Anglo-Spanish War (1727???1729)','Second Fox War','Patrona Halil Revolt','Ottoman???Persian War (1730???1735)','Kovenu war[18]','1733 slave insurrection on St. John','War of the Polish Succession','Miao Rebellion (1735???36)','Spanish???Portuguese War (1735???1737)','Russo???Turkish War (1735???1739)','Bashkir Rebellion','Nader Shah s invasion of India','Stono Rebellion',' War of Jenkins  Ear','Part of the War of the Austrian Succession ','War of the Austrian Succession','First Silesian War','Java War (1741???1743)',' Russo-Swedish War (1741???1743)','Part of the War of the Austrian Succession ','Ottoman???Persian War (1743???1746)','Dagohoy rebellion','Chukchi War',' King George s War','Part of the War of the Austrian Succession ',' Second Silesian War','Part of the War of the Austrian Succession ',' Jacobite rising of 1745','Also called   The Forty-Five   ',' First Carnatic War','Part of the War of the Austrian Succession ','Choctaw Civil War','Civil War between Afsharid and Qajar','Second Carnatic War','Third Javanese War of Succession','Konbaung???Hanthawaddy War',' French and Indian War','Part of the Seven Years  War ','Guaran?? War','Seven Years  War',' Third Silesian War','Part of the Seven Years  War ',' Third Carnatic War','Part of the Seven Years  War ',' Pomeranian War','Part of the Seven Years  War ','Revolt of the Altishahr Khojas',' Anglo-Cherokee War','Part of the French and Indian War ','Burmese???Siamese War (1759???1760)','Tacky s War','Canek Revolt',' Fantastic War','Part of the Seven Years  War ','Berbice slave uprising','Pontiac s War',' Russo-Circassian War','Part of the Caucasian War ','Strilekrigen','Burmese???Siamese War (1765???67)','Sino-Burmese War','War of the Regulation','Mysorean invasion of Kerala','First Anglo-Mysore War','Louisiana Rebellion of 1768','Koliyivshchyna','French conquest of Corsica','Russo-Turkish War (1768???1774)','Bar Confederation','First Carib War','Danish-Algerian War','Moamoria rebellion','Moscow plague riot of 1771','T??y S??n???Nguy???n War (1771???1785)','Fakir-Sannyasi rebellion','Pugachev s Rebellion','Lord Dunmore s War','Rising of the Priests','Burmese???Siamese War (1775???1776)','First Anglo-Maratha War','American Revolutionary War','Spanish???Portuguese War (1776???1777)','Chickamauga Wars (1776???1794)','War of the Bavarian Succession',' Anglo-Spanish War','Part of the American Revolutionary War ','First Xhosa War',' Fourth Anglo-Dutch War','Part of the American Revolutionary War ','Second Anglo-Mysore War','Jahriyya revolt','Revolt of the Comuneros (New Granada)','1782 Sylhet uprising','Unification of Hawaii','1782???83 unrest in Bahrain','Kuban Nogai Uprising','Oman-Zanzibar War','Kettle War','Revolt of Horea, Clo??ca and Cri??an','Battle of R???ch G???m-Xo??i M??t','Burmese???Siamese War (1785???86)','Northwest Indian War','T??y S??n???Tr???nh War','Lofthuus  Rebellion','Shays  Rebellion','Prussian invasion of Holland','Burmese???Siamese War (1787)','Austro-Turkish War (1787???1791)','Russo-Turkish War (1787???92)','T??y S??n???Nguy???n War (1787???1802)','Russo-Swedish War (1788???1790)','Theatre War','Australian frontier wars','Sino-Nepalese War','Battle of Ng???c H???i-?????ng ??a','Menashi-Kunashir Rebellion','Third Anglo-Mysore War','Qajar conquest of the Zand Dynasty','Second Xhosa War','Li??ge Revolution','Brabant Revolution','Pemulwuy Resistance','Saxon Peasants  Revolt','Haitian Revolution','Whiskey Rebellion','Dundiya rebellion','Polish???Russian War of 1792','Burmese???Siamese War (1792)',' War of the First Coalition','Part of the French Revolutionary Wars ',' War in the Vend??e','Part of the War of the First Coalition ','Tripolitanian civil war','Cotiote War','Nickajack Expedition','Pazvanto??lu Rebellion','Ko??ciuszko Uprising','White Lotus Rebellion','Cura??ao Slave Revolt of 1795','Battle of Krtsanisi','F??don s rebellion','Hawkesbury and Nepean Wars','Second Carib War','Miao Rebellion (1795???1806)','Persian Expedition of 1796','Anglo-Spanish War (1796???1808)','1797 Rugby School rebellion','Denisko uprising','Burmese???Siamese War (1797)','Peasants  War (1798)',' War of the Second Coalition','Part of the French Revolutionary Wars ','Quasi-War','Irish Rebellion of 1798','Fourth Anglo-Mysore War',' War of Knives','Part of Haitian Revolution ','Fries s Rebellion','Third Xhosa War','Norman conquest of southern Italy','Battle of Peshawar (1001)','German???Polish War (1002???18)','Hungarian???Ahtum War','Battle of Chach','Battle at Herdaler','Fitna of al-Andalus','Second conflict in the Goryeo???Khitan War','Battle of Clontarf','Cnut the Great s conquest of England','Pisan???Genoese expeditions to Sardinia','Byzantine???Georgian wars','Battle of Pontlevoy','Boleslaw I s intervention in the Kievan succession crisis, 1018','Battle of Vlaardingen','Battle of Carham','Third conflict in the Goryeo???Khitan War','Toi Invasion','Chola expedition to North India','Chola invasion of Srivijaya','Battle of Azaz (1030)','Battle of Stiklestad','The Civil War in Georgia','Stefan Vojislav s Uprising','Battle of Dandanaqan','Uprising of Peter Delyan','Czech-Germany war','Byzantine???Norman wars','Rus ???Byzantine War (1043)','Vata pagan uprising','Byzantine???Seljuq wars','Former Nine Years War','Norman conquest of Sicily','Crusade of Barbastro','Breton???Norman War','War of the Three Sanchos','Battle of Stamford Bridge','Norman conquest of England','Norman invasion of Wales','Battle on the Nemiga River','Battle of the Alta River','Battle of Kerl??s','Kiev uprising of 1068','Battle of Pedroso','Battle of Golpejera','Uprising of Georgi Voiteh','Battle of Kerj Abu Dulaf','Saxon Rebellion','Georgian???Seljuk wars','L?????Song War','Revolt of the Earls','Varendra Rebellion','Great Saxon Revolt','Gosannen War','Rebellion of 1088',' First Crusade','Part of the Crusades ','Chola invasion of Kalinga (1097)','','Name of Conflict','',' Crusade of 1101','Part of the Crusades ',' Battle of Ramla (1101)','Part of the Crusades ',' Battle of Ramla (1102)','Part of the Crusades ',' Norwegian Crusade','Part of the Crusades ','Chola invasion of Kalinga (1110)',' 1113???15 Balearic Islands expedition','Part of the Crusades ',' Venetian Crusade','Part of the Crusades ','Muhammad Tapar s anti-Nizari campaign',' Kalmare ledung','Part of the Crusades ','Jurchen campaigns against the Song Dynasty','Byzantine-Hungarian War (1127???29)','Civil war era in Norway','Danish Civil War','The Anarchy','Baussenque Wars',' Second Crusade','Part of the Crusades ',' Northern Crusades','Part of the Crusades ','H??gen Rebellion','Heiji Rebellion','Norman invasion of Ireland','Pandyan Civil War (1169-1177)','Byzantine???Venetian War of 1171','Revolt of 1173???74',' Battle of Montgisard','Part of the Crusades ','Battle of Lod??nice',' Battle of Marj Ayyun','Part of the Crusades ',' Battle of Jacob s Ford','Part of the Crusades ','Genpei War',' Battle of Belvoir Castle','Part of the Crusades ',' Battle of Al-Fule','Part of the Crusades ','Uprising of Asen and Peter',' Battle of Cresson','Part of the Crusades ',' Battle of Hattin','Part of the Crusades ','Siege of Jerusalem',' Third Crusade','Part of the Crusades ','Conquest of Cyprus',' Crusade of 1197','Part of the Crusades ',' Livonian Crusade','Part of the Crusades ','','Name of Conflict','','War of the Antiochene Succession',' Fourth Crusade','Part of the Crusades ','Intervention in Chaldia','Anglo-Norman War (1202???04)','Anglo-French War of 1202???1214','Loon War','Bulgarian???Latin wars','Mongol invasions and conquests','Lombard Rebellion',' Albigensian Crusade','Part of the Crusades ','Welsh uprising of 1211',' Fifth Crusade','Part of the Crusades ','Battle of Bouvines','First Barons  War','Mongol conquest of the Qara Khitai','War of the Succession of Champagne','J??ky?? War','Battle of Genter',' Sixth Crusade','Part of the Crusades ','War of the Lombards','Friso-Drentic War','Dernbacher Feud',' Stedinger Crusade','Part of the Crusades ',' Bosnian Crusade','Part of the Crusades ','Teltow War','Saintonge War',' Livonian campaign against Rus ','Part of the Northern Crusades ','First Prussian Uprising','War of the Flemish Succession','War of the Thuringian Succession','Genoese occupation of Rhodes',' Seventh Crusade','Part of the Crusades ','Tumapel-Kediri war','Shepherds  Crusade (1251)','War of the Euboeote Succession','War of Saint Sabas','Rebellion of Arbanon','Epirote???Nicaean conflict (1257???59)','Toluid Civil War','Great Prussian Uprising','Mongol invasions of the Levant','Berke???Hulagu war','Scottish???Norwegian War','Second Barons  War',' Battle of Benevento','Part of Guelphs and Ghibellines ','Ma??va War','Kaidu???Kublai war','Catalan Crusade [ca]','Kelana Bhayangkara rebellion',' Eighth Crusade','Part of the Crusades ','Sambyeolcho Rebellion',' Ninth Crusade','Part of the Crusades ','War of the Cow','Mongol invasions of Japan','Manx revolt of 1275','Pamalayu Expedition','6000-mark war','Uprising of Ivaylo','Conquest of Wales by Edward I','First Mongol invasion of Burma','Mahisa Rangka rebellion','War of the Sicilian Vespers','War of the Limburg Succession','Pabali Expedition','Southwest Borneo Expedition','War of the Outlaws','Jayakatwang rebellion','Mongol invasion of Java','Majapahit invasion of Sambas','Battle of Red Ford','Anglo-French War of 1294???1303','Ranggalawe rebellion','War of Curzola','Byzantine???Venetian War (1296???1302)','First War of Scottish Independence','Franco-Flemish War','','Name of Conflict','','Second Mongol invasion of Burma','Lembu Sora rebellion','K aissape???Hvalsey war','Conquest of Sylhet','Teutonic takeover of Danzig (Gda??sk)','Crusade of the Poor','Rebellion of mayor Albert','Dehli-Seuna War','Esen Buqa???Ayurbarwada war','Battle of Morgarten','Bruce campaign in Ireland','Nambi rebellion','Semi rebellion','Ra Kuti rebellion','Shepherds  Crusade (1320)','Swedish???Novgorodian Wars','Despenser War','Peasant revolt in Flanders 1323???28','War of Metz','First War of the R??gen Succession','War of Hum','Polish???Teutonic War (1326???32)','Tver Uprising of 1327','War of the Two Capitals','Bhre Sedang and Keta rebellion','Serbian civil war of 1331','Genk?? War','Eltz Feud','Second War of Scottish Independence','Nanboku-ch?? Wars','Hundred Years  War','Trapezuntine Civil War','Majapahit invasion of Aru','Galicia???Volhynia Wars','Bulgarian???Ottoman Wars',' War of the Breton Succession','Part of the Hundred Years  War ','Byzantine civil war of 1341???47','Battle of Zava','Thuringian Counts  War','Second War of the R??gen Succession','St. George s Night Uprising','Neapolitan campaigns of Louis the Great','Byzantine???Genoese War (1348???49)','Hook and Cod wars','Red Turban Rebellion','Byzantine civil war of 1352???57','Delhite invasion of Bengal (1353???1354)','War of the Two Peters','Ispah rebellion','Jacquerie','Delhite invasion of Bengal (1353???1354)','War of the Bands','Revolt of Saint Titus','Castilian Civil War','Cham???Vietnamese War (1367???1390)','War of the L??neburg Succession','War of the Guelderian Succession','Byzantine civil war of 1373???79','War of the Eight Saints','War of Chioggia',' Tuchin Revolt','Part of the Hundred Years  War ','Battle of Kulikovo','Peasants  Revolt','Lithuanian Civil War (1381???84)','Ming conquest of Yunnan','Harelle','Despenser s Crusade','Greater Poland Civil War','1383???85 Crisis','Tokhtamysh???Timur war','Dohna Feud','Forty Years  War','Timur s invasions of Georgia','War of the Cities (1387???1389)','Kronberger feud [de]','Crusade of Tedelis','Epiphany Rising','Jingnan Campaign','','Name of Conflict','','English invasion of Scotland','Glynd??r Rising','Battle of Ankara','Ottoman Interregnum','Conquest of the Canary Islands','Percy Rebellion','Paregreg war','Scrope Rebellion','First Scutari War','Ming conquest of ?????i Vi???t',' Armagnac???Burgundian Civil War','Part of the Hundred Years  War ','Revolts of Tr???n princes','Polish???Lithuanian???Teutonic War','Ming???Kotte War',' Cabochien Revolt','Part of the Hundred Years  War ','Great Frisian War','Korbach Feud','Hunger War','Oldcastle Revolt','Lam S??n uprising','??ei Invasion','Second Scutari War','Hussite Wars','Bavarian War',' War of the Oxen','Part of the Bavarian War ','Siege of Constantinople (1422)','Siege of Thessalonica (1422-1430)','Gollub War','War of L Aquila','Muscovite Civil War','Wars in Lombardy','Dano-Hanseatic War (1426???35)','Mainz-Hessian War','Shocho uprising','Neville???Neville feud','Polish???Teutonic War (1431???35)','First Irmandi??o','Lithuanian Civil War (1431???35)','Albanian Revolt of 1432???36','Engelbrekt rebellion','Pukefejden','Luchuan???Pingmian campaigns','Transylvanian peasant revolt','Dutch???Hanseatic War','Praguerie','Old Z??rich War','Battle of Torvioll','Soest Feud','Saxon Fratricidal War','Flower war','Albanian???Venetian War','Milanese War of Succession','Tumu Crisis','First Margrave War','Revolt of Ghent (1449???53)','Kotte conquest of the Jaffna Kingdom','Jack Cade Rebellion','Navarrese Civil War','Fall of Constantinople','Morea revolt of 1453???1454','Percy???Neville feud','Thirteen Years  War (1454???66)','Flower war','Bonville???Courtenay feud','Wars of the Roses','Siege of Belgrade (1456)','Ayutthaya-Lan Na War','Koshamain s War','Bavarian War (1459???63)','Rebellion of Cao Qin','The Night Attack','Catalan Civil War','War of the Succession of Stettin','1465 Moroccan revolt','Ballaban s campaign of 1465','War of the Public Weal','Wars of Li??ge','First Irmandi??o','??nin War','War of the Priests','Bohemian War (1468???78)','B??ckler war [de]','Dano-Swedish War (1470???71)','First Utrecht Civil War','Cham???Vietnamese War (1471)','Tenochtitlan-Tlatelolco Conflict','Burgundian Wars','War of the Castilian Succession','Ottoman-Moldavian War of 1476','Austrian???Hungarian War (1477???88)','Vietnamese-Laotian War (1479???80)','Siege of Rhodes (1480)','Saltpeter War (Mexico)','Second Utrecht Civil War','War of Ferrara','Granada War','Buckingham s rebellion','1483 Flemish Revolt','Mieres Uprising','Mad War','Stafford and Lovell Rebellion','Simmel Rebellion','Kaga Rebellion','1487 Flemish Revolt','War of Rovereto','Yorkshire rebellion 1489','Bread and Cheese Revolt','First Muscovite???Lithuanian War','Bundschuh movement','Italian War of 1494???98','Russo-Swedish War (1495???97)','Cornish Rebellion of 1497','Second Cornish Uprising of 1497','Warbeck Rebellion','Swabian War','Conquest of Melilla','Rebellion of the Alpujarras (1499???1501)','Ottoman???Venetian War (1499???1503)','Italian War of 1499???1504',' Campaign by King Scorpion (I) against King   Taurus  ','Existence disputed ',' Narmer s campaign against Wash','Existence disputed ','Unification of Upper and Lower Egypt','Hor-Aha s Nubia Campaign',' Civil war between Horus Bird and Sneferka[1][2][3]','Existence disputed ','Kish-Elam War',' Enmerkar s Siege of Aratta','Existence disputed ',' Aga s Siege of Uruk','Existence disputed ','Campaigns of Sneferu','Campaigns of Enshakushanna','Campaigns of Eannatum','Lugal-Anne-Mundu s Campaign on Ur','Umma s First War of Independence','Umma s Second War of Independence','Campaigns of Lugal-zage-si','Formation of the Akkadian Empire','Sargon s Campaigns Northeast of the Akkadian Empire','Invasion of Elam','Naram-Sin s Campaign on the Lullubi','Gutian raids and conquests in the Akkadian Empire','Fall of the Gutian dynasty','Ur-Nammu s conquest of Lagash','Fall of the Neo-Sumerian Empire','War in Persenbet','Campaigns of Rim-Sin I','Elam s Invasion into Mesopotamia','Conquests of Hammurabi',' Elamite attack on Babylon','Part of the Conquests of Hammurabi ',' Hammurabi s Conquest on Larsa','Part of the Conquests of Hammurabi ','War between Babylon, Eshnunna and Mar [fr]',' Hammurabi s Conquests in the North','Part of the Conquests of Hammurabi ',' Hammurabi s War with Assyria','Part of the Conquests of Hammurabi ','Decline and Fall of the Babylonian Empire',' Kassite invasions into Babylon','Part of the Decline and Fall of the Babylonian Empire ',' Puzur-Sin s Uprising','Part of the Decline and Fall of the Babylonian Empire ',' Assyrian Civil War','Part of the Decline and Fall of the Babylonian Empire ',' Foundation of the Sealand Dynasty','Part of the Decline and Fall of the Babylonian Empire ',' Babylonian attack on the Sealand Dynasty','Part of the Decline and Fall of the Babylonian Empire ','Xia???Shang War',' Sack of Babylon','Part of the Decline and Fall of the Babylonian Empire','Part of the Campaigns of Mursili I ','Campaigns of Hattusili I','Hyksos invasion','Campaigns of Mursili I','Conquest of the Hyksos','Campaigns of Thutmose I','Campaigns of Thutmose II','Campaigns of Thutmose III',' First Syria Campaign','Part of the Campaigns of Thutmose III ',' Second Syria Campaign','Part of the Campaigns of Thutmose III ',' Third Syria Campaign','Part of the Campaigns of Thutmose III ',' Fourth Syria Campaign','Part of the Campaigns of Thutmose III ',' Fifth Syria Campaign','Part of the Campaigns of Thutmose III ',' Sixth Syria Campaign','Part of the Campaigns of Thutmose III ',' Seventh Syria Campaign','Part of the Campaigns of Thutmose III ',' Attack on Mitanni (Eighth Syria Campaign)','Part of the Campaigns of Thutmose III ',' Ninth Syria Campaign','Part of the Campaigns of Thutmose III ',' Tenth Syria Campaign','Part of the Campaigns of Thutmose III ',' Eleventh Syria Campaign','Part of the Campaigns of Thutmose III ',' Twelfth Syria Campaign','Part of the Campaigns of Thutmose III ',' Thirteenth Syria Campaign','Part of the Campaigns of Thutmose III ',' Fourteenth Syria Campaign','Part of the Campaigns of Thutmose III ',' Fifteenth Syria Campaign','Part of the Campaigns of Thutmose III ',' Sixteenth Syria Campaign','Part of the Campaigns of Thutmose III ',' Seventeenth Syria Campaign','Part of the Campaigns of Thutmose III ',' Nubian Campaign','Part of the Campaigns of Thutmose III ','Kaska invasions into the Hittite Empire','Battle of the Ten Kings','Arzawa Revolt','Wars of Ramesses II',' Battle against Sherden sea pirates','Part of the Wars of Ramesses II ',' First Syrian Campaign','Part of the Wars of Ramesses II ',' Second Syrian campaign','Part of the Wars of Ramesses II ',' Third Syrian Campaign','Part of the Wars of Ramesses II ',' Later campaigns in Syria','Part of the Wars of Ramesses II ',' Campaigns in Nubia','Part of the Wars of Ramesses II ','Piyama-Radu Revolt',' Campaigns in Libya','Part of the Wars of Ramesses II ','Battle of Nihriya','Late Bronze Age collapse','Trojan War',' Destruction of Ugarit','Part of the Late Bronze Age collapse ',' Battle of the Delta','Part of the Late Bronze Age collapse ','Diauehi-Assyrian war','Babylonian War with Elam','Kurukshetra war','Shang???Zhou War','Rebellion of the Three Guards','','Name of Conflict','','Assyrian conquest of Aram','Colchis conquer Diauehi','First Messenian War','Syro-Ephraimite War','Pekah-Ahaz War [he]','Nubian Conquest of Egypt','Colchian-Scythian war','Wars of the Chinese Spring and Autumn period','Urartu???Assyria War','Lelantine War','Sennacherib s War with Babylon','Sennacherib s campaign in Judah','Second Messenian War','Esarhaddon s War against Egypt','Assyrian conquest of Elam','Shamash-shum-ukin s Civil War','War of Qi s succession','Roman-Latin wars','Cylonian Affair','Revolt of Babylon (626 BC)','Lydian-Miletus war [ru]','Fall of Assur','Battle of Nineveh (612 BC)','Fall of Harran','Battle of Carchemish','Jewish???Babylonian war','Median-Lydian war [ru]','First Sacred War','Achaemenid Colchis war','Wars of Cyrus the Great',' Persian Revolt','Part of the Wars of Cyrus the Great ',' Cyrus  Conquest of the Lydian Empire','Part of the Wars of Cyrus the Great ',' Cyrus  Conquest of Elam','Part of the Wars of Cyrus the Great ',' Cyrus  Conquest of Babylonia','Part of the Wars of Cyrus the Great ','Battle of Alalia','Achaemenid invasion of the Indus Valley',' Ionian Revolt','Part of the Persian Wars ','Greco-Persian Wars','Latin War (498???493 BC)',' First Persian invasion of Greece','Part of the Persian Wars ','Babylonian revolts (484 BC)',' Second Persian invasion of Greece','Part of the Persian Wars ',' Greek counterattack','Part of the Persian Wars ',' First Sicilian campaign (Battle of Himera)','Part of the Sicilian Wars ','Battle of the Cremera','Wars of Warring States period in China','Battle of Cumae','Helot Revolt during the 464 BC Sparta earthquake','First Peloponnesian War','Rebellion of Inaros II','Second Sacred WarPart of the First Peloponnesian War','Samian War','Peloponnesian War','Athenian coup of 411 BC',' Second Sicilian War','Part of the Sicilian Wars ','Second Persian invasion of Greece','Corinthian War','Battle of the Allia','Artaxerxes  II Cadusian Campaign','Dardanian invasion of Epirus','First Olynthian War [de; ky; ru; sr]','Boeotian War','Revolt of the Satraps','First Spartan Revolt against the Boeotian League','Second Spartan Revolt against the Boeotian League','Perdiccas III s expedition in Upper Macedonia[4]','Wars of the Rise of Macedon','Social War','Third Sacred War',' First Samnite War','Part of the Samnite Wars ','Latin War','Philip II s campaign in Greece (Fourth Sacred War)',' Second Samnite War','Part of the Samnite Wars ','Wars of Alexander the Great','Rebellion against Macedonian Rule','Lamian War','Conquest of the Nanda Empire',' Third Sicilian campaign','Part of the Sicilian Wars ',' Antigonid???Nabataean confrontations','Part of the Wars of the Diadochi ',' Babylonian War','Part of the Wars of the Diadochi ','Bosporan Civil War',' Siege of Rhodes (305???304 BC)','Part of the Wars of the Diadochi ','Seleucid-Mauryan War','Gojoseon???Yan War',' Third Samnite War','Part of the Samnite Wars ','Gallic invasion of the Balkans','Pyrrhic War','Syrian Wars',' First Syrian War','Part of the Syrian Wars ',' Second Syrian War','Part of the Syrian Wars ',' Third Syrian War','Part of the Syrian Wars ',' Fourth Syrian War','Part of the Syrian Wars ',' Fifth Syrian War','Part of the Syrian Wars ','Chremonidean War','Kalinga War','Punic Wars',' First Punic War','Part of the Punic Wars ',' Second Punic War','Part of the Punic Wars ',' Third Punic War','Part of the Punic Wars ','Mercenary War','Parni conquest of Parthia','Barcid conquest of Hispania','Overthrow of Diodotus II','Qin s wars of unification',' Conquest of Han','Part of the Qin wars of unification ','First Illyrian War','Cleomenean War',' Conquest of Zhao','Part of the Qin wars of unification ',' First Conquest of Yan','Part of the Qin wars of unification ','Bella Gallica cisalpina [la; de]',' Conquest of Wei','Part of the Qin wars of unification ',' Conquest of Chu','Part of the Qin wars of unification ',' Second Conquest of Yan','Part of the Qin wars of unification ',' Conquest of Dai','Part of the Qin wars of unification ',' Conquest of Wu','Part of the Qin wars of unification ',' Conquest of Qi','Part of the Qin wars of unification ','Second Illyrian War','Lyttian War','Qin s campaign against the Xiongnu','Macedonian Wars',' First Macedonian War','Part of the Macedonian Wars ','Qin s campaign against the Yue tribes','Seleucid invasion of Bactria','Fall of the Qin dynasty',' Dazexiang uprising','Part of the Fall of the Qin dynasty ',' Xiang Liang s Rebellion','Part of the Fall of the Qin dynasty ',' Liu Bang s Insurrection against the Qin dynasty','Part of the Fall of the Qin dynasty ','Seleucid???Parthian wars',' Siege of Bactra','Part of the Seleucid invasion of Bactria ','Chu-Han contention','Cretan War',' Second Macedonian War','Part of the Macedonian Wars ','Han invasion of the Xiongnu','Roman-Spartan War','Roman-Syrian War','Galatian War','Bactrian Expansion into India','Dardanian-Bastarnae war',' Third Macedonian War','Part of the Macedonian Wars ','Usurpation of Eucratides','Parthian invasion into Bactria','Maccabean Revolt','Nomadic invasions into Bactria','Lusitanian War','Rebellion of the Seven States',' Han campaigns against Minyue','Part of the Han wars against the Baiyue ','Roman Servile Wars',' First Servile War','Part of the Roman Servile Wars ','Han???Xiongnu War','Roman conquest of the Balearic Islands','Jugurthine War','Cimbrian War',' Han???Nanyue War','Part of the Han wars against the Baiyue ',' Han campaigns against Dian','Part of the Han wars against the Baiyue ','Gojoseon???Han War','Civil War of Ptolemy Lathyros','War of the Heavenly Horses',' Second Servile War','Part of the Roman Servile Wars ','Battle of Gadara','Judean Civil War','Social War','Mithridatic Wars',' First Mithridatic War','Part of the Mithridatic Wars ','Sulla s first civil war','Armenian???Parthian War','Battle of Cana',' Second Mithridatic War','Part of the Mithridatic Wars ','Sulla s second civil war',' Third Servile War','or Spartacist Rebellion','Part of the Roman Servile Wars ',' Third Mithridatic War','Part of the Mithridatic Wars ',' Hasmonean Civil War','Part of the Mithridatic Wars ','Roman???Parthian Wars','Pompey s campaign in Iberia and Albania','Gallic Wars','Caesar s invasions of Britain',' Parthian War','of Marcus Licinius Crassus ','Caesar s Civil War','Pontic War [ru]','Roman civil wars',' Post-Caesarian civil war','Part of the Roman civil wars ',' Liberators  civil war','Part of the Roman civil wars ',' Sicilian revolt','Part of the Roman civil wars ','Perusine War',' Fulvia s civil war','Part of the Roman civil wars ',' Final War of the Roman Republic','Part of the Roman civil wars ','Antony s Parthian War','Cantabrian Wars','War with the Garamantes','','Name of Conflict','','Bellum Batonianum','Battle of the Teutoburg Forest','Goguryeo-Dongbuyeo Wars','Maroboduus  War with Arminius','L??lin Rebellion','Tacfarinas  Rebellion','Red Eyebrows Rebellion','Trung sisters  rebellion','Roman conquest of Britain','Iceni revolt against Publius Ostorius Scapula','War between Armenia and Iberia','Hermunduri-Chatti War','Roman???Parthian War of 58???63','Roman conquest of Anglesey','Boudica s Uprising','First Jewish???Roman War','Year of the Four Emperors','Revolt of the Batavi','Battle of Yiwulu','Destruction of the Xiongnu state','First Dacian War','Second Dacian War','Trajan s Parthian campaign',' Kitos War','Part of Trajan s Parthian Campaign ','Civil War of Wa','Bar Kokhba revolt','Roman???Parthian War of 161???166','Marcomannic Wars','Yellow Turban Rebellion','Campaign against Dong Zhuo','Year of the Five Emperors','Sun Ce s conquests in Jiangdong','Clodius Albinus  Failed Usurpation','Conquest of Garama','Roman invasion of Caledonia 208???210','Parthian war of Caracalla','Zhuge Liang s Southern Campaign','Zhuge Liang s Northern Expeditions','Civil Wars during the Crisis of the Third Century','Goguryeo-Wei War','Jiang Wei s Northern Expeditions','Gothic War (249???253)',' Invasion of Raetia by the Juthungi','Part of the Crisis of the Third Century ','Conquest of Shu by Wei',' Battle of Naissus','Part of the Crisis of the Third Century ',' Establishment of the Palmyrene Empire','Part of the Crisis of the Third Century ','Wars of Emperor Aurelian',' Campaigns against Germanic tribes','Part of the Wars of Emperor Aurelian ',' Suppression of the Uprising led by Felicissimus','Part of the Wars of Emperor Aurelian ',' Conquest of the Palmyrene Empire','Part of the Wars of Emperor Aurelian ',' Conquest of the Gallic Empire','Part of the Wars of Emperor Aurelian ','Conquest of Wu by Jin','Carausian Revolt','War of the Eight Princes','Civil wars of the Tetrarchy',' War of Constantine and Maxentius','Part of the Civil wars of the Tetrarchy ',' War of Licinius and Maximinus Daia','Part of the Civil wars of the Tetrarchy ',' Wars of Constantine and Licinius','Part of the Civil wars of the Tetrarchy ','Jewish revolt against Constantius Gallus','Great Conspiracy','Gothic War (376???382)','Tanukh revolt against Rome','Conquests of Siyaj K ak ','Battle of Fei River','Goguryeo???Wa War','Conquests of Alaric I',' Visigothic Invasion of Greece','Part of the Conquests of Alaric I ','Stilicho s Pictish War','Gildonic revolt',' Visigothic First Invasion of Italy','Part of the Conquests of Alaric I ','Battle of Mainz (406)',' Visigothic Second Invasion of Italy','Part of the Conquests of Alaric I ',' Sack of Rome (410)','Part of the Conquests of Alaric I ','Roman???Sasanian War (421???422)','Conquest of Cop??n and Quirigu??','Battle of Ravenna (432)','Hunnic invasion of Europe','Battle of Avarayr','Germanic-Hunnic Wars','Sack of Rome (455)','Battle of Cap Bon (468)','Prince Hoshikawa Rebellion','Italian conquest of Roman Dalmatia','Battle of Herat (484)','Sukhra s Hephthalite campaign','Battle of Soissons (486)','Conquest of Italy by Theoderic the Great','Franco-Visigothic Wars','Basus War','Anastasian War','Revolt of Vitalian','Iberian War','Iwai Rebellion','Battle of Unstrut','Vandalic War','Wars against the Moors','Gothic War (535???554)','First Tikal-Calakmul War','Lazic War','Bhavavarman I s invasion of Funan','Conquest of Spania','Decline and Visigothic conquest of Spania',' First Tikal-Caracol War','Part of the Tikal-Caracol Wars ','Battle of Bukhara',' First   Star War   (Second Tikal-Caracol War)','Part of the Tikal-Caracol Wars','Part of the   Star Wars   ','Lombard???Gepid War (567)','Siege of Sana a (570)','Byzantine???Sasanian War of 572???591','Sassanid reconquest of Yemen','Hermenegild s revolt','G??kt??rk civil war','Maurice s Balkan campaigns','First Perso-Turkic War','Goguryeo???Sui Wars','Frisian???Frankish wars','Sui???Former L?? War','Byzantine???Sasanian War of 602???628','Sino???Cham war','Transition from Sui to Tang','Jewish revolt against Heraclius','Second Perso-Turkic War','Muslim???Quraysh War','Third Perso-Turkic War',' First Caracol-Naranjo War','Part of the Caracol-Naranjo Wars ',' Second Caracol-Naranjo War','Part of the Caracol-Naranjo Wars ','Sasanian civil war of 628???632','Tang campaign against the Eastern Turks','Battle of Hunayn','Battle of Wogastisburg',' Second   Star War   (Third Caracol-Naranjo War)','Part of the Caracol-Naranjo Wars','Part of the   Star Wars   ','Ridda wars',' Muslim conquest of Persia','Part of the Muslim conquests ',' Muslim conquest of the Levant','Part of the Byzantine???Arab Wars ',' Third   Star War   (Fourth Caracol-Naranjo War)','Part of the Caracol-Naranjo Wars','Part of the   Star Wars   ','Emperor Taizong s campaign against Tuyuhun','Tibetan attack on Songzhou','Muslim conquest of Egypt','Tang campaigns against the Western Turks',' Tang campaign against the oasis states','Part of the Tang wars against the Western Turks ',' Tang campaign against Karakhoja','Part of the Tang wars against the Western Turks ',' Fourth   Star War  ','Part of the   Star Wars   ','Battle of Rasil',' Tang campaigns against Karasahr','Part of the Tang wars against the Western Turks ','Goguryeo???Tang War',' Muslim conquest of the Maghreb','Part of the Byzantine???Arab Wars ',' Tang campaign against Kucha','Part of the Tang wars against the Western Turks ','Emperor Taizong s campaign against Xueyantuo','Second Tikal-Calakmul War','First Fitna',' Conquest of the Western Turks','Part of the Tang wars against the Western Turks ',' Fifth and Seventh   Star War   (Tikal-Dos Pilas War)','Part of the   Star Wars   ','North expedition of Abe no HirafuAlso called Mishihase War','Baekje???Tang War','Silla???Tang Wars','Jinshin War',' Sixth   Star War  ','Part of the   Star Wars   ','Nuun Ujol Chaak s Conquest of Dos Pilas','Muslim conquest of Transoxiana',' Eighth   Star War  ','Part of the   Star Wars   ','War against Nuun Ujol Chaak',' Ninth   Star War   (Fifth Caracol-Naranjo War)','Part of the Caracol-Naranjo Wars','Part of the   Star Wars   ','Byzantine???Bulgarian Wars','Second Fitna','Palenque-Tonin?? Wars','Jasaw Chan K awiil I s Campaign on Calakmul','Battle of Varnakert',' Tenth   Star War  ','Part of the   Star Wars   ',' Eleventh   Star War  ','Part of the   Star Wars   ','Umayyad conquest of Hispania','Frankish Civil War',' Siege of Constantinople (717???18)','Part of the Byzantine???Arab Wars ','Islamic invasion of Gaul','Hayato Rebellion','Third Tikal-Calakmul War','Bashmurian revolts',' Twelfth   Star War  ','Part of the   Star Wars   ','Marwan ibn Muhammad s invasion of Georgia',' Yik in Chan K awiil s Conquest of Calakmul','Part of Yik in Chan K awiil s Conquests ','K ak  Tiliw Chan Yopaat s War against Cop??n','Berber Revolt','Zaydi Revolt','Fujiwara no Hirotsugu Rebellion',' Yik in Chan K awiil s Conquest of Waka ','Part of Yik in Chan K awiil s Conquests ',' Yik in Chan K awiil s Conquest of Naranjo','Part of Yik in Chan K awiil s Conquests ','Abbasid Revolution','Battle of Talas','An Lushan Rebellion','Alid Revolt (762???63)','Fujiwara no Nakamaro Rebellion','Thirty-Eight Years  War','Saxon Wars','Battle of Bagrevand','Tan Te  K inich s War',' Thirteenth   Star War  ','Part of the   Star Wars   ','Rebellion of Elpidius','Battle of Fakhkh','Qaysi???Yamani war (793???96)','Viking Raids on the British Isles','Viking Invasion of Ireland','Viking Invasion of Francia','Khan Krum s Wars','Paphlagonian expedition of the Rus ','Sweet Dew Incident','Viking Raids in Spain','Era of Fragmentation','Viking Raid in Portugal','Tang???Nanzhao war','Rus ???Byzantine War (860)','Hungarian invasions of Europe','Viking Invasion and Occupation of the British Isles','Kharijite Rebellion','Zanj Rebellion','Battle of Bathys Ryax','Frankish-Moravian War','Byzantine???Bulgarian war of 894???896','Rus ???Byzantine War (907)','Byzantine???Bulgarian war of 913???927','Caspian Expedition of the Rus  (913)','Fatimid invasion of Egypt (914???915)','Second Viking Invasion of Ireland','Battle of Sevan','Croatian-Bulgarian battle of 926','Battle of Lenzen','Battle of B???ch ?????ng (938)','Tengy?? no Ran','Rus ???Byzantine War (941)','Caspian Expedition of the Rus  (943)',' Battle of Lechfeld','Part of the Hungarian invasions of Europe ','Destruction of Khazaria','Second Viking Raid in Portugal','Sviatoslav s invasion of Bulgaria','Byzantine conquest of Bulgaria','War of the Three Henries (977???978)','Second Viking Invasion of the British Isles','Song???Vietnamese war (981)','Cham???Vietnamese War (982)','Rebellion of Bardas Phokas the Younger','First conflict in the Goryeo???Khitan War','Peasants  revolt of 996 in Normandy','Kopp??ny s Revolt','Battle of Svolder','Leinster revolt against Brian Bor??']
            choice = random.choice(wars)
            await ctx.send(choice)

        if randomized_item.lower() == 'senator':
            senators = ['Richard Shelby','Tommy Tuberville','Lisa Murkowski','Dan Sullivan','Kyrsten Sinema','Mark Kelly','John Boozman','Tom Cotton','Dianne Feinstein','Alex Padilla','Michael Bennet','John Hickenlooper','Richard Blumenthal','Chris Murphy','Tom Carper','Chris Coons','Marco Rubio','Rick Scott','Jon Ossoff','Raphael Warnock','Brian Schatz','Mazie Hirono','Mike Crapo','Jim Risch','Dick Durbin','Tammy Duckworth','Todd Young','Mike Braun','Chuck Grassley','Joni Ernst','Jerry Moran','Roger Marshall','Mitch McConnell','Rand Paul','Bill Cassidy','John Kennedy','Susan Collins','Angus King','Ben Cardin','Chris Van Hollen','Elizabeth Warren','Ed Markey','Debbie Stabenow','Gary Peters','Amy Klobuchar','Tina Smith','Roger Wicker','Cindy Hyde-Smith','Roy Blunt','Josh Hawley','Jon Tester','Steve Daines','Deb Fischer','Ben Sasse','Catherine Cortez Masto','Jacky Rosen','Jeanne Shaheen','Maggie Hassan','Bob Menendez','Cory Booker','Martin Heinrich','Ben Ray Luj??n','Chuck Schumer','Kirsten Gillibrand','Richard Burr','Thom Tillis','John Hoeven','Kevin Cramer','Sherrod Brown','Rob Portman','Jim Inhofe','James Lankford','Ron Wyden','Jeff Merkley','Bob Casey Jr.','Pat Toomey','Jack Reed','Sheldon Whitehouse','Lindsey Graham','Tim Scott','John Thune','Mike Rounds','Marsha Blackburn','Bill Hagerty','John Cornyn','Ted Cruz','Mike Lee','Mitt Romney','Patrick Leahy','Bernie Sanders','Mark Warner','Tim Kaine','Patty Murray','Maria Cantwell','Joe Manchin','Shelley Moore Capito','Ron Johnson','Tammy Baldwin','John Barrasso','Cynthia Lummis']
            choice = random.choice(senators)
            await ctx.send(choice)

        if randomized_item.lower() == 'representative':
            reps = ['Jerry Carl','Barry Moore','Mike Rogers','Robert Aderholt','Mo Brooks','Gary Palmer','Terri Sewell','Don Young','Tom O\'Halleran','Ann Kirkpatrick','Ra??l Grijalva','Paul Gosar','Andy Biggs','David Schweikert','Ruben Gallego','Debbie Lesko','Greg Stanton','Rick Crawford','French Hill','Steve Womack','Bruce Westerman','Doug LaMalfa','Jared Huffman','John Garamendi','Tom McClintock','Mike Thompson','Doris Matsui','Ami Bera','Jay Obernolte','Jerry McNerney','Josh Harder','Mark DeSaulnier','Nancy Pelosi','Barbara Lee','Jackie Speier','Eric Swalwell','Jim Costa','Ro Khanna','Anna Eshoo','Zoe Lofgren','Jimmy Panetta','David Valadao','Devin Nunes','Kevin McCarthy','Salud Carbajal','Mike Garcia','Julia Brownley','Judy Chu','Adam Schiff','Tony C??rdenas','Brad Sherman','Pete Aguilar','Grace Napolitano','Ted Lieu','Jimmy Gomez','Norma Torres','Raul Ruiz','Karen Bass','Linda S??nchez','Young Kim','Lucille Roybal-Allard','Mark Takano','Ken Calvert','Maxine Waters','Nanette Barrag??n','Katie Porter','Lou Correa','Alan Lowenthal','Michelle Steel','Mike Levin','Darrell Issa','Juan Vargas','Scott Peters','Sara Jacobs','Diana DeGette','Joe Neguse','Lauren Boebert','Ken Buck','Doug Lamborn','Jason Crow','Ed Perlmutter','John B. Larson','Joe Courtney','Rosa DeLauro','Jim Himes','Jahana Hayes','Lisa Blunt Rochester','Matt Gaetz','Neal Dunn','Kat Cammack','John Rutherford','Al Lawson','Michael Waltz','Stephanie Murphy','Bill Posey','Darren Soto','Val Demings','Daniel Webster','Gus Bilirakis','Charlie Crist','Kathy Castor','Scott Franklin','Vern Buchanan','Greg Steube','Brian Mast','Byron Donalds','VACANT','Lois Frankel','Ted Deutch','Debbie Wasserman Schultz','Frederica Wilson','Mario D??az-Balart','Carlos Gim??nez','Maria Elvira Salazar','Buddy Carter','Sanford Bishop','Drew Ferguson','Hank Johnson','Nikema Williams','Lucy McBath','Carolyn Bourdeaux','Austin Scott','Andrew Clyde','Jody Hice','Barry Loudermilk','Rick W. Allen','David Scott','Marjorie Taylor Greene','Ed Case','Kai Kahele','Russ Fulcher','Mike Simpson','Bobby Rush','Robin Kelly','Marie Newman','Jes??s "Chuy" Garc??a','Mike Quigley','Sean Casten','Danny K. Davis','Raja Krishnamoorthi','Jan Schakowsky','Brad Schneider','Bill Foster','Mike Bost','Rodney Davis','Lauren Underwood','Mary Miller','Adam Kinzinger','Cheri Bustos','Darin LaHood','Frank J. Mrvan','Jackie Walorski','Jim Banks','Jim Baird','Victoria Spartz','Greg Pence','Andr?? Carson','Larry Bucshon','Trey Hollingsworth','Ashley Hinson','Mariannette Miller-Meeks','Cindy Axne','Randy Feenstra','Tracey Mann','Jake LaTurner','Sharice Davids','Ron Estes','James Comer','Brett Guthrie','John Yarmuth','Thomas Massie','Hal Rogers','Andy Barr','Steve Scalise','Troy Carter','Clay Higgins','Mike Johnson','Julia Letlow','Garret Graves','Chellie Pingree','Jared Golden','Andy Harris','Dutch Ruppersberger','John Sarbanes','Anthony G. Brown','Steny Hoyer','David Trone','Kweisi Mfume','Jamie Raskin','Richard Neal','Jim McGovern','Lori Trahan','Jake Auchincloss','Katherine Clark','Seth Moulton','Ayanna Pressley','Stephen F. Lynch','Bill Keating','Jack Bergman','Bill Huizenga','Peter Meijer','John Moolenaar','Dan Kildee','Fred Upton','Tim Walberg','Elissa Slotkin','Andy Levin','Lisa McClain','Haley Stevens','Debbie Dingell','Rashida Tlaib','Brenda Lawrence','Jim Hagedorn','Angie Craig','Dean Phillips','Betty McCollum','Ilhan Omar','Tom Emmer','Michelle Fischbach','Pete Stauber','Trent Kelly','Bennie Thompson','Michael Guest','Steven Palazzo','Cori Bush','Ann Wagner','Blaine Luetkemeyer','Vicky Hartzler','Emanuel Cleaver','Sam Graves','Billy Long','Jason Smith','Matt Rosendale','Jeff Fortenberry','Don Bacon','Adrian Smith','Dina Titus','Mark Amodei','Susie Lee','Steven Horsford','Chris Pappas','Ann McLane Kuster','Donald Norcross','Jeff Van Drew','Andy Kim','Chris Smith','Josh Gottheimer','Frank Pallone','Tom Malinowski','Albio Sires','Bill Pascrell','Donald Payne Jr.','Mikie Sherrill','Bonnie Watson Coleman','Melanie Stansbury','Yvette Herrell','Teresa Leger Fernandez','Lee Zeldin','Andrew Garbarino','Thomas Suozzi','Kathleen Rice','Gregory Meeks','Grace Meng','Nydia Vel??zquez','Hakeem Jeffries','Yvette Clarke','Jerry Nadler','Nicole Malliotakis','Carolyn Maloney','Adriano Espaillat','Alexandria Ocasio-Cortez','Ritchie Torres','Jamaal Bowman','Mondaire Jones','Sean Patrick Maloney','Antonio Delgado','Paul Tonko','Elise Stefanik','Claudia Tenney','Tom Reed','John Katko','Joseph Morelle','Brian Higgins','Chris Jacobs','G. K. Butterfield','Deborah Ross','Greg Murphy','David Price','Virginia Foxx','Kathy Manning','David Rouzer','Richard Hudson','Dan Bishop','Patrick McHenry','Madison Cawthorn','Alma Adams','Ted Budd','Kelly Armstrong','Steve Chabot','Brad Wenstrup','Joyce Beatty','Jim Jordan','Bob Latta','Bill Johnson','Bob Gibbs','Warren Davidson','Marcy Kaptur','Mike Turner','VACANT','Troy Balderson','Tim Ryan','David Joyce','VACANT','Anthony Gonzalez','Kevin Hern','Markwayne Mullin','Frank Lucas','Tom Cole','Stephanie Bice','Suzanne Bonamici','Cliff Bentz','Earl Blumenauer','Peter DeFazio','Kurt Schrader','Brian Fitzpatrick','Brendan Boyle','Dwight Evans','Madeleine Dean','Mary Gay Scanlon','Chrissy Houlahan','Susan Wild','Matt Cartwright','Dan Meuser','Scott Perry','Lloyd Smucker','Fred Keller','John Joyce','Guy Reschenthaler','Glenn Thompson','Mike Kelly','Conor Lamb','Mike Doyle','David Cicilline','James Langevin','Nancy Mace','Joe Wilson','Jeff Duncan','William Timmons','Ralph Norman','Jim Clyburn','Tom Rice','Dusty Johnson','Diana Harshbarger','Tim Burchett','Chuck Fleischmann','Scott DesJarlais','Jim Cooper','John Rose','Mark E. Green','David Kustoff','Steve Cohen','Louie Gohmert','Dan Crenshaw','Van Taylor','Pat Fallon','Lance Gooden','Jake Ellzey','Lizzie Pannill Fletcher','Kevin Brady','Al Green','Michael McCaul','August Pfluger','Kay Granger','Ronny Jackson','Randy Weber','Vicente Gonzalez','Veronica Escobar','Pete Sessions','Sheila Jackson Lee','Jodey Arrington','Joaquin Castro','Chip Roy','Troy Nehls','Tony Gonzales','Beth Van Duyne','Roger Williams','Michael C. Burgess','Michael Cloud','Henry Cuellar','Sylvia Garcia','Eddie Bernice Johnson','John Carter','Colin Allred','Marc Veasey','Filemon Vela Jr.','Lloyd Doggett','Brian Babin','Blake Moore','Chris Stewart','John Curtis','Burgess Owens','Peter Welch','Rob Wittman','Elaine Luria','Bobby Scott','Donald McEachin','Bob Good','Ben Cline','Abigail Spanberger','Don Beyer','Morgan Griffith','Jennifer Wexton','Gerry Connolly','Suzan DelBene','Rick Larsen','Jaime Herrera Beutler','Dan Newhouse','Cathy McMorris Rodgers','Derek Kilmer','Pramila Jayapal','Kim Schrier','Adam Smith','Marilyn Strickland','David McKinley','Alex Mooney','Carol Miller','Bryan Steil','Mark Pocan','Ron Kind','Gwen Moore','Scott Fitzgerald','Glenn Grothman','Tom Tiffany','Mike Gallagher','Liz Cheney']
            choice = random.choice(reps)
            await ctx.send(choice)
        
        if randomized_item == 'adjective' or randomized_item == 'adj':
            adj = ['adorable','agreeable','amused','annoying','ashamed','awful','better','bloody','blushing','brave','busy','cautious','clean','cloudy','combative','condemned','courageous','crowded','cute','dead','delightful','different','distinct','doubtful','eager','elegant','encouraging','envious','expensive','faithful','fantastic','fine','frail','frightened','gifted','glorious','graceful','grumpy','healthy','hilarious','horrible','ill','inexpensive','itchy','jolly','talented','tender','thankful','tired','ugliest','unsightly','uptight','vivacious','wicked','witty','wrong\n https://tenor.com/view/wrong-drumpf-trump-stupid-gif-6220235','adventurous','alert','angry','anxious','attractive','bad','bewildered','blue','bored','breakable','calm','charming','clear','clumsy','comfortable','confused','crazy','cruel','dangerous','defeated','depressed','difficult','disturbed','drab','easy','embarrassed','energetic','evil','exuberant','famous','fierce','foolish','frantic','funny','glamorous','good','grieving','handsome','helpful','homeless','hungry','important','innocent','jealous','joyous','tame','tense','thoughtful','tough','ugly','unusual','vast','wandering','wide-eyed','worried','zany','aggressive','alive','annoyed','arrogant','average','beautiful','black','blue-eyed','brainy','bright','careful','cheerful','clever','colorful','concerned','cooperative','creepy','curious','dark','defiant','determined','disgusted','dizzy','dull','elated','enchanting','enthusiastic','excited','fair','fancy','filthy','fragile','friendly','gentle','gleaming','gorgeous','grotesque','happy','helpless','homely','hurt','impossible','inquisitive','jittery','kind','tasty','terrible','thoughtless','troubled','uninterested','upset','victorious','weary','wild','worrisome','zealous']
            choice = random.choice(adj)
            await ctx.send(choice)
        
        if randomized_item == 'friendgroup' or randomized_item == 'fg':
            friends = ['Liam', 'Abby', 'Anika', 'Dominic', 'Armen', 'Katie', 'James', 'Onur']
            choice = random.choice(friends)
            await ctx.send(choice)
    
    
    @random.error
    async def randerror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Argument", value='The randomizer needs something valid to randomize')
            await ctx.send(embed=embed)

    @commands.command(aliases=['ml'])
    async def madlibs(self, ctx, user1:discord.User, user2:discord.User, word_count:int):
        start_sentence = []
        part_of_speech = ['Noun', 'Verb', 'Adjective', 'Adverb', 'Article', 'Conjunction']
        articles = ['a', 'the']
        conjunction = ['and', 'but', 'for', 'because', 'or']
        def check1 (m):
            if m.author == user1 or m.author == user2:
                return m.content is not None and m.channel == ctx.channel

        for x in range(0, word_count) :
            chosen_part = random.choice(part_of_speech)
            if chosen_part == 'Conjunction' or chosen_part == 'Article':
                if chosen_part == 'Conjunction':
                    word = random.choice(conjunction)
                    start_sentence.append(word)

                if chosen_part == 'Article':
                    word = random.choice(articles)
                    start_sentence.append(word)
            else:
                await ctx.send(chosen_part + ' is the next part of speech for the game.')
                msg = await self.bot.wait_for('message', check=check1)
                start_sentence.append(msg.content)
        output = ' '.join(start_sentence)
        await ctx.send(output)


    @madlibs.error
    async def madliberror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide all required fields. Make sure they are correct as well.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='The word count must be an integer')
            await ctx.send(embed=embed)


    @commands.command(name='8ball', aliases=['eightball'])
    async def eightball(self, ctx, *, question):
        """The 8ball will try to predict the answer to a yes or no question."""
        responses = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]

        embed = Embed(title="8ball predicts that...", colour=0x000080)
        print("Question from 8ball: " + question)

        if any(word in question for word in france):
            embed.add_field(name=f"Question: {question}", value="France will always find a way to surrender, even in that circumstance.")
        elif any(word in question for word in andrew):
            embed.add_field(name=f'Question: {question}', value="Sorry, I don't answer questions for deceitful liberals.")
        else:
            embed.add_field(name=f'Question: {question}', value=f'{random.choice(responses)}')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870409765728182352/8ball.png')
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Pondered by {ctx.author.name}')
        await ctx.send(embed=embed)
        
    @eightball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Question", value='The 8ball requires a question to answer.')
            await ctx.send(embed=embed)
        
    @commands.command()
    async def weirdfact(self, ctx):
        """Sends a weird fact about the world."""
        await ctx.send(random.choice(random_fact_list))

    @commands.command(aliases=['mitch','weirdo'])
    async def creep(self,ctx):
        """he rly is a creep"""
        await ctx.send('https://tenor.com/view/mitch-mc-connell-mitch-mcconnell-smile-awkward-gif-8010168')

    @commands.command(aliases=['ooc'])
    async def outofcontext(self,ctx):
        """You have done that yourself"""
        embed = discord.Embed(title='Interesting...', color=0x000080)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870717643315888168/bae_emoji.png')
        embed.set_image(url=random.choice(ooc))
        embed.add_field(name=random.choice(oocname), value=random.choice(ooctext))
        await ctx.send(embed=embed)

    """@commands.command()
    async def prank(self, ctx, joke):

        if not (ctx.voice_client):
            channel = ctx.message.author.voice.channel
            await channel.connect()
        
        if joke.lower() == 'rickroll':
            embed = Embed(title='Another One Bites the Dust...', color=0x000080)
            embed.add_field(name=f"+1 to {ctx.author.name}'s rickroll counter!", value="Good job, you're rising up in the world.")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870765083406508092/rickmanhedobekindanice.jpg')
            await ctx.send(
                embed=embed,
                components = [
                    Button(style=ButtonStyle.URL, label='Claim Reward!', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                ]
            )
            interaction = await self.bot.wait_for("button_click", check=lambda i: i.component.label.startswith("Claim"))
            await interaction.respond(content="You have claimed your reward!")

        elif joke.lower() == 'soviet':
            embed = Embed(title='Good Job Comrade!', color=0x000080)
            embed.add_field(name=f"{ctx.author.name} is really becoming a true Comrade.", value="One day you might become the leader of the Soviet Union.")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870451513854672896/soviet_union_flag.png')
            await ctx.send(embed=embed)
        
        elif joke.lower() == 'crabrave':
            embed = Embed(title='CRAB RAVEEEE', color=0x000080)
            embed.add_field(name=f"{ctx.author.name} just why", value="Ig we have a crab rave now...")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/795023687501611018/872228944827539466/DUNDUNDUNDANUN.jpg')
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="You must pick a valid option.", value='As of now its just Rick Astley and the Soviet Anthem.')
            await ctx.send(embed=embed)

        voice = ctx.guild.voice_client
        song = joke + '.mp3'
        source = FFmpegPCMAudio(song)
        voice.play(source)

    @prank.error
    async def prank_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Can't have both at once sadly", value='You must pick a prank to do.')
            await ctx.send(embed=embed)"""

    @commands.command()
    async def leavevc(self, ctx):

        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
        else:
            embed = discord.Embed(title='Error', description='I am not in a voice channel.', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def pause(self, ctx):
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)

    @commands.command()
    async def mlg(self, ctx):
        embed = discord.Embed(title='Super Intense Minecraft Player Here', color=0x000080)
        embed.set_image(url='https://cdn.discordapp.com/attachments/783881442622308382/870725370456977498/image0.jpg')
        await ctx.send(embed=embed)

    @commands.command()
    async def tord(self, ctx, tord):
        if tord == 'dare':
            embed = discord.Embed(title='Dare!', color=0x000080)
            embed.add_field(name="Your dare is to...", value=random.choice(dares))
            await ctx.send(embed=embed)

        elif tord == 'truth':
            embed = discord.Embed(title='Truth!', color=0x000080)
            embed.add_field(name="Your truth is to...", value=random.choice(truths))
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title='Error', description='You must pick either truth or dare.', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            await ctx.send(embed=embed)

    @tord.error
    async def tord_error(self,ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="You must choose", value='You must select truth or dare in order to play.')
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gstart(self, ctx):
        await ctx.send("Giveaway started. Answer the questions within 15 seconds.")

        questions = ["Which channel should it be hosted in?",
                    "What should be the duration of the giveaway? (s, m, h, d)",
                    "What is the prize?"]

        answers = []

        def check(m: discord.Message):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.bot.wait_for(event='message', check=check, timeout=15.0)
            except asyncio.TimeoutError:
                await ctx.send("You did not answer in time.")
                return
            else:
                answers.append(msg.content)
            

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"Please mention a channel correctly such as {ctx.channel.mention}")
            return

        channel = self.bot.get_channel(c_id)
        
        time = convert(answers[1])
        if time == -1:
            await ctx.send(f'You must use a correct unit.')
            return
        elif time == -2:
            await ctx.send(f"Time must be an integer.")
            return
        prize = answers[2]

        await ctx.send(f"Giveaway will be held in {channel.mention} and will last {answers[1]}!")


        embed = discord.Embed(title = "Giveaway", description = f"{prize}", color = 0x000080)

        embed.add_field(name="Hosted by:", value=ctx.author.mention)

        embed.set_footer(text=f"Ends {answers[1]} from now!")

        my_msg = await channel.send(embed = embed)


        await my_msg.add_reaction("????")


        await asyncio.sleep(time)


        new_msg = await channel.fetch_message(my_msg.id)


        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        winner = random.choice(users)

        await channel.send(f"Congrats! {winner.mention} has won {prize} from the giveaway!")

    @gstart.error
    async def gstarterror(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Permissions", value="You aren't qualified enough to just give things away.")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reroll(self,ctx, channel:discord.TextChannel, id_:int):
        try:
            new_msg = await channel.fetch_message(id_)
        except:
            await ctx.send("The id is invalid.")
            return
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        winner = random.choice(users)

        await channel.send(f"Congrats! {winner.mention} is the new winner of the giveaway.")

    @reroll.error
    async def gstarterror(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Permissions", value="You aren't qualified enough to just give things away.")
            await ctx.send(embed=embed)

    @commands.command(aliases=['nw'])
    async def nerdwars(self, ctx, nerd1:discord.User, nerd2:discord.User, *, prompt):
        embed = discord.Embed(title="Nerd Wars!", color=0x000080)
        embed.add_field(name="Prompt:", value=prompt)
        embed.set_footer(text=f"{nerd1.name} vs {nerd2.name}")
        await ctx.send(embed=embed)


        global nerd_1
        global nerd_2
        nerd_1 = nerd1
        nerd_2 = nerd2

        def check(m):
            return nerd1.author == m.author or nerd2.author == m.author
        time = 180
        await asyncio.sleep(time)

        await ctx.send(f'{nerd1.mention} and {nerd2.mention} times up!')
        embed = discord.Embed(title="Results!", color=0x000080)

        if nerd1_score_list != []:
            embed.add_field(name=f'{nerd1.name} got {len(nerd1_score_list)}', value=f', '.join(nerd1_score_list))
        if nerd1_score_list == []:
            embed.add_field(name=f'{nerd1.name} got {len(nerd1_score_list)}', value="None")
        if nerd2_score_list != []:
            embed.add_field(name=f'{nerd2.name} got {len(nerd2_score_list)}', value=f', '.join(nerd2_score_list))
        if nerd2_score_list == []:
            embed.add_field(name=f'{nerd2.name} got {len(nerd2_score_list)}', value="None")
        await ctx.send(embed=embed)
        nerd_1 = None
        nerd_2 = None
        nerd1_score_list.clear()
        nerd2_score_list.clear()

    @nerdwars.error
    async def nerdwarserror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide all required fields. Make sure they are correct as well.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='All arguments must be mentions except the prompt.')
            await ctx.send(embed=embed)

    @commands.command(description='Only true nerds can win at this.', aliases=['nwa', 'ans', 'answer', 'a'])
    async def nwanswer(self, ctx, *, answer:str):
        global nerd_1
        global nerd_2
        
        if ctx.author == nerd_1:
            if answer.title() not in nerd1_score_list and answer.title() not in nerd2_score_list:
                nerd1_score_list.append(answer.title())
                await ctx.send(f"+1 point to {ctx.author.mention}")
            elif answer.title() in nerd1_score_list or answer.title() in nerd2_score_list:
                await ctx.send("Someone has already answered that.")

        elif ctx.author == nerd_2:
            if answer.title() not in nerd1_score_list and answer.title() not in nerd2_score_list:
                nerd2_score_list.append(answer.title())
                await ctx.send(f"+1 point to {ctx.author.mention}")
            elif answer.title() in nerd1_score_list or answer.title() in nerd2_score_list:
                await ctx.send("Someone has already answered that.")

        else:
            await ctx.send("You are not currently playing a nerdwars.")

    @nwanswer.error
    async def nwanswererror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide all required fields. Make sure they are correct as well.')
            await ctx.send(embed=embed)

    @commands.command(description="Will send a question for you to answer.", aliases=["quiz"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def trivia(self, ctx, *, category=None):
        questions = [["What year did WW2 start? (History)", "C", 1, "A: 1936\nB: 1914\nC: 1939\nD: 1938", "history"],
                     ["What was the precursor to the Republican Party? (History)", "A", 3, "A: Opposition Party\nB: Unconditional Union Party\nC: Whig Party\nD: Nullifier Party", "history"],
                     ["What does SSD stand for? (Computer Science)", "D", 2, "A: Solid State Disk\nB: Static State Disk\nC: Static State Drive\nD: Solid State Drive", "computer science"],
                     ["Which island in Indonesia has the most population? (Geography)", "B", 2, "A: Borneo\nB: Java\nC: Sumatra\nD: Timor", 'geography'],
                     ["What is the territory that France ceded in the Franco-Prussian war? (History)","A", 2, "A: Alsace-Lorraine\nB: Savoy\nC: Maginot\nD: Calais", "history"],
                     ["A communist or authoritarian state normally requires what system? (Political Science)", "C", 2, "A: Nonpartisan System\nB: Fascism\nC: One Party System\nD: Multiparty System", "political science"],
                     ["What was Coldplay's first album? (Music)","D", 2, "A: A Rush of Blood to the Head\nB: A Head Full of Dreams\nC: X&Y\nD: Parachutes", "music"],
                     ["What is the closest star to Earth other than the Sun? (Astronomy)", "B", 1, "A: Sirius A\nB: Alpha Centauri\nC: The North Star\nD: Bernard's Star", "astronomy"],
                     ["What is Sumerian, family and larger than a whale? (Jokes)", "D", 1, "A: Chariots\nB: Mesopatamia\nC: Spears\nD: Ur mom", 'joke'],
                     ["How many Pok??mon were in the original games (Red/Blue)? (Gaming)", "B", 2, "A: 809\nB: 151\nC: 333\nD: 69", 'gaming'],
                     ["Which empire was the largest in history? (History)", "A", 1, "A: British Empire\nB: Mongol Empire\nC: Roman Empire\nD: Spanish Empire", 'history'],
                     ["Who was the president before Abraham Lincoln? (History)", "C", 3, "A: Taylor\n B: Polk\n C: Buchanan\n D: Jackson", "history"],
                     ["What is the most spoken language in the world? (Language)", "B", 1, "A: Hindi\n B: Mandarin\n C: English\n D: Spanish", 'language'],
                     ["What is the most searched website in the US?(as of 2020) (General Trends)", "D", 2, "A: YouTube\n B: Facebook\n C: Twitter\n D: Google", "general trends"],
                     ["What is the one country without a national anthem? (Geography)", "C", 3, "A: The Republic of Bosnia and Herzegovina\n B: Barbados\n C: Islamic Emirate of Afghanistan\n D: Republic of Mozambique", "geography"],
                     ["(cosx)/(sinx) is equal to what? (Math)", "A", 2, "A: cotx\n B: cscx\n C: secx\n D: tanx", "math"],
                     ["What tempo is typically used in marches? (Music)", "D", 2, "A: 90 BPM\n B: 100 BPM\n C: 110 BPM\n D: 120 BPM", "music"],
                     ["In 1937, the supreme court generally switched its position on which clause of the constitution from narrow to broad? (Law)", "B", 3, "A: Common Defense Clause\n B: Commerce Clause\n C: Revenue Clause\n D: Property Clause", "law"],
                     ["What is the process of people willingly moving that causes uneven congressional districts? (Political Science)", "C", 2, "A: Natural Selection\n B: Self Detirmination\n C: Self Sorting\n D: Reassortment", "political science"], 
                     ["What is a Fatwa? (Law)", "A", 3, "A: A non binding opinion by an Islamic Scholar\n B: A Jewish law scripture\n C: Vedic laws about worship\n D: Another word for plantiff", "law"],
                     ["What is the name of the successor state to the Islamic Republic of Afghanistan? (History)", "D", 2, "A: The Democratic People's Republic of Afghanistan\n B: The Taliban\n C: Afghani Provisional Government\n D: The Panjshir Resistance", "history"],
                     ["The theodemocracy used in Iran is similar to the system of what 19th century North American State? (Political Science)", "B", 3, "A: The Republic of Texas\n B: State of Deseret\n C: Vermont Republic\n D: The United Mexican States", "political science"],
                     ["What is the Derivative of 4x+3? (Math)", "C", 3, "A: 3\n B: There isn't a derivative\n C: 4\n D: 3.5", 'math'],
                     ["What is the systematic name of a molecule with 6 carbon atoms, all linked by single bonds, with one fluorine atom replacing the hydrogen of the 3rd carbon? (Chemistry)", "A", 2, "A: 3-Flourohexane\n B: Gamma-Hexoflouride\n C: Third-Bonded Hexane\n D: Chi-Flourohexane", "chemistry"],
                     ["What is the 4th letter of the Greek Alphabet? (Language)", "B", 1, "A: Epsilon\n B: Delta\n C: Eta\n D: Zeta", "language"],
                     ["Which list correctly describes the order of ideologies that Germany followed in the 20th century? (History)", "D", 3, "A: Democracy, Fascism, Communism, Monarchy\n B: Naziism, Marxism, Democracy\n C: Kaiserreich, Weimar, NDSAP, Soviet Puppet, Democracy\n D: Monarchy, Democracy, Fascism, Communism, Democracy", "history"],
                     ["What scientist who worked with Otto Hahn has their name on the periodic table? (History)", "C", 2, "A: Marie Curie\n B: Fritz Haber\n C: Lise Meitner\n D: Eugen Fischer", "history"],
                     ["What is the genus of Oak trees? (Biology)", "B", 2, "A: Areca\n B: Quercus\n C: Acer\n D: Juglans", "biology"], 
                     ["What is the limit as x approaches 0 of sinx/x? (Math)", "A", 1, "A: 1\n B: ??\n C: -1\n D: -??", "math"],
                     ["Who was the first lord protector of England? (History)", "D", 1, "A: William of Orange\n B: William the Conqueror\n C: ??thelred\n D: Oliver Cromwell", "history"],
                     ["What is the most stable radioactive isotope of Carbon? (Chemistry)", "C", 2, "A: Carbon-12\n B: Carbon-13\n C: Carbon-14\n D: Carbon-15", "chemistry"],
                     ["What is an example of a non object-orientated programming language? (Computer Science)", "B", 1, "A: Python\n B: SQL\n C: Java\n D: Ruby", "computer science"],
                     ["What does *args do in Python? (Computer Science)", "C", 3, "A: Returns a list of all used arguments inside a function\n B: Returns the number of arguments used in a function\n C: Unpacks a list called args to be used as positional arguments in a function call\n D: Sets a default value for arguments used for a function", "computer science"],
                     ["What are the most common types of loops in programming languages? (Computer Science)", "A", 1, "A: For & While loops\n B: Repeating & Timed loops\n C: While & Repeating loops\n D: For & Timed loops", "computer science"]
                     ]

        answers = []
        def check (m):
            return m.author == ctx.author and m.channel == ctx.channel
        completed = False
        if category == None:
            question_used = random.choice(questions)
        elif category == 'history':
            history_questions = []
            for q in questions:
                if q[4] == 'history':
                    history_questions.append(q)
                    completed = True
            question_used = random.choice(history_questions)
        elif category == 'chemistry':
            chem_questions = []
            for q in questions:
                if q[4] == 'chemistry':
                    chem_questions.append(q)
                    completed = True
            question_used = random.choice(chem_questions)
        elif category == 'math':
            math_questions = []
            for q in questions:
                if q[4] == 'math':
                    math_questions.append(q)
                    completed = True
            question_used = random.choice(math_questions)
        elif category == 'computer science':
            comp_questions = []
            for q in questions:
                if q[4] == 'computer science':
                    comp_questions.append(q)
                    completed = True
            question_used = random.choice(comp_questions)
        else:
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Invalid Argument", value='That is not a valid category.')
            await ctx.send(embed=embed)
            return
            

        embed = discord.Embed(title="Question!", color=0xFFFF00)
        embed.add_field(name=question_used[0], value=question_used[3])
        embed.set_author(name=f"Difficuly Level {question_used[2]}")
        embed.set_footer(text="Type the letter of the answer, not the words.")
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/871723684816097370/questiones.png')
        await ctx.send(embed=embed)
       
        words = await self.bot.wait_for(event="message", check=check)
    
        answers.append(words.content)
        if str(answers[0]).lower() == str(question_used[1]).lower():
            result = sheet.values().get(spreadsheetId=TRIVIA_ID,
                        range="Streaks!A1:C2400").execute()
            values = result.get('values')
            found = False
            counter = 0
            for row in values:
                counter += 1
                if ctx.author.name == row[0]:
                    streak = int(row[1]) + 1
                    total_correct = int(row[2]) + 1
                    found = True
                    streaks.update_cell(counter, 2, streak)
                    streaks.update_cell(counter, 3, total_correct)
            if not found:
                streak = 1
                total_correct = 1
                inputs = [[ctx.author.name, streak, total_correct]]
                request = sheet.values().append(spreadsheetId=TRIVIA_ID, 
                            range="Streaks!A1", valueInputOption="USER_ENTERED", body={"values":inputs}).execute()
            if streak >= 5:
                embed = discord.Embed(title="YOU'RE ON FIRE!", color=0xFFA500)
                embed.add_field(name=f"You have added another correct answer to your collection.", value=f"Total: {total_correct}")
                embed.set_footer(text=f"Streak: {streak} in a row")
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/850408868919509004/883765428986478642/fire.png')
                await ctx.send(embed=embed)
                return
            if streak < 5:
                embed = discord.Embed(title="Correct!", color=0x00FF00)
                embed.add_field(name=f'You have added another correct answer to your collection.',value=f'Total: {total_correct}')
                embed.set_footer(text=f"Streak: {streak} in a row")
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/871435654049955860/CHECKMARKSTHESPOT.png')
                await ctx.send(embed=embed)
                return
            
        else:
            result = sheet.values().get(spreadsheetId=TRIVIA_ID,
                        range="Streaks!A1:C2400").execute()
            values = result.get('values')
            found = False
            counter = 0
            for row in values:
                counter += 1
                if ctx.author.name == row[0]:
                    streak = 0
                    total_correct = int(row[2])
                    found = True
                    streaks.update_cell(counter, 2, streak)
                    
            if not found:
                streak = 0
                total_correct = 0
                inputs = [[ctx.author.name, streak, total_correct]]
                request = sheet.values().append(spreadsheetId=TRIVIA_ID, 
                            range="Streaks!A1", valueInputOption="USER_ENTERED", body={"values":inputs}).execute()
            embed = discord.Embed(title="Incorrect!",color=0xFF0000)
            embed.add_field(name=f"The correct answer was {str(question_used[1])}",value=f"Difficulty Level: {question_used[2]}")
            embed.set_footer(text=f'Streak: {streak}')
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
        await ctx.send(embed=embed)
            


    @commands.command()
    async def miniship(self, ctx, name1:str, name2:str):
        test1 = len(name1)
        test2 = len(name2)
        splicer1 = random.randint(1, test1)
        splicer2 = random.randint(0, test2)
        ship1 = name1[:splicer1]
        ship2 = name2[splicer2:]
        shipname = str(ship1)+str(ship2)
        ship_score = random.randint(0, 1000)
        if ship_score < 5:
            ship_statement = "You go worse than dinosaurs and comets and then some. Just say goodbye to that matchup."
        elif 5 <= ship_score < 25:
            ship_statement = "You go together like Kimmy and South Korea. Not well, as South Korea clearly doesn't exist. Its just The Democratic People's  Republic of Korea. They just like to be rebellious..."
        elif 25 <= ship_score < 50:
            ship_statement = "Schlafly would be a better match than this for both of you."
        elif '69' in str(ship_score):
            ship_statement = "????"
        elif 50 <= ship_score < 100:
            ship_statement = "You work about as well as Anakin and younglings."
        elif 100 <= ship_score < 150:
            ship_statement = "A website could treat u better than this. Well *almost* any website..."
        elif 150 <= ship_score < 200:
            ship_statement = "You all would work better than Gorbachev and the Soviet Union, but *dang* the Pizza Hut was good."
        elif 200 <= ship_score < 250:
            ship_statement = "Mike Pence would kiss the fly on his head before you both got along."
        elif 250 <= ship_score < 350:
            ship_statement = "This working out is as likely as Poland surviving in World War 2. Oh wait, that got split in half."
        elif 350 <= ship_score < 450:
            ship_statement = "Once Astatine works into a stable relationship, so might you two."
        elif 450 <= ship_score < 550:
            ship_statement = "Flip a coin. Thats about how likely it'll work."
        elif 550 <= ship_score < 650:
            ship_statement = "You might work out better than Israel and Palestine! Just maybe though..."
        elif 650 <= ship_score < 750:
            ship_statement = "Two Oxygen atoms look on with jealousy at how well you mesh."
        elif 750 <= ship_score < 850:
            ship_statement = "A binary star wouldn't have the same kind of positive gravity you two would have."
        elif 850 <= ship_score < 950:
            ship_statement = "Rick Astley wouldn't even mesh better with you than that. Thats just downright impressive."
        elif ship_score == 1000:
            ship_statement = "Best. Couple. To. Ever. Exist."
        else:
            ship_statement = "Y'all are **so** good, Schlafly wouldn't call it deceit."
        embed = discord.Embed(title="The Latest Ship is...", color=0xFF0000)
        embed.add_field(name="Ship Name:", value=shipname.capitalize())
        embed.add_field(name="Works like...", value=f'{ship_statement}', inline=False)
        embed.add_field(name="Ship Score:", value=f'{ship_score}',inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/850408868919509004/878825591875448922/awww.png')
        await ctx.send(embed = embed)

    @commands.command(description="The True Information, none of the liberal deceit.", aliases=['cp'])
    async def conservapedia(self, ctx, *, page:str):
        site = page.replace(' ', '_')
        await ctx.send(f"https://conservapedia.com/{site}")

    @conservapedia.error
    async def cperror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide a page for the link.')
            await ctx.send(embed=embed)

    @commands.command(description="Brings you to any desired page on Wikipedia.", aliases=['wikipedia', 'liamsbae'])
    async def wiki(self, ctx, *, page:str):
        site = page.replace(' ', '_')
        await ctx.send(f"https://en.wikipedia.org/wiki/{site}")

    @wiki.error
    async def wikierror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='Error', color=0xFF0000)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/800039486339678250/870443863100248104/XMARKSTHESPOT.png')
            embed.add_field(name="Missing Arguments", value='You must provide a page for the link.')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))