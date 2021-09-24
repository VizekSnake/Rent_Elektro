import os
import random
import sys
import pytest
from mixer.backend.django import mixer
from faker import Faker
from rentapp.models import Category, Brand, PowerTool

sys.path.append(os.path.dirname(__file__))


@pytest.fixture
def categoryfx(db):
    return Category.objects.create(category="testcategory")


@pytest.fixture
def brandfx(db):
    return Brand.objects.create(name="somebrand")

@pytest.fixture
def conditionfx(db):
    BRANDNEW = 'BN'
    IDEALSHAPE = 'IS'
    GOOD = 'GC'
    USED = 'US'
    HEAVILYUSED = 'HU'

    CONDITION = [
        (BRANDNEW, 'Brand new'),
        (IDEALSHAPE, 'Ideal shape'),
        (GOOD, 'Good condition'),
        (USED, 'Used'),
        (HEAVILYUSED, 'Heavily used')
    ]
    condition = random.choice(CONDITION)
    condition = condition[0]
    return condition


@pytest.fixture
def typefx(db):
    CORDLESSDRILL = 'CD'
    HAMMERDRILL = 'HD'
    IMPACTWRENCH = 'IW'
    ROTARYHAMMER = 'RH'
    IMPACTDRIVER = 'ID'
    ELECTRICSCREWDRIVER = 'ES'
    ROTARYTOOL = 'RT'
    JIGSAW = 'JS'
    RECIPROCATINGSAW = 'RS'
    CIRCULARSAW = 'CS'
    MITERSAW = 'MS'
    BANDSAW = 'BS'
    TABLESAW = 'TS'
    CHAINSAW = 'HS'
    BISCUITJOINER = 'BJ'
    ANGLEGRINDER = 'AG'
    BENCHGRINDER = 'BG'
    SHOPVAC = 'SV'
    BELTSANDER = 'LS'
    RANDOMORBITALSANDER = 'RO'
    DISCSANDER = 'DS'
    WOODROUTER = 'WR'
    NAILGUN = 'NG'
    AIRCOMPRESSOR = 'AC'
    MOISTUREMETER = 'MM'

    TYPE_OF_TOOL = [
        (CORDLESSDRILL, 'Cordless Drill'),
        (IMPACTDRIVER, 'Impact Driver'),
        (HAMMERDRILL, 'Hammer Drill'),
        (ROTARYHAMMER, 'Rotary Hammer'),
        (IMPACTWRENCH, 'Impact Wrench'),
        (ELECTRICSCREWDRIVER, 'Electric Screwdriver'),
        (ROTARYTOOL, 'Rotary Tool'),
        (JIGSAW, 'Jigsaw'),
        (RECIPROCATINGSAW, 'Reciprocating Saw'),
        (CIRCULARSAW, 'Circular Saw'),
        (MITERSAW, 'Miter Saw'),
        (BANDSAW, 'Band Saw'),
        (TABLESAW, 'Table Saw'),
        (CHAINSAW, 'Chainsaw'),
        (BISCUITJOINER, 'Biscuit Joiner'),
        (ANGLEGRINDER, 'Angle Grinder'),
        (BENCHGRINDER, 'Bench Grinder'),
        (SHOPVAC, 'Shop Vac'),
        (BELTSANDER, 'Belt Sander'),
        (RANDOMORBITALSANDER, 'Random Orbital Sander'),
        (DISCSANDER, 'Disc Sander'),
        (WOODROUTER, 'Wood Router'),
        (NAILGUN, 'Nail Gun'),
        (AIRCOMPRESSOR, 'Air Compressor'),
        (MOISTUREMETER, 'Moisture Meter'),
    ]

    type = random.choice(TYPE_OF_TOOL)
    type = type[0]
    return type

