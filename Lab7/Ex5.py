celebs = ("Taylor Swift", "Beyonce", "Adele", "Zendaya", "Tom Holland")
ages = (36, 41, 35, 30, 30)	

celeb_list = []
for celeb in celebs:
    celeb_list.append(celeb)
    
ages_list = [age for age in ages]
celebs_dict = {"celebs": celeb_list, "ages": ages_list}
print(celebs_dict)
