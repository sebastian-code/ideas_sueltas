#!/usr/bin/python

import gobject
import pango
import gtk
import gtk.gdk as gdk

BORDER_WIDTH=1

def osd(text, bgcolor, fgcolor, fontdesc,
        use_markup=False, alignment=pango.ALIGN_CENTER,
        fake_translucent_bg=False, drop_shadow=False,
        max_width=None, debug_frame=False, ellipsize=pango.ELLIPSIZE_NONE):
    assert isinstance(fontdesc, pango.FontDescription)
    win = gtk.Window(gtk.WINDOW_POPUP)
    win.add_events(gtk.gdk.ENTER_NOTIFY_MASK)

    darea = gtk.DrawingArea()
    win.add(darea)
    darea.show()
    if use_markup:
        layout = win.create_pango_layout('')
        layout.set_markup(text)
    else:
        layout = win.create_pango_layout(text)
    try:
        layout.set_ellipsize(ellipsize)
    except AttributeError:
        print "ellipsize attribute not supported, ignored"
    layout.set_justify(False)
    layout.set_alignment(alignment)
    layout.set_font_description(fontdesc)
    if max_width is None:
        MAX_WIDTH = gdk.screen_width() - 8
    else:
        MAX_WIDTH = max_width - 8
    layout.set_width(pango.SCALE*MAX_WIDTH)
    if ellipsize != pango.ELLIPSIZE_NONE:
        layout.set_wrap(pango.WRAP_WORD)
    width, height = layout.get_pixel_size()
    off_x = BORDER_WIDTH*2
    off_y = BORDER_WIDTH*2

    if alignment == pango.ALIGN_CENTER:
        off_x -= MAX_WIDTH/2 - width/2
    elif alignment == pango.ALIGN_RIGHT:
        off_x -= MAX_WIDTH - width
    
    width += BORDER_WIDTH*4
    height += BORDER_WIDTH*4
    if drop_shadow:
        drop_shadow_distance = max(2, int(fontdesc.get_size()/pango.SCALE*0.1))
        width += drop_shadow_distance
        height += drop_shadow_distance
    darea.set_size_request(width, height)
    darea.realize()
    pixmap = gtk.gdk.Pixmap(darea.window, width, height)
    pixmap.set_colormap(darea.window.get_colormap())
    
    fg_gc = gdk.GC(pixmap); fg_gc.copy(darea.style.fg_gc[gtk.STATE_NORMAL])
    bg_gc = gdk.GC(pixmap); bg_gc.copy(darea.style.fg_gc[gtk.STATE_NORMAL])
    fg_gc.set_foreground(darea.get_colormap().alloc_color(fgcolor))
    bg_gc.set_background(darea.get_colormap().alloc_color(bgcolor))
    pixmap.draw_rectangle(bg_gc, True, 0, 0, width, height)
    pixmap.draw_layout(fg_gc, off_x, off_y, layout)

    if debug_frame:
        pixmap.draw_rectangle(fg_gc, False, 0, 0, width - 1, height - 1)

    bitmap = gtk.gdk.Pixmap(darea.window, width, height, 1)
    bitmap.set_colormap(darea.window.get_colormap())
    
    fg_gc = gdk.GC(bitmap)
    bg_gc = gdk.GC(bitmap)
    fg_gc.set_foreground(gdk.Color(pixel=-1))
    bg_gc.set_background(gdk.Color(pixel=0))

    if fake_translucent_bg:
        w, h = 2, 2
        stipple = gtk.gdk.Pixmap(None, w, h, 1)
        stipple.draw_rectangle(bg_gc, True, 0, 0, w, h)
        stipple.draw_point(fg_gc, 0, 0)
        stipple.draw_point(fg_gc, 1, 1)
        fg_gc.set_stipple(stipple)
        bitmap.draw_rectangle(bg_gc, True, 0, 0, width, height)
        fg_gc.set_fill(gtk.gdk.STIPPLED)
        bitmap.draw_rectangle(fg_gc, True, 0, 0, width, height)
        fg_gc.set_fill(gtk.gdk.SOLID)

        # draw corners
        
        corner_size = int(fontdesc.get_size()/pango.SCALE*0.5)
        fg_gc.set_function(gtk.gdk.AND)
        gc = gdk.GC(bitmap)
        corner = gtk.gdk.Pixmap(bitmap, corner_size, corner_size)
        def draw_corner(angle1, x, y, arc_x0, arc_y0):
            gc.set_foreground(gdk.Color(pixel=0))
            corner.draw_rectangle(gc, True, 0, 0, corner_size, corner_size)
            gc.set_foreground(gdk.Color(pixel=1))
            corner.draw_arc(gc, True, arc_x0, arc_y0, corner_size*2, corner_size*2,
                            angle1*64, 90*64)
            bitmap.draw_drawable(fg_gc, corner, 0, 0, x, y, corner_size, corner_size)
        # top-left
        draw_corner(90, 0, 0, 0, 0)
        # bottom-left
        draw_corner(180, 0, height - corner_size, 0, -corner_size)
        # bottom-right
        draw_corner(270, width - corner_size, height - corner_size, -corner_size, -corner_size)
        # top-right
        draw_corner(0, width - corner_size, 0, -corner_size, 0)
        
        fg_gc.set_function(gtk.gdk.SET)
    else:
        bitmap.draw_rectangle(bg_gc, True, 0, 0, width, height)
    bitmap.draw_layout(fg_gc, off_x, off_y, layout)
    bitmap.draw_layout(fg_gc, off_x + BORDER_WIDTH, off_y, layout)
    bitmap.draw_layout(fg_gc, off_x + BORDER_WIDTH, off_y + BORDER_WIDTH, layout)
    bitmap.draw_layout(fg_gc, off_x, off_y + BORDER_WIDTH, layout)
    bitmap.draw_layout(fg_gc, off_x - BORDER_WIDTH, off_y + BORDER_WIDTH, layout)
    bitmap.draw_layout(fg_gc, off_x - BORDER_WIDTH, off_y, layout)
    bitmap.draw_layout(fg_gc, off_x - BORDER_WIDTH, off_y - BORDER_WIDTH, layout)
    bitmap.draw_layout(fg_gc, off_x, off_y - BORDER_WIDTH, layout)
    bitmap.draw_layout(fg_gc, off_x + BORDER_WIDTH, off_y - BORDER_WIDTH, layout)

    if drop_shadow:
        bitmap.draw_layout(fg_gc, off_x + drop_shadow_distance,
                           off_y + drop_shadow_distance, layout)
    if debug_frame:
        bitmap.draw_rectangle(fg_gc, False, 0, 0, width - 1, height - 1)

    darea.window.set_back_pixmap(pixmap, False)
    win.window.shape_combine_mask(bitmap, 0, 0)
    win.width = width
    win.height = height

    # Set the overlay mode of the window
    pixmap = gdk.Pixmap(None, width, height, 1)
    win.input_shape_combine_mask(pixmap, 0, 0)

    return win

def popup(text, bgcolor=None, fgcolor=None, fontdesc=None, use_markup=False):
    assert isinstance(fontdesc, pango.FontDescription)
    win = gtk.Window(gtk.WINDOW_POPUP)
    win.set_border_width(0)
    frame = gobject.new(gtk.Frame, shadow_type=gtk.SHADOW_ETCHED_OUT,
                        visible=True)
    win.add(frame)
    label = gobject.new(gtk.Label, use_markup=True, label=text, visible=True)
    label.modify_font(fontdesc)
    
    frame.add(label)

    win.show()
    win.width, win.height = win.allocation.width, win.allocation.height
    return win


if __name__ == '__main__':
    w = osd("<i>Hello</i> <span size='larger' weight='bold'>World</span>"
            "<span foreground='red'>!</span> sad adasd asd asd as das asd"
            " asdasdasdashdjasdlasl dkasdaskdjakaskdjasdlsajldj", "#000000", "#80ff80",
            pango.FontDescription("sans serif 48"),
            use_markup=True, drop_shadow=True, debug_frame = True, ellipsize=pango.ELLIPSIZE_END)
    w.move(gdk.screen_width()/2 - w.width/2, gdk.screen_height() - w.height - 10)
    def motion(wid, ev):
        print "enter notify!"
    w.connect("enter-notify-event", motion)
    w.show()
    gtk.main()

