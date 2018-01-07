import requests
import pprint
import json
url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json"
def check(menu, menu_list, curr_list):
	valid_list = True
	tmp_list = []
	curr_list.append(menu['id'])
	for i in menu['child_ids']:
		if i in curr_list:
			valid_list = False
		else:
			for m in menu_list:
				if m['id']==i:
					if valid_list:
						valid_list, tmp_list = check(m, menu_list, curr_list)
					else:
						_, tmp_list = check(m, menu_list, curr_list)
		for m in tmp_list:
			if not(m in curr_list):
				curr_list.append(m)
	return valid_list, curr_list

def get_menu(challenge_id):
	print("Challenge Part No.", challenge_id)
	params = {"id": challenge_id, "page": 1}
	menu_list = []
	total_pages = 1
	print("Retrieving menu list...")
	while params['page']<=total_pages:
		r = json.loads(requests.get(url, params=params).text)
		total_pages = r['pagination']['total']
		for menu in r['menus']:
			menu_list.append(menu) 
		params['page']+=1
	print("Done")
	return menu_list

def check_menu_list(menu_list):
	answer = {"valid_menus": [], "invalid_menus": []}
	checked = []
	for menu in menu_list:
		if menu['id'] in checked:
			continue
		print("Checking menu id: ", menu['id'])
		valid_list,curr_list = check(menu, menu_list, [])
		for m in curr_list:
			checked.append(m)
		if(valid_list):
			answer['valid_menus'].append({'root_id': curr_list[0], 'children': curr_list[1:] })
		else:
			answer['invalid_menus'].append({'root_id': curr_list[0], 'children': curr_list[1:]})
	return answer

menus = get_menu(1)
print("Part 1 Answer: ")
pprint.pprint(check_menu_list(menus))
print()

menus = get_menu(2)
print("Part 2 Answer: ")
pprint.pprint(check_menu_list(menus))
print()





	