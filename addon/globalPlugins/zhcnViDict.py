# -*- coding: utf-8 -*-
# Chinese-Vietnamese Dictionary Global Plugin for NVDA
# Uses custom speech processing with multi-value dictionary

import globalPluginHandler
import speech.speech
import tones
import os
import addonHandler
import logHandler

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Punctuation mapping - Standardize to Latin + Space
	PUNCT_MAP = {
		'。': '. ',
		'，': ', ',
		'、': ', ',
		'；': '; ',
		'：': ': ',
		'！': '! ',
		'？': '? ',
		'“': '"',
		'”': '"',
		'‘': "'",
		'’': "'",
		'（': ' (',
		'）': ') ',
		'【': ' [',
		'】': '] ',
		'《': ' <',
		'》': '> ',
		'…': '... ',
		'—': '- '
	}

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.dictionary = {}  # {chinese: [vietnamese1, vietnamese2, ...]}
		self.enabled = False  # Default: disabled
		self.loadDictionary()
		
		# Register speech hook
		try:
			speech.speech.pre_speech.register(self.onPreSpeech)
			logHandler.log.info("Registered with speech.pre_speech extension point")
		except Exception as e:
			logHandler.log.error(f"Failed to register speech hook: {e}")
		
		logHandler.log.info("Chinese-Vietnamese Dictionary addon initialized (disabled by default)")
	
	def loadDictionary(self):
		"""Load dictionary file - supports multiple values per key"""
		try:
			addonPath = os.path.dirname(os.path.dirname(__file__))
			dictPath = os.path.join(addonPath, "dictionaries", "dic.dic")
			
			if not os.path.exists(dictPath):
				logHandler.log.error(f"Dictionary file not found: {dictPath}")
				return
			
			logHandler.log.info(f"Loading dictionary from: {dictPath}")
			
			# Load all entries, keeping duplicates as list
			count = 0
			with open(dictPath, 'r', encoding='utf-8') as f:
				for line in f:
					line = line.strip()
					if not line or line.startswith('#'):
						continue
					
					parts = line.split('\t')
					if len(parts) >= 2:
						chinese = parts[0].strip()
						vietnamese = parts[1].strip()
						
						if chinese:
							# FILTER: Skip punctuation in dictionary (let PUNCT_MAP handle it fallback)
							if chinese in self.PUNCT_MAP:
								continue

							# CLEANUP: Handle '的' (đích) and '了' (liễu)
							
							# Handle '的'
							if chinese == '的':
								vietnamese = ''
							elif chinese.endswith('的'):
								if vietnamese.endswith(' đích'):
									vietnamese = vietnamese[:-5]
								elif vietnamese.endswith('đích'):
									vietnamese = vietnamese[:-4]
							
							# Handle '了'
							if chinese == '了':
								vietnamese = '' # Mute '了' (was 'liễu')
							elif chinese.endswith('了'):
								if vietnamese.endswith(' liễu'):
									vietnamese = vietnamese[:-5]
								elif vietnamese.endswith('liễu'):
									vietnamese = vietnamese[:-4]
							
							# Add to list (support multiple values)
							if chinese not in self.dictionary:
								self.dictionary[chinese] = []
							
							# avoid adding duplicates if we already have this translation
							if vietnamese not in self.dictionary[chinese]:
								self.dictionary[chinese].append(vietnamese)
							
							count += 1
			
			logHandler.log.info(f"Successfully loaded {count} dictionary entries")
			logHandler.log.info(f"Unique Chinese words: {len(self.dictionary)}")
		except Exception as e:
			logHandler.log.error(f"Error loading dictionary: {e}")
	
	def onPreSpeech(self, speechSequence=None, **kwargs):
		"""Handler called before speech - modifies speechSequence in place"""
		if not self.enabled or not self.dictionary:
			return
		
		try:
			for i, item in enumerate(speechSequence):
				if isinstance(item, str):
					speechSequence[i] = self._replaceText(item)
		except Exception as e:
			logHandler.log.error(f"Error in onPreSpeech: {e}", exc_info=True)
	
	def _replaceText(self, text):
		"""Replace text using dictionary with longest match first"""
		if not text or not self.dictionary:
			return text
		
		result = []
		i = 0
		textLen = len(text)
		replacementCount = 0
		lastWasReplacement = False
		
		while i < textLen:
			maxMatchLen = min(50, textLen - i)
			matched = False
			
			# Try longest match first
			for length in range(maxMatchLen, 0, -1):
				substring = text[i:i+length]
				if substring in self.dictionary:
					# Found match - get Vietnamese
					vietnameseOptions = self.dictionary[substring]
					vietnameseText = vietnameseOptions[0]
					
					# Add space BEFORE replacement if previous char was not space/punct
					if result:
						lastChar = result[-1][-1] if result[-1] else ''
						if lastChar not in ' \t\n\r"\'([<{':
							result.append(' ')
					
					result.append(vietnameseText)
					i += length
					matched = True
					replacementCount += 1
					lastWasReplacement = True
					break
			
			if not matched:
				# No match found (original character)
				currentChar = text[i]
				
				# Standarize punctuation
				if currentChar in self.PUNCT_MAP:
					currentChar = self.PUNCT_MAP[currentChar]
				
				# Add space BEFORE original char IF previous was a replacement
				# BUT NOT if current char is punctuation (comma, dot, etc)
				# This handles "Việt"+"NVDA" -> "Việt NVDA"
				# But "Việt"+"," -> "Việt,"
				if lastWasReplacement:
					if currentChar not in ' \t\n\r,.;:!?)[]>}\'"-_':
						result.append(' ')
					# else: no space before punctuation
				
				result.append(currentChar)
				lastWasReplacement = False
				i += 1
		
		finalText = ''.join(result)
		if replacementCount > 0:
			logHandler.log.debug(f"Made {replacementCount} replacements in text")
		
		return finalText
	
	def script_toggleDictionary(self, gesture):
		"""Toggle dictionary on/off with NVDA+Alt+V"""
		self.enabled = not self.enabled
		
		if self.enabled:
			tones.beep(800, 100)  # High beep = ON
			logHandler.log.info("Dictionary enabled")
		else:
			tones.beep(200, 100)  # Low beep = OFF
			logHandler.log.info("Dictionary disabled")
	
	script_toggleDictionary.__doc__ = "Toggle Chinese-Vietnamese dictionary processing"
	
	def terminate(self):
		"""Cleanup when addon is disabled"""
		try:
			speech.speech.pre_speech.unregister(self.onPreSpeech)
			logHandler.log.info("Unregistered from speech.pre_speech")
		except Exception as e:
			logHandler.log.error(f"Error unregistering speech hook: {e}")
		
		logHandler.log.info("Chinese-Vietnamese Dictionary addon terminated")
		super(GlobalPlugin, self).terminate()
	
	__gestures = {
		"kb:NVDA+alt+v": "toggleDictionary",
	}
