import os
import string
import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver



def generate_random_string(length, stringset=string.ascii_letters+string.digits+string.punctuation):
    '''
    Returns a string with `length` characters chosen from `stringset`
    >>> len(generate_random_string(20) == 20 
    '''
    token = ''.join([stringset[i%len(stringset)] \
        for i in [ord(x) for x in os.urandom(length)]])

    return hashlib.sha256(token).hexdigest()[:64]


RANK_CHOICES = (
	(0,'Emperor'),
	(1,'General'),
	(2,'Colonel'),
	(3,'Major'),
	(4,'Captain'),
	(5,'Lieutenant'),
	)

END_TYPE_CHOICES = (
	(0, 'Surender'),
	(1, 'Timeout'),
	(2, 'Victory'),
	(3, 'Domination'),
	(4, 'Disconnection'),
	(5, 'Draw'),
	)

TYPE_ENUM_CHOICES = (
	(0, 'Pro'),
	(1, 'Con')
	)

class Empire(models.Model):
	emperor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="emperorEmpire")
	name = models.CharField(max_length=255, blank=True, null=True)
	start_date = models.DateTimeField(auto_now_add=True)
	fallen_date = models.DateTimeField(blank=True, null=True)
	supply_points = models.IntegerField(default=200)
	moral = models.IntegerField(default=3)
	summary = models.CharField(max_length=255, blank=True, null=True)
	summary_locked = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True ,null=True, related_name="summary_lockedEmpire")
	decision_locked = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='decision_lockedEmpire')

	def __unicode__(self):
		return u'%s' % self.emperor

	def create_user_empire(sender, instance, created, **kwargs):
		if created:
			Empire.objects.create(emperor=instance)

	#Signal to create when new empire 
	post_save.connect(create_user_empire, sender=settings.AUTH_USER_MODEL)


class UserCustom(AbstractUser):
	empire = models.ForeignKey(Empire, blank=True, null=True)
	rank = models.CharField(max_length=255, choices=RANK_CHOICES)
	websocket_token = models.CharField(max_length=255, default=generate_random_string(64))
	supply_points = models.IntegerField(default=0)
	chat_empire_connected = models.BooleanField(default=False)
	chat_oneonone_connected = models.BooleanField(default=False)


class Event(models.Model):
	name = models.CharField(max_length=255)

	def __unicode__(self):
		return u'%s' % self.name


class EmpireEvent(models.Model):
	is_public = models.BooleanField(default=True)
	event = models.ForeignKey(Event)
	timestamp = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=1024)

	def __unicode__(self):
		return u'%s' % self.event


class Territory(models.Model):
	name = models.CharField(max_length=255)
	empire = models.ForeignKey(Empire)
	commander = models.ForeignKey(settings.AUTH_USER_MODEL)
	frontier1 = models.ForeignKey('self', related_name='frontier1Territory')
	frontier2 = models.ForeignKey('self', related_name='frontier2Territory')
	frontier3 = models.ForeignKey('self', related_name='frontier3Territory')
	supply_points = models.IntegerField(default=0)
	sp_points_1mov = models.IntegerField(default=0)
	sp_points_2mov = models.IntegerField(default=0)

	def __unicode__(self):
		return u'%s' % self.name


class Battle(models.Model):
	attacker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='attackerBattle')
	defender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='defenderBattle')
	timestamp = models.DateTimeField(auto_now_add=True)
	winner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='winnerBattle')
	sp_attacker = models.IntegerField()
	sp_defender = models.IntegerField()
	conf_attacker = models.CharField(max_length=1024)
	conf_defender = models.CharField(max_length=1024)
	territory = models.ForeignKey(Territory, related_name='territoryBattle')
	sp_conceded = models.IntegerField()
	sp_casualities_attacker = models.IntegerField()
	sp_casualities_defender = models.IntegerField()
	end_type = models.CharField(max_length=255, choices=END_TYPE_CHOICES)
	attacker_empire = models.ForeignKey(Empire, related_name='attacker_empireBattle')
	defender_empire = models.ForeignKey(Empire, related_name='defender_empireBattle')

	def __unicode__(self):
		return u'Attacker: %s Defender %s' % (self.attacker, self.defender)


class Decision(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	empire = models.ForeignKey(Empire)
	territory = models.ForeignKey(Territory)

	def __unicode__(self):
		return u'Empire %s Territory %s' % (self.empire, self.territory)


class DecisionAttack(Decision):
	commander = models.ForeignKey(settings.AUTH_USER_MODEL)

class DecisionDefend(Decision):
	commander = models.ForeignKey(settings.AUTH_USER_MODEL)


class DecisionMove(Decision):
	territory_destination = models.ForeignKey(Territory)
	supply_points = models.IntegerField()


class DecisionEvaluation(models.Model):
	type_enum = models.CharField(max_length=255, choices=TYPE_ENUM_CHOICES)
	description = models.CharField(max_length=255)


class DecisionEvaluationAtack(DecisionEvaluation):
	decision_attack = models.ForeignKey(DecisionAttack)


class DecisionEvaluationDefend(DecisionEvaluation):
	decision_defend = models.ForeignKey(DecisionDefend)


class DecisionEvaluationMove(DecisionEvaluation):
	decision_move = models.ForeignKey(DecisionMove)







