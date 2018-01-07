import requests
import pprint
import json
import sys
from time import sleep
url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json"
def progress(count, total):
	bar_len = 60
	filled_len = int(round(bar_len * count / float(total)))

	percents = round(100.0 * count / float(total), 1)
	bar = '=' * filled_len + '-' * (bar_len - filled_len)

	if count!=total:
		sys.stdout.write('Progress: [%s] %s%s...\r' % (bar, percents, '%'))
		sys.stdout.flush()
	else:
		sys.stdout.write('Progress: [%s] %s%s...Done\r' % (bar, percents, '%'))
		sys.stdout.flush()
		print("\n")

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
		total_pages = r['pagination']['total'] // r['pagination']['per_page']
		progress(params['page'], total_pages)
		for menu in r['menus']:
			menu_list.append(menu) 
		params['page']+=1
	return menu_list

def check_menu_list(menu_list):
	answer = {"valid_menus": [], "invalid_menus": []}
	checked = []
	for menu in menu_list:
		if menu['id'] in checked:
			continue
		valid_list,curr_list = check(menu, menu_list, [])
		for m in curr_list:
			checked.append(m)
			progress(len(checked), len(menu_list));
			sleep(0.1)
		if(valid_list):
			answer['valid_menus'].append({'root_id': curr_list[0], 'children': curr_list[1:] })
		else:
			answer['invalid_menus'].append({'root_id': curr_list[0], 'children': curr_list[1:]})
	return answer

menus = get_menu(1)
print("Part 1 Answer: ")
answer = check_menu_list(menus)
pprint.pprint(answer)
for menu_list in answer['invalid_menus']:
	cyclic_id = -1
	for menu_id in menu_list['children']:
		for menu in menus:
			if menu_list['root_id'] in menu['child_ids']:
				cyclic_id = menu['id']
				break
	print("Menu list rooted at", menu_list['root_id'], "is invalid. Recommended fix: remove menu", menu_list['root_id'], "as a child of", cyclic_id)
print()

menus = get_menu(2)
print("Part 2 Answer: ")
answer = check_menu_list(menus)
pprint.pprint(answer)
for menu_list in answer['invalid_menus']:
	for menu in menus:
			if menu_list['root_id'] in menu['child_ids']:
				cyclic_id = menu['id']
				break
	print("Menu list rooted at", menu_list['root_id'], "is invalid. Recommended fix: remove menu", menu_list['root_id'], "as a child of", cyclic_id)
print()





	