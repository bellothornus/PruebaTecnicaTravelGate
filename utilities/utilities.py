def lowercase_dictionary(dictionary):
	new_dict = {}
	if isinstance(dictionary,str):
		return dictionary.lower()
	if isinstance(dictionary, dict):
		for k, v in dictionary.items():
			if isinstance(v, dict):
				new_dict[lowercase_dictionary(k)] = lowercase_dictionary(v)
			else:
				new_dict[lowercase_dictionary(k)] = v
	else:
		new_dict = dictionary
	return new_dict

# p_dict = {'Hola': {'Y': {'Adios': "NO ME CAMBIES PORFI"}}}
# p_dict2 =  {'Hola': {'Y': {'Adios': 98}}}

# p_dict_new = lowercase_dictionary(p_dict)
# p_dict2_new = lowercase_dictionary(p_dict2)
# print(p_dict_new)
# print(p_dict2_new)