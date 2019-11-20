import sys
import re
import textwrap

class Tokenizer:

	def __init__(self):
		# Document Standards
		self.paperWidth = 793.7
		self.paperHeight = 1122.5
		self.paperMarginLeft = 20
		self.paperMarginRight = 20
		self.paperMarginTop = 20
		self.paperMarginBottom = 20
		self.paperBodyWidth = self.paperWidth - (self.paperMarginLeft + self.paperMarginRight)
		self.paperBodyHeight = self.paperHeight - (self.paperMarginTop + self.paperMarginBottom)
		self.fontSize = 11
		self.fontSpacing = '1.2em'
		self.fontFamily = 'Times New Roman'
		self.blankSpace = '‏‏‎ '
		self.tabSpace = '‏‏‎ ‏‏‎ ‏‏‎ ‏‏‎ '

		self.lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. "

		self.tokens = [] # List of all tokens created

	# Take a document and process it into segments and then pass it to the tokenizer
	def lex(self, document, filename):
		segments = list(document) # List out the document into segments

		# Loop through each segment in the list and pass it to the tokenizer
		for segment in segments: 
			self.tokenize(segment) # Pass segments to tokenizer

		#self.debug(self.tokens)
		self.write(filename)
	
	# Take each segment and break it down and find each key and make them in to tokens
	def tokenize(self, segment):

		# Heading Standard
		if re.findall(r'(HS)([1-6])(.*?)$', segment):
			for t in re.findall(r'(HS)([1-6])(.*?)$', segment):
				heading = self.headingSize(t[1])
				segment = re.sub(r'(HS)([1-6])(.*?)$', 
				self.tag('tspan', t[2].strip(), fontSize = heading[0], x = self.paperMarginLeft, dy = heading[1]), 
				segment)

		# Heading Underlined
		if re.findall(r'(HU)([1-6])(.*?)$', segment):
			for t in re.findall(r'(HU)([1-6])(.*?)$', segment):
				heading = self.headingSize(t[1])
				segment = re.sub(r'(HU)([1-6])(.*?)$', 
				self.tag('tspan', t[2].strip(), fontSize = heading[0], x = self.paperMarginLeft, dy = heading[1], textDecoration = "underline"),
				segment)
		
		# Title Standard
		if re.findall(r'(TS)([1-6])(.*?)$', segment):
			for t in re.findall(r'(TS)([1-6])(.*?)$', segment):
				heading = self.headingSize(t[1])
				segment = re.sub(r'(TS)([1-6])(.*?)$', 
				self.tag('tspan', t[2].strip(), fontSize = heading[0], x = "50%", dy = heading[1], textAnchor = "middle"), 
				segment)

		# Title Underlined
		if re.findall(r'(TU)([1-6])(.*?)$', segment):
			for t in re.findall(r'(TU)([1-6])(.*?)$', segment):
				heading = self.headingSize(t[1])
				segment = re.sub(r'(TU)([1-6])(.*?)$', 
				self.tag('tspan', t[2].strip(), fontSize = heading[0], x = "50%", dy = heading[1], textAnchor = "middle", textDecoration = "underline"), 
				segment)

		# Introduction
		if re.findall(r'(IN)([1-4])(.*?)$', segment):
			for t in re.findall(r'(IN)([1-4])(.*?)$', segment):
				if t[1] == "2":
					segment = re.sub(r'(IN)([1-4])(.*?)$',
					self.tag('tspan', t[2].strip(), fontSize = 20, x = "50%", dy = "1.6em", textAnchor = "middle", textDecoration = "underline", fontStyle = "italic"), 
					segment)
				if t[1] == "3":
					segment = re.sub(r'(IN)([1-4])(.*?)$',
					self.tag('tspan', t[2].strip(), fontSize = 15, x = "50%", dy = "1.8em", textAnchor = "middle", fontStyle = "italic"), 
					segment)
				else:
					heading = self.headingSize(t[1])
					segment = re.sub(r'(IN)([1-4])(.*?)$',
					self.tag('tspan', t[2].strip(), fontSize = heading[0], x = "50%", dy = heading[1], textAnchor = "middle"), 
					segment)

		# Paragraph Standard
		if re.findall(r'(PS)([0-9]*)(.*?)$', segment):
			for t in re.findall(r'(PS)([0-9]*)(.*?)$', segment):
				segment = re.sub(r'(PS)([0-9]*)(.*?)$', '', segment)
				if t[1] == '':
					size = self.fontSize
				else:
					size = t[1]

				self.wordWrap(t[2].strip(), size)

		# Paragraph Leading
		if re.findall(r'(PL)([0-9]*)(.*?)$', segment):
			for t in re.findall(r'(PL)([0-9]*)(.*?)$', segment):
				segment = re.sub(r'(PL)([0-9]*)(.*?)$', '', segment)
				if t[1] == '':
					size = self.fontSize
				else:
					size = t[1]

				self.wordWrap(t[2], size, True)

		# Blank Space Fixed and Adjustable
		if re.findall(r'(SP)([0-9]*)', segment):
			for t in re.findall(r'(SP)([0-9]*)', segment):
				if t[1] == '':
					spacing = '1.2em'
				else:
					spacing = t[1]
				
				segment = re.sub(r'(SP)([0-9]*)', self.tag('tspan', self.blankSpace, dy = f'{spacing}em'), segment)

		# Bold
		if re.findall(r'\*\*(.*?)\*\*', segment):
			for t in re.findall(r'\*\*(.*?)\*\*', segment):
				print(t)
				segment = re.sub(r'\*\*(.*?)\*\*', 
				self.tag('tspan', t, fontWeight = "bold", space = "preserve"),
				segment)

		self.tokens.append(segment.strip('\n').strip('\t')) # Clean new line and tabs from tokens

	## Debug Function ## 
	def debug(self, tokens):
		for token in tokens:
			print(token)

	# XML Tag generator
	def tag(self, name, *content, 
		fontSize = None,
		fontStyle = None,
		fontWeight = None,
		textAnchor = None,
		textDecoration = None,
		space = None,
		**attrs):

		if fontSize is not None: attrs['font-size'] = fontSize
		if fontStyle is not None: attrs['font-style'] = fontStyle		
		if fontWeight is not None: attrs['font-weight'] = fontWeight
		if textAnchor is not None: attrs['text-anchor'] = textAnchor	
		if textDecoration is not None: attrs['text-decoration'] = textDecoration
		if space is not None: attrs['xml:space'] = space

		if attrs:
			attr_str = ''.join(f' {attr}="{value}"'
						for attr, value in
						sorted(attrs.items()))
		else:
			attr_str = ''
		
		if content:
			return '\n'.join(f'<{name}{attr_str}>{c}</{name}>'
					for c in content)
		else:
			return f'<{name}{attr_str} />'

	# Heading Size Assignment
	def headingSize(self, heading):
		if heading == '1':
			size = 35
			spacing = "1.5em"
		elif heading == '2':
			size = 30
			spacing = "1.2em"
		elif heading == '3':
			size = 25
			spacing = "1.4em"
		elif heading == '4':
			size = 20
			spacing = "1.6em"
		elif heading == '5':
			size = 15
			spacing = "1.8em"
		elif heading == '6':
			size = 10
			spacing = "2"
		
		return [size, spacing]

	# Word Wrap
	def wordWrap(self, text, size, tab = False):
		wrapPoint = (self.paperBodyWidth / (int(size) / 2.5) )
		wrapper = textwrap.TextWrapper(width = int(wrapPoint))
		if tab != False:
			text = '\n\n\n\n\n\n\n\n' + text
		wrappedText = wrapper.wrap(text=text)
		count = len(wrappedText)
		for segment in wrappedText:
			if count == len(wrappedText):
				spacing = '2em'
			else:
				spacing = self.fontSpacing
			
			if count > 1:
				textLength = self.paperBodyWidth
			else:
				textLength = ""

			#self.tokens.append(self.tag('tspan', segment, fontSize = size, x = self.paperMarginLeft, dy = spacing, space = "preserve", textLength = textLength))
			token = self.tag('tspan', segment, fontSize = size, x = self.paperMarginLeft, dy = spacing, space = "preserve", textLength = textLength)
			self.tokenize(token)
			count -= 1

	# Write Document
	def write(self, filename):
		# Create File
		c = open(f'{filename}.svg', 'w+')
		c.write('')
		c.close()

		# Document
		f = open(f'{filename}.svg', 'a+')
		f.write('<?xml version="1.2" encoding="utf-8" ?>\n')
		f.write(f'<svg version="1.2" baseProfile="tiny" height="{self.paperHeight}" width="{self.paperWidth}" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">\n')
		f.write('<defs />\n')
		f.write('<rect fill="white" height="100%" width="100%" x="0" y="0" />\n')
		f.write('<rect fill="white" height="1082.5" stroke="rgb(10%,10%,16%)" width="753.7" x="20" y="20" />\n')
		f.write(f'<g font-family="{self.fontFamily}" font-size="{self.fontSize}">\n')
		f.write(f'<text x="50" y="{self.paperMarginTop}" dy="0">\n')

		for token in self.tokens:
			f.write(f'{token}\n')
		
		f.write('</text>\n')
		f.write('</g>\n')
		f.write('</svg>')
		f.close()


lexer = Tokenizer()

def main():
	document = open(sys.argv[1] + '.zm')
	lexer.lex(document, sys.argv[1])

if __name__ == "__main__":
	main()
