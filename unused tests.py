def test():
	def testBinTree():
		tree1 = CompleteBinTreeByLink()
		# seq = list(chr(x+65) for x in range(0, 26))
		seq = list(x for x in range(1, 16))
		tree1.buildFromSeq(seq)
		draw1 = DrawTreeByLink(tree1)
		tree1.append(*(16,17))
		draw1.updateDrawing('append')
		tree1.deleteAndMove()
		draw1.updateDrawing('delete')
		tree1.deleteAndMove(ID = 3)
		draw1.updateDrawing('delete', ID = 3)
		tree1.deleteAndMove(fromID = 6, toID = 14)
		draw1.updateDrawing('delete', fromID = 6, toID = 14)

	def testNormalTree():
		tree1 = CompleteBinTreeByLink()
		seq1 = list(x for x in range(1, 16))
		tree1.buildFromSeq(seq1)
		draw1 = DrawTreeByLink(tree1)

		tree2 = CompleteBinTreeByLink()
		seq2 = list(chr(x+65) for x in range(0, 10))
		tree2.buildFromSeq(seq2)
		draw2 = DrawTreeByLink(tree2)	

		# tree1.insert(13, 30, 'x')
		# draw1.updateDrawing('insert')
		# tree2.insert(6, 31, 'y', ndxInSib = 0)
		# draw2.updateDrawing('insert', insertID = 31)

		tree1.moveToTree(6, tree2, 8)
		draw1.updateDrawing('redraw')
		draw2.updateDrawing('redraw')

		# tree1.insert(11, 32, 'z', ndxInSib = 0)
		# draw1.updateDrawing('insert', insertID = 32)
		# tree1.deleteDown(deleteID = 5)
		# draw1.updateDrawing('deleteDown', lastDeletedIDs = tree1.lastDeletedIDs)

	def testExpTree():
		tree = ExpressionTree()
		expr = '((1-2-4/5*(1/3))+(2+4+3*5)*5)/7'
		# ((1+2-4/5*(1/3))+(2+4+3*5)*5)/7
		# 1,2,+,4,5,/,1,3,/,*,-,2,4,+,3,5,*,+,5,*,+,7,/
		# expr = '1+2*3'
		tree.buildFromExpr(expr)
		draw = DrawTreeByLink(tree)
		draw.updateDrawing('redraw')
		value = tree.evaluate(tree._root)
		print(value)

	def testHeapTree():
		htree = HeapTree()
		# htree.buildFromRandom(10)
		seq = [3, 17, 7, 12, 19, 5, 15, 2, 18, 6]
		htree.buildFromSeq(seq)
		htree.minSort(htree._root)
		draw = DrawTreeByList(htree)
		htree.heapAppend(4)
		draw.updateDrawing('redraw')
		sortedSeq = []
		while htree.size != 0:
			sortedSeq.append(htree.headExtract())
		print(sortedSeq)

	def testBSTree():
		bsTree = BinSearchTree()
		seq = [7, 15, 6, 19, 18, 9, 8, 10, 17, 1, 6, 0, 15, 16, 12]
		seq = [x for x in range(20, 0, -1)]
		bsTree.buildFromSeq(seq)
		bsTree.deleteValue(17)
		bsTree.deleteValue(19)
		seq = bsTree.genSortedSeq()
		print(seq)

	def testAVLTree():
		avlTree = AVLTree()
		# seq = [2, 15, 6, 19, 18, 9, 8, 10, 17, 1, 6, 0, 15, 16, 12]
		seq = [x*2 for x in range(10)]
		avlTree.buildFromSeq(seq)
		avlTree.reshapeAVL()
		draw2 = DrawTreeByLink(avlTree)
		for x in range(21, 29):
			avlTree.insertNodeAVL(x)
		for x in range(-10, 0):
			avlTree.insertNodeAVL(x)
		draw2.updateDrawing('redraw')
		# avlTree.deleteValue(-3)
		# draw2.updateDrawing('redraw')
		for x in range(-3, 3):
			avlTree.deleteValue(x)
			draw2.updateDrawing('redraw')

	def testBMTree():
		btree = BMTree()
		for x in range(13):
			btree.insertValue(x*2)
		draw = DrawTreeByLink(btree)
		btree.insertValue(3)
		draw.updateDrawing('redraw')
		btree.insertValue(5)
		draw.updateDrawing('redraw')

		# print(btree)

	# testBinTree()
	# testNormalTree()
	# testExpTree()
	# testHeapTree()
	# testBSTree()
	# testAVLTree()
	# testBMTree()

	def testRBTree():
		rbTree = RBTree()
		# seq = [randint(0,100) for x in range(23)]
		# seq = [18, 9, 8, 2, 15, 6, 19]
		# seq = [2, 6, 19, 16, 10, 22, 18,17]
		seq = [56, 79, 35, 64, 46, 85, 53, 94, 27, 25, 4, 45, 91, 100, 98, 80, 97, 83, 9, 62, 48, 96, 24]
		seq2 = [163, 118, 147, 164, 119, 117, 121, 158, 126, 165, 196, 191, 163, 177, 109, 187, 135, 172, 164, 139]
		seq += seq2
		for x in seq:
			rbTree.insertValue(x)
		draw1 = DrawTreeByLink(rbTree)
		# # rbTree.insert(17)
		rbTree.deleteValue(45)
		rbTree.deleteValue(46)
		rbTree.deleteValue(9)
		rbTree.deleteValue(24)
		rbTree.deleteValue(35)
		rbTree.deleteValue(53)
		rbTree.deleteValue(4)
		draw1.updateDrawing('redraw')
		rbTree.deleteValue(119)
		draw1.updateDrawing('redraw')
		rbTree.deleteValue(121)
		rbTree.deleteValue(126)
		rbTree.deleteValue(27)
		draw1.updateDrawing('redraw')