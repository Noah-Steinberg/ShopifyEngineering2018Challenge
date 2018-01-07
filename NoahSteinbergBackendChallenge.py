import requests
import pprint
import json
url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json"
def check(menu, menus, nodes):
	valid = True
	tmp = []
	nodes.append(menu['id'])
	for i in menu['child_ids']:
		if i in nodes:
			valid = False
		else:
			for m in menus:
				if m['id']==i:
					if valid:
						valid, tmp = check(m, menus, nodes)
					else:
						_, tmp = check(m, menus, nodes)
		for node in tmp:
			if not(node in nodes):
				nodes.append(node)
	return valid, nodes

def get_menu(challenge_id):
	print("Challenge Part No.", challenge_id)
	params = {"id": challenge_id, "page": 1}
	menus = []
	total_pages = 1
	print("Retrieving menu list...")
	while params['page']<=total_pages:
		r = json.loads(requests.get(url, params=params).text)
		total_pages = r['pagination']['total']
		for m in r['menus']:
			menus.append(m) 
		params['page']+=1
	print("Done")
	return menus

def check_menu_list(menus):
	answer = {"valid_menus": [], "invalid_menus": []}
	checked = []
	for m in menus:
		if m['id'] in checked:
			continue
		print("Checking menu id: ", m['id'])
		valid,nodes = check(m, menus, [])
		for n in nodes:
			checked.append(n)
		if(valid):
			answer['valid_menus'].append({'root_id': nodes[0], 'children': nodes[1:] })
		else:
			answer['invalid_menus'].append({'root_id': nodes[0], 'children': nodes[1:]})
	return answer

menus = get_menu(1)
print("Part 1 Answer: ")
pprint.pprint(check_menu_list(menus))
print()

menus = get_menu(2)
print("Part 2 Answer: ")
pprint.pprint(check_menu_list(menus))
print()





	