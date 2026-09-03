def get_direction(horizontal, vertical):
	if horizontal < 0.35:
		return "esquerda"

	if horizontal > 0.65:
		return "direita"

	if vertical < 0.35:
		return "cima"

	if vertical > 0.65:
		return "baixo"

	return "centro"
