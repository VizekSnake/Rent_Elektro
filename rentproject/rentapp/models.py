from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Max


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}'


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Brand(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True)
    logo = models.ImageField(default='/brand_pic/default.jpg', upload_to='brand_logo')
    history = models.TextField

    def __str__(self):
        return f'{self.name} tools'


class Category(models.Model):
    category = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.category} '


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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tool_img = models.ImageField(default='/tool_pic/default.jpg', upload_to='tool_pic')
    category = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.brand} {self.get_type_display()} with power of {self.power} W'


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_message(from_user, to_user, body):
        sender_message = Message(
            user=from_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            is_read=True)
        sender_message.save()

        recipient_message = Message(
            user=to_user,
            sender=from_user,
            body=body,
            recipient=from_user, )
        recipient_message.save()
        return sender_message

    def get_messages(user):
        messages = Message.objects.filter(user=user).values('recipient').annotate(last=Max('date')).order_by(
            '-last')
        users = []
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['recipient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'],
                                                 is_read=False).count()
            })
        return users


class RentToolProposition(models.Model):
    from_date = models.DateField()
    to_date = models.DateField()
    by_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tool = models.ForeignKey(PowerTool, on_delete=models.CASCADE)
    accepted_by_owner = models.BooleanField(default=False)
    reservation_to_acceptation = models.BooleanField(default=False)
    rented = models.BooleanField(default=False)
    isread = models.BooleanField(default=False)
    rent_price = models.IntegerField(null=True)
    rejected = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    tool_owner_view = models.BooleanField(default=True)
    by_user_view = models.BooleanField(default=True)
    by_user_return = models.BooleanField(default=False)
    tool_owner_return = models.BooleanField(default=False)


    def __str__(self):
        return f'Proposition of rent :{self.tool} from {self.by_user}'
