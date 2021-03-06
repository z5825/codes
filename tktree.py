import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mbox

import win32api,win32con

class BiTreeForTreeviewTTK(object):
	def __init__(self, items):
		self.master = tk.Tk()
		self.items = items

		tree = ttk.Treeview(height = len(self.items), show = 'tree')
		tree.column('#0', width = 400)
		assert len(self.items) > 0, 'the tree shall not be empty.'
		tree.insert('', 0, items[0], text = items[0])
		for i in range(1, len(items)):
			tree.insert(items[(i-1)//2], i, items[i], text = items[i])
			tree.see(items[i])
		tree.pack()

	def mainloop(self):
		self.master.mainloop()

class DrawTreeByLink(object):
	def __init__(self, tree):
		self.tree = tree
		self._initTreeSize = self.tree.width, self.tree.height
		self.root = tk.Tk()

		self.step = tk.IntVar(master = self.root, value = 0)

		self.fmCanvas = tk.Frame(self.root)
		self.fmVerBar = tk.Frame(self.fmCanvas)
		self.fmHorBar = tk.Frame(self.fmCanvas)
		self.fmForButtons = tk.Frame(self.root)

		self.fmForButtons.pack(side = 'top', fill = 'both', expand = True)
		self.fmCanvas.pack(side = 'top', fill = 'both', expand = True)
		self.fmVerBar.pack(side = 'right', fill = 'both', expand = False)
		self.fmHorBar.pack(side = 'bottom', fill = 'both', expand = False)

		self.bt1 = tk.Button(self.fmForButtons, text = '   next   ', command = lambda: self.step.set(self.step.get()+1))
		self.bt2 = tk.Button(self.fmForButtons, text = 'button-2')
		self.bt1.pack(side = 'left')
		self.bt2.pack(side = 'left')
		
		cx = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
		cy = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
		# cx, cy = 1440, 900
		self.baseSize = 25 * cx/1440
		self.zoomX, self.zoomY = 2 + self.tree.width//20 * cx/1440, 1.5 + self.tree.height//12 * cy/720
		self.root.geometry('%dx%d+%d+%d' %(cx*self.zoomX*0.2, cy*self.zoomY*0.2,cx*0.4, cy*0.5))

		self._drawCanvas()
		self._drawNodesAndLines(fromNode = self.tree._root, toNode = self.tree._last)
		self.bt1.waitvar(self.step)

	def _drawCanvas(self):
		self.canvasWidth = self.baseSize * self.tree.width * self.zoomX 
		self.canvasHeight = self.baseSize * (self.tree.height + 1)* self.zoomY
		self.offset = self.baseSize // 1.5
		self.cv = tk.Canvas(self.fmCanvas, width = self.canvasWidth, height = self.canvasHeight, \
							borderwidth = 3, relief = 'ridge')
		self.cv.pack(side = 'left', fill = 'both', expand = True)

		self.verBar = tk.Scrollbar(self.fmVerBar, width = 20)
		self.verBar.pack(side = 'right', fill = 'both', expand = False)
		self.horBar = tk.Scrollbar(self.fmHorBar, orient = 'horizontal', width = 20)
		self.horBar.pack(side = 'bottom', fill = 'both', expand = False)
		self.horBar.config(command = self.cv.xview)
		self.verBar.config(command = self.cv.yview)
		self.cv.config(yscrollcommand = self.verBar.set, xscrollcommand = self.horBar.set, 
					scrollregion = (0, 0, self.canvasWidth, self.canvasHeight))

	def _recMinDrawWidth(self, node, contentLength, scale):
		if len(node.validChildren) == 0:
			return self.baseSize * contentLength * scale
		else:
			sumWidth = 0
			for ch in node.validChildren.values():
				sumWidth += self._recMinDrawWidth(ch, contentLength, scale)
			return sumWidth 

	def _drawNodesAndLines(self, **kw):
		drawList = []
		fromNode = toNode = None
		if 'fromNode' in kw and 'toNode' in kw:
			fromNode, toNode = kw['fromNode'], kw['toNode']
			curNode = fromNode
			while curNode != toNode.next:
				drawList.append(curNode) 
				curNode = curNode.next
		elif 'fromID' in kw and 'toID' in kw:
			fromNode, toNode = self.tree.idDict[kw['fromID']], self.tree.idDict[kw['toID']]
			curNode = fromNode
			while curNode != toNode.next:
				drawList.append(curNode) 
				curNode = curNode.next
		elif 'downFromNode' in kw:
			self.tree._updateDesendants(kw['downFromNode'])
			drawList = kw['downFromNode'].descendants
		else:
			mbox.showerror('', 'nothing drawed.')
			return

		# draw nodes:
		for curNode in drawList:
			if isinstance(curNode.children, dict):
				contentLength = 1 
			if hasattr(curNode, 'size'): 
				contentLength *= 1.5
			if hasattr(curNode, 'rank'): 
				contentLength *= 1.5
			elif isinstance(curNode.children, list):
				contentLength = max(1, len(curNode.content)) 
			if curNode.level == 1:
				curNode.centerXY = [0.5 * self.canvasWidth, self.offset]
				curNode.drawWidth = self.canvasWidth
				scale = 1.5 if self.tree.width < 8 else 1.2
				curNode.drawRect = [[curNode.centerXY[0] - self.baseSize * contentLength * 0.5 * scale, \
									curNode.centerXY[1] - self.offset * 0.5 * scale],\
									[curNode.centerXY[0] + self.baseSize * contentLength * 0.5 * scale, \
									curNode.centerXY[1] + self.offset * 0.5 * scale]]
			else:
				countOfCh = len(curNode.parent.validChildren)
				curNode.drawWidth = max(self._recMinDrawWidth(curNode, contentLength, scale), \
										curNode.parent.drawWidth/min(2, countOfCh))
				curNode.centerXY = [curNode.parent.centerXY[0] - 1/2 * curNode.parent.drawWidth + \
								(0.5 + curNode.ndxInSib) * curNode.drawWidth, \
								(curNode.level-1)*self.baseSize*self.zoomY + self.offset]
				curNode.drawRect = [[curNode.centerXY[0] - self.baseSize * contentLength * 0.5 * scale, \
									curNode.centerXY[1] - self.offset * 0.5 * scale],\
									[curNode.centerXY[0] + self.baseSize * contentLength * 0.5 * scale, \
									curNode.centerXY[1] + self.offset * 0.5 * scale]]
		
		# to adjust the position of overlayed nodes:
		lMark = rMark = self.tree._last
		while lMark is not None:
			while lMark is not None and lMark.level == rMark.level:
				lMark = lMark.prev
			
			# loop: to move a node to the centerX of its children
			if	lMark is not None: 
				curNode = lMark.next
			else: curNode = self.tree._root
			while curNode != rMark.next:
				if len(curNode.validChildren) > 1:
					x = 0
					if isinstance(curNode.children, dict):
						tmpList = curNode.validChildren.values()
					elif isinstance(curNode.children, list):
						tmpList = curNode.validChildren
					for ch in tmpList:
						x += ch.centerXY[0]
					xMove = x/len(curNode.validChildren) - curNode.centerXY[0]
				elif 0 in curNode.validChildren:
					xMove = curNode.children[0].centerXY[0] + curNode.drawWidth/2 - curNode.centerXY[0]
				elif 1 in curNode.validChildren:
					xMove = curNode.children[1].centerXY[0] - curNode.drawWidth/2 - curNode.centerXY[0]
				elif len(curNode.children) == 1 and isinstance(curNode.children, list):  # for case of 23Tree, etc.
					xMove = curNode.children[0].centerXY[0] + curNode.children[0].drawWidth/2 - curNode.centerXY[0]
				else: 
					xMove = 0
				curNode.drawRect[0][0] += xMove
				curNode.drawRect[1][0] += xMove
				curNode.centerXY[0] += xMove
				curNode = curNode.next

			# loop: to right move node and its sons if it enters the prev node's right bound
			if	lMark is not None: 
				curNode = lMark.next
			else: curNode = self.tree._root
			while curNode != rMark: 
				nextNode = curNode.next
				rBound, lBound = curNode.centerXY[0] + curNode.drawWidth/2, \
								nextNode.centerXY[0] - nextNode.drawWidth/2
				if lBound < rBound:
					xMove = rBound - lBound 
					self.tree._updateDesendants(nextNode)
					for node in [nextNode] + nextNode.descendants:
						node.drawRect[0][0] += xMove
						node.drawRect[1][0] += xMove
						node.centerXY[0] += xMove
				curNode = nextNode
			rMark = lMark

		for curNode in drawList:
			(x1, y1), (x2, y2) = curNode.drawRect
			tmpTag = ('nodes', 'node'+str(curNode.nodeID))
			self.cv.create_oval(x1, y1, x2, y2, fill = curNode.color, tag = tmpTag)
			txt = str(curNode.content)
			if hasattr(curNode, 'size'):
				txt += ' s:' + str(curNode.size)
			if hasattr(curNode, 'rank'):
				txt += ' r:' + str(curNode.rank)
			if isinstance(curNode.content, list):
				txt = str()
				for x in curNode.content:
					txt += str(x) + ', ' 
				txt = txt.rstrip(', ')
			self.cv.create_text(curNode.centerXY[0], curNode.centerXY[1], text = txt, tag = tmpTag)

		#draw lines:
		for curNode in drawList:
			if isinstance(curNode.children, dict):
				tmpList = curNode.validChildren.values()
			elif isinstance(curNode.children, list):
				tmpList = curNode.children
			for ch in tmpList:
				tmpTag = ('lines', str(curNode.nodeID) + '->', '->'+ str(ch.nodeID))
				self.cv.create_line(curNode.centerXY[0], curNode.centerXY[1], ch.centerXY[0], ch.centerXY[1], \
									width = 2, fill = 'black', tag = tmpTag)

		#draw cousin lines:
		for curNode in drawList:
			if curNode.lCou is not None:
				x1, y1, x2, y2 = curNode.centerXY[0] + self.offset, curNode.centerXY[1] + self.offset, \
						curNode.lCou.centerXY[0] + self.offset, curNode.lCou.centerXY[1] + self.offset
				tmpTag = ('lines', str(curNode.nodeID) + '->', '->'+ str(curNode.lCou.nodeID))
				self.cv.create_line(x1, y1, x2, y2, width = 2, fill = 'green', tag = tmpTag)
			if curNode.rCou is not None:
				x1, y1, x2, y2 = curNode.centerXY[0] + self.offset, curNode.centerXY[1] + self.offset, \
						curNode.rCou.centerXY[0] + self.offset, curNode.rCou.centerXY[1] + self.offset
				tmpTag = ('lines', str(curNode.nodeID) + '->', '->'+ str(curNode.rCou.nodeID))
				self.cv.create_line(x1, y1, x2, y2, width = 2, fill = 'green', tag = tmpTag)

		self.cv.lift('nodes')
		self._lastDrawNode = drawList[-1]

	def _deleteNodeAndLines(self, **kw):
		'''kw: deleteAll, downFromNode, fromID/toID, lastDeletedIDs '''
		if 'deleteAll' in kw:
			self.cv.destroy()
			self._drawCanvas()
		elif 'downFromNode' in kw:
			self.tree._updateDesendants(kw['downFromNode'])
			for node in kw['downFromNode'].descendants:
				tmpTag = 'node'+str(node.nodeID), str(node.nodeID)+'->', '->'+str(node.nodeID)
				self.cv.delete(*tmpTag)
		elif 'fromID' in kw and 'toID' in kw:
			fromID, toID = kw['fromID'], kw['toID']
			endID = max(self._lastDrawNode.nodeID, toID)
			for id in range(fromID, endID + 1):
				tmpTag = 'node'+str(id), str(id)+'->', '->'+str(id)
				self.cv.delete(*tmpTag)
			# mbox.showinfo('', 'deleted')
			if (toID + 1) in self.tree.idDict and self.tree.idDict[toID + 1] is not None:
				updateFromNode = self.tree.idDict[toID + 1]
				self._drawNodesAndLines(fromNode = updateFromNode, toNode = self.tree._last)
			else:
				self._lastDrawNode = self.tree._last
		elif 'lastDeletedIDs' in kw:
			for id in kw['lastDeletedIDs']:
				tmpTag = 'node'+str(id), str(id)+'->', '->'+str(id)
				self.cv.delete(*tmpTag)
		# mbox.showinfo('', 'drawed')

	def updateDrawing(self, operation, **kw):
		'''operation: 'append', 'delete', 'insert', 'redraw'. kw: fromID, toID, ID, fromNode, toNode, node, insertID  '''
		if operation == 'append':
			mbox.showinfo('', 'appending:')
			if self._lastDrawNode.next is None:
				mbox.showinfo('', 'nothing appended.')
			else:
				if self._initTreeSize == (self.tree.width, self.tree.height):
					self._drawNodesAndLines(fromNode = self._lastDrawNode.next, toNode = self.tree._last)
				else: 
					self._redraw()
			mbox.showinfo('', 'appended')
		if operation == 'delete':
			''' args is the same to delete in tree class. '''
			if 'fromID' in kw and 'toID' in kw:
				mbox.showinfo('', ('delete:', kw['fromID'], kw['toID']))
			elif 'ID' in kw:
				mbox.showinfo('', ('delete:', kw['ID']))
			else:
				mbox.showinfo('', 'delete last')
			if self._lastDrawNode == self.tree._last:
				mbox.showinfo('', 'nothing deleted.')
			else:
				fromNode = toNode = self._lastDrawNode
				fromID, toID = fromNode.nodeID, toNode.nodeID
				if 'node' in kw:
					fromID = toID = kw['node'].nodeID
				elif 'ID' in kw:
					fromID = toID = kw['ID']
				if 'fromNode' in kw and 'toNode' in kw:
					fromID, toID = kw['fromNode'].nodeID, kw['toNode'].nodeID
				elif 'fromID' in kw and 'toID' in kw:
					fromID, toID = kw['fromID'], kw['toID']
				assert fromID is not None and toID is not None, 'error 404'
				self._deleteNodeAndLines(fromID = fromID, toID = toID)
		if operation == 'insert':
			if self._initTreeSize != (self.tree.width, self.tree.height):
					self._redraw()
					mbox.showinfo('', 'inserted')
			else:
				if 'insertID' in kw:
					insertID = kw['insertID']
					self._deleteNodeAndLines(downFromNode = self.tree.idDict[insertID].parent)
					self._drawNodesAndLines(downFromNode = self.tree.idDict[insertID].parent)
				else:
					self._deleteNodeAndLines(deleteAll = True)
					self._drawNodesAndLines(fromNode = self.tree._root, toNode = self.tree._last)
				mbox.showinfo('', 'inserted')
		if operation == 'deleteDown':
			if 'lastDeletedIDs' in kw:
				self._deleteNodeAndLines(lastDeletedIDs = kw['lastDeletedIDs'])
				mbox.showinfo('', 'delete down:')
		if operation == 'redraw':
			self._redraw()
		
	def _redraw(self):
		self._initTreeSize = (self.tree.width, self.tree.height)
		self.root.destroy()
		self.__init__(self.tree)
		# self._drawCanvas()
		# self._drawNodesAndLines(fromNode = self.tree._root, toNode = self.tree._last)
		# mbox.showinfo('',('redrawed', self.tree.size))
		# self.root.mainloop()

class DrawTreeByList(DrawTreeByLink):
	def __init__(self, tree):
		super().__init__(tree)
	
	def _drawNodesAndLines(self, **kw):
		# draw nodes:
		for curNode in self.tree:
			if curNode.level == 1:
				curNode.centerXY = 0.5 * self.canvasWidth, self.offset
				curNode.drawWidth = self.canvasWidth
			else:
				w1 = curNode.parent.drawWidth
				if isinstance(curNode.parent.children, dict):
					w2 = curNode.drawWidth = w1 / (1 + max(curNode.parent.children.keys()))
				elif isinstance(curNode.parent.children, list):
					w2 = curNode.drawWidth = w1 / (1 + len(curNode.parent.children)) 
				curNode.centerXY = curNode.parent.centerXY[0] - 1/2 * w1 + (1/2 + curNode.ndxInSib) * w2, \
								(curNode.level-1)*self.baseSize*self.zoomY + self.offset
			x1, y1 = curNode.centerXY
			x2, y2 = x1 + self.baseSize, y1 + self.baseSize
			tmpTag = ('nodes', 'node'+str(curNode.nodeID))
			self.cv.create_oval(x1, y1, x2, y2, fill = 'white', tag = tmpTag)
			self.cv.create_text(x1 + self.offset, y1 + self.offset, text = curNode.content, tag = tmpTag)

		#draw lines:
		for curNode in self.tree:
			if isinstance(curNode.children, dict):
				tmpList = curNode.children.values()
			elif isinstance(curNode.children, list):
				tmpList = curNode.children
			for ch in tmpList:
				x1, y1, x2, y2 = curNode.centerXY[0] + self.offset, curNode.centerXY[1] + self.offset,  \
					ch.centerXY[0] + self.offset, ch.centerXY[1] + self.offset
				tmpTag = ('lines', str(curNode.nodeID) + '->', '->'+ str(ch.nodeID))
				self.cv.create_line(x1, y1, x2, y2, width = 3, fill = 'red', tag = tmpTag)
			if curNode.parent is not None:   # to draw for newly added nodes.
				tmpTag = ('lines', str(curNode.parent.nodeID) + '->', '->' + str(curNode.nodeID))
				if self.cv.find('withtag', tmpTag) == ():
					parentXY = curNode.parent.centerXY[0] + self.offset, curNode.parent.centerXY[1] + self.offset
					x1, y1, x2, y2 =  parentXY[0], parentXY[1], 	\
						curNode.centerXY[0] + self.offset, curNode.centerXY[1] + self.offset
					self.cv.create_line(x1, y1, x2, y2, width = 3, fill = 'red', tag = tmpTag)					

		self.cv.lift('nodes')
		mbox.showinfo('','drawed')












