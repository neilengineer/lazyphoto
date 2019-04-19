#pip install pillow
from PIL import Image, ImageOps, ImageEnhance

def beautify_img(img_obj):
	try:
		tmpimg = img_obj
		tmpimg_border = ImageOps.expand(tmpimg, 1)
		tmpimg_enhance = ImageEnhance.Brightness(tmpimg_border).enhance(1.2)
	except Exception as ex:
		template = "An exception of type {0} occurred. Arguments:\n{1!r}"
		message = template.format(type(ex).__name__, ex.args)
		print(message)
		return -2
	else:
		return tmpimg_enhance

#Make photo e.g. 4x6 inch
#photo_size in inch
def make_photo(img_obj, photo_size, target_name, target_type):
	target_file_name=target_name+"."+target_type

	#300 PPI is usual photo quality
	ppi=300
	photo_size_pixel = (photo_size[0]*ppi,photo_size[1]*ppi)

	newimg = Image.new('RGBA', photo_size_pixel, 'white')

	newimg_w, newimg_h = photo_size_pixel
	small_img_w, small_img_h = img_obj.size
	#print(newimg_w, newimg_h, small_img_w, small_img_h)
	if newimg_w%(small_img_w)==0 or newimg_h%(small_img_h)==0:
		gap = 0
	else:
		gap = 10

	#find the origin of sub-imgs
	total_pic_num_w = int(newimg_w/(small_img_w+gap))
	g_left = (newimg_w - total_pic_num_w*(small_img_w+gap))/2
	total_pic_num_h = int(newimg_h/(small_img_h+gap))
	g_top = (newimg_h - total_pic_num_h*(small_img_h+gap))/2

	#paste small img as tile
	for left in range(int(g_left), newimg_w, small_img_w+gap):
		for top in range(int(g_top), newimg_h, small_img_h+gap):
			if left+small_img_w+gap>newimg_w or top+small_img_h+gap>newimg_h:
				break;
			newimg.paste(img_obj, (left+gap, top+gap))

	newimg = newimg.convert('RGB')

	try:
		newimg.save(target_file_name)
	except KeyError:
		print("format not supported")
		return -1
	except IOError:
		print("IOError error")
		return -2
	except Exception as ex:
		template = "An exception of type {0} occurred. Arguments:\n{1!r}"
		message = template.format(type(ex).__name__, ex.args)
		print(message)
		return -3
	else:
		return target_file_name

#import sys
#app, inputfile = sys.argv

#img=Image.open(inputfile)
#beautified = beautify_img(img)

#make photo
'''
ppi=300
target_w = 1*ppi
target_h = 2*ppi
crop_size_inch_w = target_w/ppi
crop_size_inch_h = target_h/ppi 

if crop_size_inch_w <= 4:
	photo_paper_size = (4,6)
elif crop_size_inch_w > 4 and crop_size_inch_w < 8:
	photo_paper_size = (8,10)
else:
	photo_paper_size = (4,6)

make_photo(beautified, photo_paper_size, "cat-tile","png")
'''

