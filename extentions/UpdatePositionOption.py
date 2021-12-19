from api.models import Position,Position_option

class UpdatePositionOption():
	def check(position,type_position):
		try:
			position_option = Position_option.objects.filter(in_position=position).update(status=type_position)
			return True
		except :
			return False

