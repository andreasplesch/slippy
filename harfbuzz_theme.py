# vim: set fileencoding=utf-8 :
# Written by Behdad Esfahbod, 2007,2009
# Not copyrighted, in public domain.

# A theme file should define two functions:
#
# - prepare_page(renderer): should draw any background and return a tuple of
#   x,y,w,h that is the area to use for slide canvas.
# 
# - draw_bubble(renderer, x, y, w, h, data=None): should setup canvas for the
#   slide to run.  Can draw a speaking-bubble for example.  x,y,w,h is the
#   actual extents that the slide will consume.  Data will be the user-data
#   dictionary from the slide.
#
# Renderer is an object similar to a cairo.Context and pangocairo.CairoContext
# but has its own methods too.  The more useful of them here are put_text and
# put_image.  See their pydocs.

import cairo

side_margin = .06
top_margin = .02
bottom_margin = .06
padding = .005
bubble_rad = .25

def bubble (cr, x0, y0, x, y, w, h):

	r = min (w, h) * (bubble_rad / (1 - 2./8*bubble_rad))

	p = r / 7.
	x, y, w, h, r = x - p, y - p, w + 2*p, h + 2*p, r + p

	x1, y1, x2, y2 = x, y, x + w, y + h

	cr.move_to (x1+r, y1)
	cr.line_to (x2-r, y1)
	cr.curve_to (x2, y1, x2, y1, x2, y1+r)
	cr.line_to (x2, y2-r)
	cr.curve_to (x2, y2, x2, y2, x2-r, y2)
	cr.line_to (x1+r, y2)
	cr.curve_to (x1, y2, x1, y2, x1, y2-r)
	cr.line_to (x1, y1+r)
	cr.curve_to (x1, y1, x1, y1, x1+r, y1)
	cr.close_path ()

	xc, yc = .5 * (x1 + x2), .5 * (y1 + y2)
	cr.move_to (xc+r, yc)
	cr.curve_to (xc+r, y0, .5 * (xc+r+x0), (yc+y0*2)/3, x0, y0)
	cr.curve_to (.5 * (xc-r+x0), (yc+y0*2)/3, xc-r, y0, xc-r, yc)


def prepare_page (renderer):
	cr = renderer.cr
	width = renderer.width
	height = renderer.height
	
	s = side_margin * width
	l = top_margin * height
	f = bottom_margin * height
	p = padding * min (width, height)
	p2 = 2 * p

	cr.set_source_rgb (128/255., 255/255., 148/255.)
	cr.paint ()

	cr.move_to (.5 * width, height-p2)
	cr.set_source_rgba (0,.2,0)
	renderer.put_text ("Internationalization &amp; Unicode Conference, October 15, 2009, San Jose", height=(f-p2)*.8, width=(width-2*s)*.8, valign=-1)

	cr.move_to (width-p, height-p)
	#renderer.put_image ("unicode.png", height = f-p2, valign=-1, halign=-1)

	# Cartoon icons for speakers
	cr.move_to (p, height-p)
	renderer.put_image ("behdad.svg", width = s-p2, valign=-1, halign=+1)

	# Compute rectangle available for slide content
	w = width - s - s - p * 2
	x = s + p
	h = height - l - f - p * 2
	y = l + p

	# Adjust for bubble padding. the 8 comes from bezier calculations
	d = min (w, h) * bubble_rad / 8.
	x, y, w, h = x + d, y + d, w - d*2, h - d*2

	return x, y, w, h

def draw_bubble (renderer, x, y, w, h, data=None):
	# Fancy speech bubble!
	cr = renderer.cr
	width = renderer.width
	height = renderer.height
	
	s = side_margin * width
	p = padding * min (width, height)

	cr.save()
	x, y = cr.user_to_device (x, y)
	w, h = cr.user_to_device_distance (w, h)
	cr.identity_matrix ()

	who = data.get ('who', None)
	if not who:
		xc, yc = x + w*.5, y + h*.5
	elif who < 0:
		xc, yc = s * .9, height - .7 * s
	else:
		xc, yc = width - s * .9, height - .7 * s

	bubble (cr, xc, yc, x, y, w, h)
	cr.rectangle (width, 0, -width, height)
	cr.clip ()

	a = .5

	bubble (cr, xc, yc, x, y, w, h)
	cr.set_source_rgb (64/255.*a, 128/255.*a, 64/255.*a)
	cr.set_line_width (p)
	cr.set_miter_limit (20)
	cr.stroke_preserve ()

	cr.restore ()

	cr.clip ()
	cr.set_source_rgba (.92, .98, 1, 1)
	cr.paint ()

	cr.set_source_rgb (96/255.*a, 128/255.*a, 96/255.*a)
