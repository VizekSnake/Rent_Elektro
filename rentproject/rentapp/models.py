from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class Brand(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True)
    logo = models.ImageField(default='default.jpg', upload_to='brand_logo')
    history = models.TextField

    def __str__(self):
        return f'{self.name} tools'


class PowerTool(models.Model):
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
    brand = models.ForeignKey(Brand, to_field='name', on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=True)
    power = models.IntegerField(null=False)
    type = models.CharField(max_length=2,
                            choices=TYPE_OF_TOOL, )
    condition = models.CharField(max_length=2,
                                 choices=CONDITION, )
    price = models.SmallIntegerField(null=False)
    deposit = models.SmallIntegerField(null=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tool_img = models.ImageField(default='default.jpg', upload_to='tool_pic')

    def __str__(self):
        return f'{self.brand} {self.type} with power of {self.power} W'

