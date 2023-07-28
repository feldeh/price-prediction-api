from enum import Enum
from pydantic import BaseModel, conint, confloat


class Region(Enum):
    Flanders = 'Flanders'
    Wallonie = 'Wallonie'
    Brussels = 'Brussels'


class BelgianProvinces(Enum):
    Antwerp = 'Antwerp'
    West_Flanders = 'West Flanders'
    Liège = 'Liège'
    East_Flanders = 'East Flanders'
    Luxembourg = 'Luxembourg'
    Flemish_Brabant = 'Flemish Brabant'
    Limburg = 'Limburg'
    Hainaut = 'Hainaut'
    Brussels = 'Brussels'
    Walloon_Brabant = 'Walloon Brabant'
    Namur = 'Namur'


class BelgianDistricts(Enum):
    Turnhout = 'Turnhout'
    Antwerp = 'Antwerp'
    Brugge = 'Brugge'
    Mechelen = 'Mechelen'
    Waremme = 'Waremme'
    Ieper = 'Ieper'
    Oudenaarde = 'Oudenaarde'
    Bastogne = 'Bastogne'
    Sint_Niklaas = 'Sint-Niklaas'
    Halle_Vilvoorde = 'Halle-Vilvoorde'
    Leuven = 'Leuven'
    Tongeren = 'Tongeren'
    Oostende = 'Oostend'
    Ath = 'Ath'
    Charleroi = 'Charleroi'
    Gent = 'Gent'
    Liège = 'Liège'
    Brussels = 'Brussels'
    Dendermonde = 'Dendermonde'
    Maaseik = 'Maaseik'
    Aalst = 'Aalst'
    Veurne = 'Veurne'
    Mouscron = 'Mouscron'
    Nivelles = 'Nivelles'
    Hasselt = 'Hasselt'
    Virton = 'Virton'
    Namur = 'Namur'
    Kortrijk = 'Kortrijk'
    Diksmuide = 'Diksmuide'
    Soignies = 'Soignies'
    Mons = 'Mons'
    Roeselare = 'Roeselare'
    Tournai = 'Tournai'
    Eeklo = 'Eeklo'
    Verviers = 'Verviers'
    Neufchâteau = 'Neufchâteau'
    Thuin = 'Thuin'
    Tielt = 'Tielt'
    Marche_en_Famenne = 'Marche-en-Famenne'
    Philippeville = 'Philippeville'
    Arlon = 'Arlon'
    Huy = 'Huy'
    Dinant = 'Dinant'


class PropertyState(Enum):
    TO_RENOVATE = 'TO_RENOVATE'
    AS_NEW = 'AS_NEW'
    GOOD = 'GOOD'
    JUST_RENOVATED = 'JUST_RENOVATED'
    TO_BE_DONE_UP = 'TO_BE_DONE_UP'


class KitchenState(Enum):
    INSTALLED = 'INSTALLED'
    SUPER_EQUIPPED = 'SUPER_EQUIPPED'
    SEMI_EQUIPPED = 'SEMI_EQUIPPED'
    NOT_INSTALLED = 'NOT_INSTALLED'


class Property(BaseModel):
    region: Region
    province: BelgianProvinces
    district: BelgianDistricts = None
    netHabitableSurface: confloat(gt=10, le=5000)
    bedroomCount: conint(gt=0, le=10)
    hasDoubleGlazing: bool = None
    condition: PropertyState = 'NO_INFO'
    hasSwimmingPool: bool
    bathroomCount: conint(gt=0, le=10)
    showerRoomCount: conint(gt=0, le=10)
    parkingCountIndoor: conint(gt=0, le=10)
    hasGarden: bool
    gardenSurface: confloat(gt=10, le=5000)
    hasTerrace: bool
    hasLift: bool = None
    kitchen: KitchenState = 'NO_INFO'
    latitude: float = None
    longitude: float = None
