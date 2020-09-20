
				direction = 'leftRotate' if n==0 else 'rightRotate'
				del pa.children[n], leafNode
				pa.children[1-n].children[1-n].color = 'gray'
				self.rotate2(pa, pa.children[1-n],direction)