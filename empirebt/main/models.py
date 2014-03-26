from django.db import models
from django.contrib.auth.models import User

RANK_CHOICES = ()
END_TYPE_CHOICES = ()
TYPE_ENUM_CHOICES = ()

class Empire(models.Model):
	emperor = models.ForeignKey(User)
	name = models.CharField(max_length=255)
	start_date = models.DateTimeField(auto_add_now=True)
	fallen_date = models.DateTimeField()
	supply_points = models.IntegerField(default=200)
	moral = models.IntegerField(default=3)
	summary = models.CharField(max_length=255)
	summary_locked = models.ForeignKey(User, blank=True ,null=True)


class UserCustom(models.Model):
	user = models.OneToOneField(User)
	commander = models.ForeignKey(Empire)
	rank = models.CharField(max_length=255, choices=RANK_CHOICES)
	supply_points = models.IntegerField(default=0)


class Event(models.Model):
	name = models.CharField(max_length=255)


class EmpireEvent(models.Model):
	is_public = models.BooleanField(default=True)
	event = models.ForeignKey(Event)
	timestamp = models.DateTimeField(auto_add_now=True)
	description = models.CharField(max_length=1024)


class Territory(models.Model):
	name = models.CharField(max_length=255)
	empire = models.ForeignKey(Empire)
	commander = models.ForeignKey(User)
	frontier1 = models.ForeignKey(Territory)
	frontier2 = models.ForeignKey(Territory)
	frontier3 = models.ForeignKey(Territory)
	supply_points = models.IntegerField(default=0)
	sp_points_1mov = models.IntegerField(default=0)
	sp_points_2mov = models.IntegerField(default=0)


class Battle(models.Model):
	attacker = models.ForeignKey(User)
	defender = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_add_now=True)
	winner = models.ForeignKey(User, blank=True, null=True)
	sp_attacker = models.IntegerField()
	sp_defender = models.IntegerField()
	conf_attacker = models.CharField(max_length=1024)
	conf_defender = models.CharField(max_length=1024)
	territory = models.ForeignKey(Territory)
	sp_conceded = models.IntegerField()
	sp_casualities_attacker = models.IntegerField()
	sp_casualities_defender = models.IntegerField()
	end_type = models.CharField(max_length=255, choices=END_TYPE_CHOICES)
	attacker_empire = models.ForeignKey(Empire)
	defender_empire = models.ForeignKey(Empire)


class Decision(models.Model):
	timestamp = models.DateTimeField(auto_add_now=True)
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







