import cairo

side_margin = .07
logo_margin = .09
footer_margin = .05
padding = .005

def bubble (cr, x0, y0, x, y, w, h):

	x1, y1, x2, y2 = x, y, x + w, y + h
	r = min (w, h) * .15

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
	l = logo_margin * height
	f = footer_margin * height
	p = padding * min (width, height)
	p2 = 2 * p

	# Blue sky (first white, then gradient)
	cr.set_source_rgb (1, 1, 1)
	sky = cairo.LinearGradient (0, 0, 0, height)
	sky.add_color_stop_rgba (0, .6, .65, 1, 1.0)
	sky.add_color_stop_rgba (1, .6, .65, 1, 0.2)
	cr.set_source (sky)
	cr.paint ()

	# Brown earth
	cr.set_source_rgb (158/255., 87/255., 0/255.)
	cr.rectangle (0, height, width, -p2)
	cr.fill ()

	# GUADEC logo on the bottom
	cr.move_to (.5 * width, height-p2)
	cr.set_source_rgb (0x03/255., 0x40/255., 0x79/255.)
	fw, fh = renderer.put_text ("GUADEC 2007, Birmingham, UK", height=f-p2, valign=-1)
	cr.move_to (.5 * (width - fw), height-p2)
	renderer.put_image ("guadec.svg", height=f-p2, valign=-1, halign=-1)

	# Red Hat/cairo logos at the top
	cr.move_to (p, p)
	renderer.put_image ("redhat.svg", height = l-p2, valign=+1, halign=+1)

	cr.move_to (width-p, p)
	renderer.put_image ("cairo.svg", height = l-p2, valign=+1, halign=-1)

	# Cartoon icons for speakers
	cr.move_to (p, height-p)
	renderer.put_image ("behdad.svg", width = s-p2, valign=-1, halign=+1)

	cr.move_to (width-p, height-p)
	renderer.put_image ("cworth.svg", width = s-p2, valign=-1, halign=-1)

	# Compute rectangle available for slide content
	w = width - s - s - p * 6
	x = s + p * 3
	h = height - l - f - p * 6
	y = l + p * 3

	return x, y, w, h

def draw_bubble (renderer, x, y, w, h):
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

	x -= 3 * p
	y -= 3 * p
	w += 6 * p
	h += 6 * p
	bubble (cr, s * .9, height - .7 * s, x, y, w, h)
	cr.set_source_rgb (0, 0, 0)
	cr.set_line_width (p)
	cr.set_miter_limit (30)
	cr.stroke_preserve ()

	cr.restore()
	cr.clip ()
	cr.set_source_rgb (1, 1, 1)
	cr.paint ()

	cr.set_source_rgb (0, 0, 0)
