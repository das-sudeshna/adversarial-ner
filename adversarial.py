# IMPORTS
import sys
import random

# TAGS
location_tags = ['Location']
person_tags = ['Person']
organization_tags = ['Organization']
nonentity_tags = ['Other']

# POSITIONS
token_at = 0
tag_at = 1

entity_tags = location_tags + person_tags + organization_tags
tags = location_tags + person_tags + organization_tags + nonentity_tags

# READ FILE
def get_file():
	with open(sys.argv[1], 'r') as f_:
		f = f_.readlines()
	return f
			
# CHECK FOR COMMON ISSUES
def sanity_check(f):
	for line in f:
		line = line.rstrip()
		if line != '':
			line = line.split('\t') # tab as column separator
			if len(line)!=2:
				print('Error: File does not contain 2 columns (tab-separated token-tag)')
				exit(0)
			else:
				if line[tag_at] not in tags:
					print('Error: Invalid tags!\nPossible issues:\n(a) Different tagging scheme in use. Fix: Edit TAGS section of code.\n(b) File not in TOKEN \\t TAG format. Edit POSITIONS section of code.')
					exit(0)

# GENERATE EVAL FILE (.conll)
def gen_evals(f, attack, alltokens, alltags):
	writefile = sys.argv[1].split('.')[0] + '-' + attack + '.conll'
	with open(writefile, 'w') as wf:
		if attack not in ['perturbation','alteration']:
			for token_, tag_ in zip(alltokens, alltags):
				if token_ != '\n':
					line = token_ + '\t' + tag_
					wf.write(line)
				else:
					wf.write('\n')
		else:#perturbation or alteration
			for token_, tag_ in zip(alltokens, alltags):
				if token_ == '\n' or token_ == '':
					wf.write('\n')
				else:
					line = token_ + '\t' + tag_ + '\n'
					wf.write(line)

# CASE ABLATION
def ablation(f):
	alltokens = []
	alltags = []
	for line in f:
		if line != '\n':
			line = line.split('\t')
			line[token_at] = line[token_at].lower()
			alltokens.append(line[token_at])
			alltags.append(line[tag_at])
		else:
			alltokens.append(line[token_at])
			alltags.append('')
	gen_evals(f, 'ablation', alltokens, alltags)

# CASE ABERRATION
def aberration(f):
	alltokens = []
	alltags = []
	entity_tokens = 0
	sent_start = True
	for line in f:
		if line != '\n':
			line = line.split('\t')
			line[tag_at] = line[tag_at].rstrip()
			if sent_start:
				alltokens.append(line[token_at])
				alltags.append(line[tag_at]+'\n')
				sent_start = False
			else:
				if line[tag_at] in entity_tags:
					if line[token_at].upper() != line[token_at]:
						entity_tokens += 1
						alltokens.append(line[token_at].lower())
						alltags.append(line[tag_at]+'\n')
					else:
						alltokens.append(line[token_at])
						#print('this done 4')
						alltags.append(line[tag_at]+'\n')
				else:
					alltokens.append(line[token_at])
					alltags.append(line[tag_at]+'\n')
		else:
			sent_start = True
			alltokens.append(line[token_at])
			alltags.append('\n')
	# capitalize N tokens randomly excluding existing capitalized/uppercase tokens
	while entity_tokens > 0:
		random_index = random.randint(0, len(alltokens) - 1)
		selected = alltokens[random_index]
		if selected[0].upper() == selected[0]:
			continue
		else:
			alltokens[random_index] = alltokens[random_index].capitalize()
			entity_tokens -= 1
	gen_evals(f, 'aberration', alltokens, alltags)

# CONTEXT PERTURBATION
def perturbation(f):
	alltokens = []
	alltags = []
	locations = []
	persons = []
	organizations = []
	temp_token_span = []
	temp_tag = ''
	for line in f:
		line = line.rstrip()
		if line != '':	
			line = line.split('\t')
			if line[tag_at] in location_tags: #is location entity token
				if temp_token_span == []: #begin location entity
					alltokens.append('LOCATIONTOKEN') #mark location in sequence where LOCATION appears
					alltags.append('LOCATIONTAG')	#mark location in sequence where LOCATION appears
					temp_token_span.append(line[token_at])
					temp_tag = line[tag_at]
				else:
					if temp_tag == line[tag_at]: #adjacent location token
						temp_token_span.append(line[token_at])
					else: #adjacent entity token but not location type
						if temp_tag == 'Organization':
							organizations.append(temp_token_span)
						elif temp_tag == 'Person':
							persons.append(temp_token_span)
						else:
							locations.append(temp_token_span)
						temp_token_span = []
						temp_token_span.append(line[token_at])
						temp_tag = line[tag_at]
			elif line[tag_at] in person_tags: #is person entity token
				if temp_token_span == []: #begin person entity
					alltokens.append('PERSONTOKEN') #mark person in sequence where PERSON appears
					alltags.append('PERSONTAG')	#mark location in sequence where PERSON appears
					temp_token_span.append(line[token_at])
					temp_tag = line[tag_at]
				else:
					if temp_tag == line[tag_at]: #adjacent person token
						temp_token_span.append(line[token_at])
					else: #adjacent entity token but not person type
						if temp_tag == 'Location':
							locations.append(temp_token_span)
						elif temp_tag == 'Organization':
							organizations.append(temp_token_span)
						else:
							persons.append(temp_token_span)
						temp_token_span = []
						temp_token_span.append(line[token_at])
						temp_tag = line[tag_at]
			elif line[tag_at] in organization_tags: #is organization entity token
				if temp_token_span == []: #begin organization entity
					alltokens.append('ORGANIZATIONTOKEN') #mark person in sequence where ORGANIZATION appears
					alltags.append('ORGANIZATIONTAG')	#mark location in sequence where ORGANIZATION appears
					temp_token_span.append(line[token_at])
					temp_tag = line[tag_at]
				else:
					if temp_tag == line[tag_at]: #adjacent organization token
						temp_token_span.append(line[token_at])
					else: #adjacent entity token but not organization type
						if temp_tag == 'Person':
							persons.append(temp_token_span)
						elif temp_tag == 'Location':
							locations.append(temp_token_span)
						else:
							organizations.append(temp_token_span)
						temp_token_span = []
						temp_token_span.append(line[token_at])
						temp_tag = line[tag_at]
			else:
				if temp_tag == 'Location':
					locations.append(temp_token_span)
					temp_token_span = []
					temp_tag = ''
					alltokens.append('LOCATIONTOKEN')
					alltags.append('LOCATIONTAG')
				elif temp_tag == 'Person':
					persons.append(temp_token_span)
					temp_token_span = []
					temp_tag = ''
					alltokens.append('PERSONTOKEN')
					alltags.append('PERSONTAG')
				elif temp_tag == 'Organization':
					organizations.append(temp_token_span)
					temp_token_span = []
					temp_tag = ''
					alltokens.append('ORGANIZATIONTOKEN')
					alltags.append('ORGANIZATIONTAG')
				else:
					alltokens.append(line[token_at])
					alltags.append(line[tag_at])
		else:
			if temp_tag == 'Location':
				locations.append(temp_token_span)
				temp_token_span = []
				temp_tag = ''
			elif temp_tag == 'Person':
				persons.append(temp_token_span)
				temp_token_span = []
				temp_tag = ''
			elif temp_tag == 'Organization':
				organizations.append(temp_token_span)
				temp_tag = ''
			else:
				alltokens.append('')
				alltags.append('')
	# perturbation
	for i, (tok_, tag_) in enumerate(zip(alltokens,alltags)):
		if tok_ == 'LOCATIONTOKEN':
			# insert person or organization entity with equal probability
			if len(persons) > 0 and len(organizations) > 0:
				pick_type = random.choice(['org', 'per'])
				if pick_type == 'per':
					tok_ = persons.pop(0)
					entlen = len(tok_)
					tag_ = []
					for j in range(entlen):
						tag_.append('Person')
				else:
					tok_ = organizations.pop(0)
					entlen = len(tok_)
					tag_ = []
					for j in range(entlen):
						tag_.append('Organization')
				alltokens.pop(i)
				alltags.pop(i)
				alltokens[i:i] = tok_
				alltags[i:i] = tag_
			elif len(persons) > 0:
				tok_ = persons.pop(0)
				entlen = len(tok_)
				tag_ = []
				for j in range(entlen):
					tag_.append('Person')
				alltokens.pop(i)
				alltags.pop(i)
				alltokens[i:i] = tok_
				alltags[i:i] = tag_
			elif len(organizations) > 0:
				tok_ = organizations.pop(0)
				entlen = len(tok_)
				tag_ = []
				for j in range(entlen):
					tag_.append('Organization')
				alltokens.pop(i)
				alltags.pop(i)
				alltokens[i:i] = tok_
				alltags[i:i] = tag_
			else:
				# truncate to last available full sentence
				alltokens = alltokens[:i]
				alltags = alltags[:i]
				trunc_at = next(i for i in reversed(range(len(alltokens))) if alltokens[i] == '')
				alltokens = alltokens[:trunc_at]
				alltags = alltags[:trunc_at]
				gen_evals(f, 'perturbation', alltokens, alltags)
				exit()
		elif tok_ == 'PERSONTOKEN':
			# insert location or organization entity with equal probability
			if len(locations) > 0 and len(organizations) > 0:
				pick_type = random.choice(['org', 'loc'])
				if pick_type == 'loc':
					tok_ = locations.pop(0)
					entlen = len(tok_)
					tag_ = []
					for j in range(entlen):
						tag_.append('Location')
				else:
					tok_ = organizations.pop(0)
					entlen = len(tok_)
					tag_ = []
					for j in range(entlen):
						tag_.append('Organization')
				alltokens.pop(i)
				alltags.pop(i)
				alltokens[i:i] = tok_
				alltags[i:i] = tag_
			elif len(locations) > 0:
				tok_ = locations.pop(0)
				entlen = len(tok_)
				tag_ = []
				for j in range(entlen):
					tag_.append('Location')
				alltokens.pop(i)
				alltags.pop(i)
				alltokens[i:i] = tok_
				alltags[i:i] = tag_
			elif len(organizations) > 0:
				tok_ = organizations.pop(0)
				entlen = len(tok_)
				tag_ = []
				for j in range(entlen):
					tag_.append('Organization')
				alltokens.pop(i)
				alltags.pop(i)
				alltokens[i:i] = tok_
				alltags[i:i] = tag_
			else:
				# truncate to last available full sentence
				alltokens = alltokens[:i]
				alltags = alltags[:i]
				trunc_at = next(i for i in reversed(range(len(alltokens))) if alltokens[i] == '')
				alltokens = alltokens[:trunc_at]
				alltags = alltags[:trunc_at]
				gen_evals(f, 'perturbation', alltokens, alltags)
				exit()
		elif tok_ == 'ORGANIZATIONTOKEN':
			# insert person or location entity with equal probability
			if len(locations) > 0 and len(persons) > 0:
				pick_type = random.choice(['per', 'loc'])
				if pick_type == 'loc':
					tok_ = locations.pop(0)
					entlen = len(tok_)
					tag_ = []
					for j in range(entlen):
						tag_.append('Location')
				else:
					tok_ = persons.pop(0)
					entlen = len(tok_)
					tag_ = []
					for j in range(entlen):
						tag_.append('Person')
				alltokens.pop(i)
				alltags.pop(i)
				alltokens[i:i] = tok_
				alltags[i:i] = tag_
			elif len(locations) > 0:
				tok_ = locations.pop(0)
				entlen = len(tok_)
				tag_ = []
				for j in range(entlen):
					tag_.append('Location')
				alltokens.pop(i)
				alltags.pop(i)
				alltokens[i:i] = tok_
				alltags[i:i] = tag_
			elif len(persons) > 0:
				tok_ = persons.pop(0)
				entlen = len(tok_)
				tag_ = []
				for j in range(entlen):
					tag_.append('Person')
				alltokens.pop(i)
				alltags.pop(i)
				alltokens[i:i] = tok_
				alltags[i:i] = tag_
			else:
				# truncate to last available full sentence
				alltokens = alltokens[:i]
				alltags = alltags[:i]
				trunc_at = next(i for i in reversed(range(len(alltokens))) if alltokens[i] == '')
				alltokens = alltokens[:trunc_at]
				alltags = alltags[:trunc_at]
				gen_evals(f, 'perturbation', alltokens, alltags)
				exit()
		else:
			pass			
	gen_evals(f, 'perturbation', alltokens, alltags)

# CONTEXT ALTERATION
def alteration(f):
	alltokens = []
	alltags = []
	locations = []
	persons = []
	organizations = []
	temp_token_span = []
	temp_tag = ''
	for line in f:
		line = line.rstrip()
		if line != '':	
			line = line.split('\t')
			if line[tag_at] in location_tags: #is location entity token
				if temp_token_span == []: #begin location entity
					temp_token_span.append(line[token_at])
					temp_tag = line[tag_at]
				else:
					if temp_tag == line[tag_at]: #adjacent location token
						temp_token_span.append(line[token_at])
					else: #adjacent entity token but not location type
						if temp_tag == 'Organization':
							organizations.append(temp_token_span)
						elif temp_tag == 'Person':
							persons.append(temp_token_span)
						else:
							locations.append(temp_token_span)
						temp_token_span = []
						temp_token_span.append(line[token_at])
						temp_tag = line[tag_at]
			elif line[tag_at] in person_tags: #is person entity token
				if temp_token_span == []: #begin person entity
					temp_token_span.append(line[token_at])
					temp_tag = line[tag_at]
				else:
					if temp_tag == line[tag_at]: #adjacent person token
						temp_token_span.append(line[token_at])
					else: #adjacent entity token but not person type
						if temp_tag == 'Location':
							locations.append(temp_token_span)
						elif temp_tag == 'Organization':
							organizations.append(temp_token_span)
						else:
							persons.append(temp_token_span)
						temp_token_span = []
						temp_token_span.append(line[token_at])
						temp_tag = line[tag_at]
			elif line[tag_at] in organization_tags: #is organization entity token
				if temp_token_span == []: #begin organization entity
					temp_token_span.append(line[token_at])
					temp_tag = line[tag_at]
				else:
					if temp_tag == line[tag_at]: #adjacent organization token
						temp_token_span.append(line[token_at])
					else: #adjacent entity token but not organization type
						if temp_tag == 'Person':
							persons.append(temp_token_span)
						elif temp_tag == 'Location':
							locations.append(temp_token_span)
						else:
							organizations.append(temp_token_span)
						temp_token_span = []
						temp_token_span.append(line[token_at])
						temp_tag = line[tag_at]
			else:
				if temp_tag == 'Location':
					locations.append(temp_token_span)
					temp_token_span = []
					temp_tag = ''
				elif temp_tag == 'Person':
					persons.append(temp_token_span)
					temp_token_span = []
					temp_tag = ''
				elif temp_tag == 'Organization':
					organizations.append(temp_token_span)
					temp_token_span = []
					temp_tag = ''
				else:
					alltokens.append(line[token_at])
					alltags.append(line[tag_at])
		else:
			if temp_tag == 'Location':
				locations.append(temp_token_span)
				temp_token_span = []
				temp_tag = ''
			elif temp_tag == 'Person':
				persons.append(temp_token_span)
				temp_token_span = []
				temp_tag = ''
			elif temp_tag == 'Organization':
				organizations.append(temp_token_span)
				temp_tag = ''
			else:
				alltokens.append('')
				alltags.append('')
	#create entity list and entity tag spans list
	allentities = []
	allentitytags = []
	for ent in locations:
		tempentitytag = []
		allentities.append(ent)
		entlen = len(ent)
		for i in range(entlen):
			tempentitytag.append('Location')
		allentitytags.append(tempentitytag)
	for ent in persons:
		tempentitytag = []
		allentities.append(ent)
		entlen = len(ent)
		for i in range(entlen):
			tempentitytag.append('Person')
		allentitytags.append(tempentitytag)
	for ent in organizations:
		tempentitytag = []
		allentities.append(ent)
		entlen = len(ent)
		for i in range(entlen):
			tempentitytag.append('Organization')
		allentitytags.append(tempentitytag)
	# insert entities in randomly selected locations
	for ent_,tag_ in zip(allentities,allentitytags):
		working_length = len(alltokens)
		random_index = random.randint(0, working_length - 1)
		alltokens[random_index:random_index] = ent_
		alltags[random_index:random_index] = tag_
	# truncate to last available full sentence
	trunc_at = next(i for i in reversed(range(len(alltokens))) if alltokens[i] == '')
	alltokens = alltokens[:trunc_at]
	alltags = alltags[:trunc_at]
	gen_evals(f, 'alteration', alltokens, alltags)

f = get_file()
sanity_check(f)
ablation(f)
aberration(f)
perturbation(f)
alteration(f)