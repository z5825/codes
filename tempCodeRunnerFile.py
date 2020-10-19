	def insertValue(self, value):
		toUpdate = super().insertValue(value)
		self._getSize(toUpdate)

	def deleteValue(self, value):
		toUpdate = super().deleteValue(value)
		if toUpdate is not None:
			self._getSize(toUpdate)