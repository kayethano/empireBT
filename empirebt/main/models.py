from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

User = settings.AUTH_USER_MODEL 

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
	emperor = models.ForeignKey(User, related_name="emperorEmpire")
	name = models.CharField(max_length=255)
	start_date = models.DateTimeField(auto_now_add=True)
	fallen_date = models.DateTimeField()
	supply_points = models.IntegerField(default=200)
	moral = models.IntegerField(default=3)
	summary = models.CharField(max_length=255)
	summary_locked = models.ForeignKey(User, blank=True ,null=True)


class UserCustom(AbstractUser):
	commander = models.ForeignKey(Empire, blank=True, null=True)
	rank = models.CharField(max_length=255, choices=RANK_CHOICES)
	websocket_token = models.CharField(max_length=255)
	supply_points = models.IntegerField(default=0)

class Event(models.Model):
	name = models.CharField(max_length=255)


class EmpireEvent(models.Model):
	is_public = models.BooleanField(default=True)
	event = models.ForeignKey(Event)
	timestamp = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=1024)


class Territory(models.Model):
	name = models.CharField(max_length=255)
	empire = models.ForeignKey(Empire)
	commander = models.ForeignKey(User)
	frontier1 = models.ForeignKey('self', related_name='frontier1Territory')
	frontier2 = models.ForeignKey('self', related_name='frontier2Territory')
	frontier3 = models.ForeignKey('self', related_name='frontier3Territory')
	supply_points = models.IntegerField(default=0)
	sp_points_1mov = models.IntegerField(default=0)
	sp_points_2mov = models.IntegerField(default=0)


class Battle(models.Model):
	attacker = models.ForeignKey(User, related_name='attackerBattle')
	defender = models.ForeignKey(User, related_name='defenderBattle')
	timestamp = models.DateTimeField(auto_now_add=True)
	winner = models.ForeignKey(User, blank=True, null=True, related_name='winnerBattle')
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


class Decision(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	empire = models.ForeignKey(Empire)
	territory = models.ForeignKey(Territory)

class DecisionAttack(Decision):
	commander = models.ForeignKey(User)

class DecisionDefend(Decision):
	commander = models.ForeignKey(User)


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







