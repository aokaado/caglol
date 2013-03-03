Smart_select from https://github.com/digi604/django-smart-selects
modified by Andreas Berg Skomedal to include functionality for many to many relationships, by using the additional parameter 'middle'

EG:
class Match(models.Model):
	teamone = ChainedForeignKey(Team, middle='Standings', chained_field='league', chained_model_field='league', show_all=False, auto_choose=True)

 meaning a model named Standings has a many to many relationship between the models Team and Match

NOTE:

 - Won't work with manager, it's even disabled (for now)
 - M2M is not implemented for filter_all, should be easy if neccessary though
 - Assumes the third party m2m class contains fields
 "<model>_id" and field as with original implementation