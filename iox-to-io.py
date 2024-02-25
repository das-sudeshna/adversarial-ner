# IMPORTS
import sys

# TAGS
## SOURCE
s_location_tags = ['B-LOC','I-LOC'] 
s_person_tags = ['B-PER','I-PER']
s_organization_tags = ['B-ORG','I-ORG']
s_nonentity_tags = ['O','B-MISC','I-MISC']

## TARGET
t_location_tag = 'Location'
t_person_tag = 'Person'
t_organization_tag = 'Organization'
t_nonentity_tag = 'Other'

# SEPARATOR
sep = '\t'

# POSITIONS
token_at = 0
tag_at = 1

# READ FILE
def get_file():
	with open(sys.argv[1],'r') as f_:
		f = f_.readlines()
	return f
			
# CHECK FOR COMMON ISSUES
def sanity_check(f):
	s_tags = s_location_tags + s_person_tags + s_organization_tags + s_nonentity_tags
	for line in f:
		line = line.rstrip()
		if line != '':
			line = line.split(sep) # tab as column separator
			if len(line)!=2:
				print('Error: File does not contain 2 columns (tab-separated token-tag)')
				exit(0)
			else:
				if line[tag_at] not in s_tags:
					print('Error: Invalid tags!\nPossible issue/fix:\n(a) Fix: Edit TAGS --> SOURCE section of code.\n(b) Issue: File not in TOKEN \\t TAG format. Edit POSITIONS section of code.\nError due to: ',line[tag_at])
					exit(0)

# CHANGE TAGGING SCHEME TO IO
def convert2io(f):
	writefile = sys.argv[1].split('.')[0] + '-io.conll'
	with open(writefile, 'w') as wf:
		for line in f:
			line = line.rstrip()
			if line != '':
				line = line.split('\t')
				line[token_at] = line[token_at]
				wf.write(line[token_at])
				wf.write('\t')
				if line[tag_at].rstrip() in s_location_tags:
					line[tag_at] = t_location_tag
					wf.write(line[tag_at])
					wf.write('\n')
				elif line[tag_at].rstrip() in s_person_tags:
					line[tag_at] = t_person_tag
					wf.write(line[tag_at])
					wf.write('\n')
				elif line[tag_at].rstrip() in s_organization_tags:
					line[tag_at] = t_organization_tag
					wf.write(line[tag_at])
					wf.write('\n')
				elif line[tag_at].rstrip() in s_nonentity_tags:
					line[tag_at] = t_nonentity_tag
					wf.write(line[tag_at])
					wf.write('\n')
				else:
					print('Error: Unknown tag found!\Fix: Edit TAGS --> SOURCE section of code. Error due to:', line[token_at], line[tag_at])
					exit(0)
			else:
				wf.write(line)
				wf.write('\n')

# GENERATE EVAL FILE (.conll)
f = get_file()
sanity_check(f)
convert2io(f)