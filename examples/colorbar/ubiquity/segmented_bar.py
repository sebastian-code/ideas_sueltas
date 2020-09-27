#
# segmented_bar.py
#
# Original author:
#   Aaron Bockover <abockover@novell.com>
#
# Translated to Python and further modifications by:
#   Evan Dandrea <evand@ubuntu.com>
#
# Copyright (C) 2008 Novell, Inc.
# Copyright (C) 2008 Canonical Ltd.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import gobject
from gtk import gdk
import gtk
import math
import cairo
import pango
import pangocairo
from ubiquity.misc import format_size
from ubiquity.misc import find_in_os_prober


class Color:
    def __init__(self, r, g, b, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a


class CairoCorners:
    none = 0
    top_left = 1
    top_right = 2
    bottom_left = 4
    bottom_right = 8
    all = 15


class CairoExtensions:
    @staticmethod
    def modula(number, divisor):
        return int((number % divisor) + (number - int(number)))

    @staticmethod
    def gdk_color_to_cairo_color(color, alpha=1.0):
        return Color(
            (color.red >> 8) / 255.0,
            (color.green >> 8) / 255.0,
            (color.blue >> 8) / 255.0,
            alpha,
        )

    @staticmethod
    def color_from_hsb(hue, saturation, brightness):
        hue_shift = [0, 0, 0]
        color_shift = [0, 0, 0]
        if brightness <= 0.5:
            m2 = brightness * (1 + saturation)
        else:
            m2 = brightness + saturation - brightness * saturation
        m1 = 2 * brightness - m2
        hue_shift[0] = hue + 120
        hue_shift[1] = hue
        hue_shift[2] = hue - 120
        color_shift[0] = brightness
        color_shift[1] = brightness
        color_shift[2] = brightness
        if saturation == 0:
            i = 3
        else:
            i = 0
        while i < 3:
            m3 = hue_shift[i]
            if m3 > 360:
                m3 = CairoExtensions.modula(m3, 360)
            elif m3 < 0:
                m3 = 360 - CairoExtensions.modula(abs(m3), 360)

            if m3 < 60:
                color_shift[i] = m1 + (m2 - m1) * m3 / 60
            elif m3 < 180:
                color_shift[i] = m2
            elif m3 < 240:
                color_shift[i] = m1 + (m2 - m1) * (240 - m3) / 60
            else:
                color_shift[i] = m1
            i = i + 1

        return Color(color_shift[0], color_shift[1], color_shift[2])

    @staticmethod
    def hsb_from_color(color):
        red = color.r
        green = color.g
        blue = color.b
        hue = 0
        saturation = 0
        brightness = 0

        if red > green:
            ma = max(red, blue)
            mi = min(green, blue)
        else:
            ma = max(green, blue)
            mi = min(red, blue)

        brightness = (ma + mi) / 2

        if abs(ma - mi) < 0.0001:
            hue = 0
            saturation = 0
        else:
            if brightness <= 0.5:
                saturation = (ma - mi) / (ma + mi)
            else:
                saturation = (ma - mi) / (2 - ma - mi)
            delta = ma - mi
            if red == max:
                hue = (green - blue) / delta
            elif green == max:
                hue = 2 + (blue - red) / delta
            elif blue == max:
                hue = 4 + (red - green) / delta
            hue = hue * 60
            if hue < 0:
                hue = hue + 360
        return (hue, saturation, brightness)

    @staticmethod
    def color_shade(color, ratio):
        # FIXME evand 2008-07-19: This function currently produces only deep
        # reds for non-white colors.
        return color
        h, s, b = CairoExtensions.hsb_from_color(color)
        b = max(min(b * ratio, 1), 0)
        s = max(min(s * ratio, 1), 0)
        c = CairoExtensions.color_from_hsb(h, s, b)
        c.a = color.a
        return c

    @staticmethod
    def rgba_to_color(color):
        # FIXME evand 2008-07-19: We should probably match the input of
        # rgb_to_color.
        a = ((color >> 24) & 0xFF) / 255.0
        b = ((color >> 16) & 0xFF) / 255.0
        c = ((color >> 8) & 0xFF) / 255.0
        d = (color & 0x000000FF) / 255.0
        return Color(a, b, c, d)

    @staticmethod
    def rgb_to_color(color):
        # FIXME evand 2008-07-19: Should we assume a hex string or should we
        # copy Hyena and require a hex number?
        r, g, b = color[:2], color[2:4], color[4:]
        r, g, b = [(int(n, 16) / 255.0) for n in (r, g, b)]
        return Color(r, g, b)
        # return CairoExtensions.rgba_to_color((color << 8) | 0x000000ff)

    @staticmethod
    def rounded_rectangle(
        cr, x, y, w, h, r, corners=CairoCorners.all, top_bottom_falls_through=False
    ):
        if top_bottom_falls_through and corners == CairoCorners.none:
            cr.move_to(x, y - r)
            cr.line_to(x, y + h + r)
            cr.move_to(x + w, y - r)
            cr.line_to(x + w, y + h + r)
        elif r < 0.0001 or corners == CairoCorners.none:
            cr.rectangle(x, y, w, h)

        if (
            corners & (CairoCorners.top_left | CairoCorners.top_right)
        ) == 0 and top_bottom_falls_through:
            y = y - r
            h = h + r
            cr.move_to(x + w, y)
        else:
            if (corners & CairoCorners.top_left) != 0:
                cr.move_to(x + r, y)
            else:
                cr.move_to(x, y)

            if (corners & CairoCorners.top_right) != 0:
                cr.arc(x + w - r, y + r, r, math.pi * 1.5, math.pi * 2)
            else:
                cr.line_to(x + w, y)

        if (
            corners & (CairoCorners.bottom_left | CairoCorners.bottom_right)
        ) == 0 and top_bottom_falls_through:
            h = h + r
            cr.line_to(x + w, y + h)
            cr.move_to(x, y + h)
            cr.line_to(x, y + r)
            cr.arc(x + r, y + r, r, math.pi, math.pi * 1.5)
        else:
            if (corners & CairoCorners.bottom_right) != 0:
                cr.arc(x + w - r, y + h - r, r, 0, math.pi * 0.5)
            else:
                cr.line_to(x + w, y + h)

            if (corners & CairoCorners.bottom_left) != 0:
                cr.arc(x + r, y + h - r, r, math.pi * 0.5, math.pi)
            else:
                cr.line_to(x, y + h)

            if (corners & CairoCorners.top_left) != 0:
                cr.arc(x + r, y + r, r, math.pi, math.pi * 1.5)
            else:
                cr.line_to(x, y)


class SegmentedBar(gtk.Widget):
    __gtype_name__ = "SegmentedBar"

    def __init__(self):
        gtk.Widget.__init__(self)

        # State
        self.segments = []
        self.layout_width = 0
        self.layout_height = 0

        # Properties
        self.bar_height = 26
        self.bar_label_spacing = 8
        self.segment_label_spacing = 16
        self.segment_box_size = 12
        self.segment_box_spacing = 6
        self.h_padding = 0

        self.show_labels = True
        self.reflect = True
        self.remainder_color = "eeeeee"

        self.disk_size = 0

    def add_segment(self, title, size, color, show_in_bar=True):
        self.do_size_allocate(self.get_allocation())
        self.disk_size += size
        self.segments.append(self.Segment(title, size, color, show_in_bar))
        self.queue_draw()

    def remove_segment(self, title):
        """Remove a segment.  Not present in the original SegmentedBar."""
        for segment in self.segments:
            if segment.title == title:
                self.segments.remove(segment)
                self.disk_size -= size
                self.queue_draw()
                break

    def remove_all(self):
        self.segments = []
        self.disk_size = 0
        self.queue_draw()

    def add_segment_rgb(self, title, size, rgb_color):
        self.add_segment(title, size, CairoExtensions.rgb_to_color(rgb_color))

    def do_size_request(self, requisition):
        requisition.width = 200
        requisition.height = 0

    def do_realize(self):
        self.set_flags(self.flags() | gtk.REALIZED)
        self.window = gdk.Window(
            self.get_parent_window(),
            width=self.allocation.width,
            height=self.allocation.height,
            window_type=gdk.WINDOW_CHILD,
            wclass=gdk.INPUT_OUTPUT,
            event_mask=self.get_events() | gdk.EXPOSURE_MASK,
        )
        self.window.set_user_data(self)
        self.style.attach(self.window)
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)

    # def do_unrealize(self):
    #    # FIXME evand 2008-07-19: Is overloading this function really
    #    # necessary?  Python's garbage collector should be able to handle
    #    # destroying the window.  Check other PyGTK programs.
    #    self.window.set_user_data(None)
    #    self.window.destroy()

    def compute_layout_size(self):
        layout = None
        self.layout_height = 0
        self.layout_width = 0

        for i in range(len(self.segments)):
            layout = self.create_adapt_layout(layout, False, True)
            title = self.segments[i].title
            layout.set_text(title)
            aw, ah = layout.get_pixel_size()

            layout = self.create_adapt_layout(layout, True, False)
            layout.set_text(self.segments[i].subtitle)
            bw, bh = layout.get_pixel_size()

            w = max(aw, bw)
            h = ah + bh

            self.segments[i].layout_width = w
            self.segments[i].layout_height = max(h, self.segment_box_size * 2)

            if i < (len(self.segments) - 1):
                self.layout_width = (
                    self.layout_width
                    + self.segments[i].layout_width
                    + self.segment_box_size
                    + self.segment_box_spacing
                    + self.segment_label_spacing
                )
            else:
                self.layout_width = (
                    self.layout_width
                    + self.segments[i].layout_width
                    + self.segment_box_size
                    + self.segment_box_spacing
                    + 0
                )
            self.layout_height = max(self.layout_height, self.segments[i].layout_height)

    def do_size_allocate(self, allocation):
        if self.reflect:
            bar_height = int(math.ceil(self.bar_height * 1.75))
        else:
            bar_height = self.bar_height

        if self.show_labels:
            self.compute_layout_size()
            h = max(
                self.bar_height + self.bar_label_spacing + self.layout_height,
                bar_height,
            )
            w = self.layout_width + (2 * self.h_padding)
            self.set_size_request(w, h)
        else:
            self.set_size_request(bar_height, self.bar_height + (2 * self.h_padding))
        gtk.Widget.do_size_allocate(self, allocation)

    def render_bar_segments(self, cr, w, h, r):
        grad = cairo.LinearGradient(0, 0, w, 0)
        last = 0.0

        for segment in self.segments:
            percent = segment.size / float(self.disk_size)
            if percent > 0:
                grad.add_color_stop_rgb(
                    last, segment.color.r, segment.color.g, segment.color.b
                )
                last = last + percent
                grad.add_color_stop_rgb(
                    last, segment.color.r, segment.color.g, segment.color.b
                )

        CairoExtensions.rounded_rectangle(cr, 0, 0, w, h, r, corners=CairoCorners.none)
        cr.set_source(grad)
        cr.fill_preserve()

        grad = cairo.LinearGradient(0, 0, 0, h)
        grad.add_color_stop_rgba(0.0, 1, 1, 1, 0.125)
        grad.add_color_stop_rgba(0.35, 1, 1, 1, 0.255)
        grad.add_color_stop_rgba(1, 0, 0, 0, 0.4)

        cr.set_source(grad)
        cr.fill()

    def make_segment_gradient(self, h, color, diag=False):
        grad = cairo.LinearGradient(0, 0, 0, h)
        c = CairoExtensions.color_shade(color, 1.1)
        grad.add_color_stop_rgba(0.0, c.r, c.g, c.b, c.a)
        c = CairoExtensions.color_shade(color, 1.2)
        grad.add_color_stop_rgba(0.35, c.r, c.g, c.b, c.a)
        c = CairoExtensions.color_shade(color, 0.8)
        grad.add_color_stop_rgba(1, c.r, c.g, c.b, c.a)
        return grad

    def render_bar_strokes(self, cr, w, h, r):
        stroke = self.make_segment_gradient(
            h, CairoExtensions.rgba_to_color(0x00000040)
        )
        seg_sep_light = self.make_segment_gradient(
            h, CairoExtensions.rgba_to_color(0xFFFFFF20)
        )
        seg_sep_dark = self.make_segment_gradient(
            h, CairoExtensions.rgba_to_color(0x00000020)
        )

        cr.set_line_width(1)
        seg_w = 20
        if seg_w > r:
            x = seg_w
        else:
            x = r

        while x <= w - r:
            cr.move_to(x - 0.5, 1)
            cr.line_to(x - 0.5, h - 1)
            cr.set_source(seg_sep_light)
            cr.stroke()

            cr.move_to(x + 0.5, 1)
            cr.line_to(x + 0.5, h - 1)
            cr.set_source(seg_sep_dark)
            cr.stroke()
            x = x + seg_w

        CairoExtensions.rounded_rectangle(
            cr, 0.5, 0.5, w - 1, h - 1, r, corners=CairoCorners.none
        )
        cr.set_source(stroke)
        cr.stroke()

    def render_labels(self, cr):
        if len(self.segments) == 0:
            return
        text_color = CairoExtensions.gdk_color_to_cairo_color(
            self.get_style().fg[self.state]
        )
        box_stroke_color = Color(0, 0, 0, 0.6)
        x = 0
        layout = None

        for segment in self.segments:
            cr.set_line_width(1)
            cr.rectangle(
                x + 0.5, 2 + 0.5, self.segment_box_size - 1, self.segment_box_size - 1
            )
            grad = self.make_segment_gradient(
                self.segment_box_size, segment.color, True
            )
            cr.set_source(grad)
            cr.fill_preserve()
            cr.set_source_rgba(
                box_stroke_color.r,
                box_stroke_color.g,
                box_stroke_color.b,
                box_stroke_color.a,
            )
            cr.stroke()

            x = x + self.segment_box_size + self.segment_box_spacing

            layout = self.create_adapt_layout(layout, False, True)
            layout.set_text(segment.title)
            (lw, lh) = layout.get_pixel_size()

            cr.move_to(x, 0)
            text_color.a = 0.9
            cr.set_source_rgba(text_color.r, text_color.g, text_color.b, text_color.a)
            pc = pangocairo.CairoContext(cr)
            pc.show_layout(layout)
            cr.fill()

            layout = self.create_adapt_layout(layout, True, False)
            layout.set_text(segment.subtitle)

            cr.move_to(x, lh)
            text_color.a = 0.75
            cr.set_source_rgba(text_color.r, text_color.g, text_color.b, text_color.a)
            pc = pangocairo.CairoContext(cr)
            pc.show_layout(layout)
            cr.fill()
            x = x + segment.layout_width + self.segment_label_spacing

    def render_bar(self, w, h):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(s)
        self.render_bar_segments(cr, w, h, h / 2)
        self.render_bar_strokes(cr, w, h, h / 2)
        pattern = cairo.SurfacePattern(s)
        return pattern

    def do_expose_event(self, event):
        if not isinstance(event.window, gdk.Window):
            # FIXME evand 2008-07-19: This will fail as Widget.do_expose_event
            # is a virtual function.  Why do we even need to do this anyway?
            # Are we not guaranteed that the event has a parent window?
            print "The event did not possess a gdk window."
            return gtk.Widget.do_expose_event(self, event)

        cr = self.window.cairo_create()
        if self.reflect:
            cr.push_group()
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.translate(self.allocation.x + self.h_padding, self.allocation.y)
        cr.rectangle(
            0,
            0,
            self.allocation.width - self.h_padding,
            max(
                2 * self.bar_height,
                self.bar_height + self.bar_label_spacing + self.layout_height,
            ),
        )
        cr.clip()

        bar = self.render_bar(
            self.allocation.width - 2 * self.h_padding, self.bar_height
        )

        cr.save()
        cr.set_source(bar)
        cr.paint()
        cr.restore()

        if self.reflect:
            cr.save()
            cr.rectangle(
                0,
                self.bar_height,
                self.allocation.width - self.h_padding,
                self.bar_height,
            )
            cr.clip()
            matrix = cairo.Matrix(xx=1, yy=-1)
            matrix.translate(0, -(2 * self.bar_height) + 1)
            cr.transform(matrix)
            cr.set_source(bar)

            mask = cairo.LinearGradient(0, 0, 0, self.bar_height)
            c = Color(0, 0, 0, 0)
            mask.add_color_stop_rgba(0.25, c.r, c.g, c.b, c.a)
            c = Color(0, 0, 0, 0.125)
            mask.add_color_stop_rgba(0.5, c.r, c.g, c.b, c.a)
            c = Color(0, 0, 0, 0.4)
            mask.add_color_stop_rgba(0.75, c.r, c.g, c.b, c.a)
            c = Color(0, 0, 0, 0.7)
            mask.add_color_stop_rgba(1.0, c.r, c.g, c.b, c.a)

            cr.mask(mask)
            cr.restore()
            cr.pop_group_to_source()
            cr.paint()
        if self.show_labels:
            if self.reflect:
                cr.translate(
                    self.allocation.x + (self.allocation.width - self.layout_width) / 2,
                    self.allocation.y + self.bar_height + self.bar_label_spacing,
                )
            else:
                cr.translate(
                    -self.h_padding + (self.allocation.width - self.layout_width) / 2,
                    self.bar_height + self.bar_label_spacing,
                )
            self.render_labels(cr)

        return True

    pango_size_normal = 0

    def create_adapt_layout(self, layout, small, bold):
        # FIXME evand 2008-07-19: Is this still broken?  Boldfaced text does
        # not seem to be working, and while it renders properly otherwise, that
        # may just be dumb luck.
        if not layout:
            context = self.create_pango_context()
            layout = pango.Layout(context)
            fd = layout.get_context().get_font_description()
            self.pango_size_normal = fd.get_size()
        else:
            fd = layout.get_context().get_font_description()

        if small:
            fd.set_size(int(fd.get_size() * pango.SCALE_SMALL))
        else:
            fd.set_size(self.pango_size_normal)

        if bold:
            fd.set_weight(pango.WEIGHT_BOLD)
        else:
            fd.set_weight(pango.WEIGHT_NORMAL)
        layout.context_changed()
        return layout

    class Segment:
        def __init__(self, device, size, color, show_in_bar=True):
            self.device = device
            self.title = ""
            if device.startswith("/"):
                self.title = find_in_os_prober(device)
            if self.title:
                self.title = "%s (%s)" % (self.title, device)
            else:
                self.title = device
            self.set_size(size)
            self.color = color
            self.show_in_bar = show_in_bar

            self.layout_width = 0
            self.layout_height = 0

        def __eq__(self, obj):
            if self.device == obj:
                return True
            else:
                return False

        def set_size(self, size):
            self.size = size
            if size > 0:
                self.subtitle = format_size(self.size)
            else:
                self.subtitle = ""


gobject.type_register(SegmentedBar)


class SegmentedBarSlider(SegmentedBar):
    __gtype_name__ = "SegmentedBarSlider"

    def __init__(self):
        SegmentedBar.__init__(self)
        self.slider_size = 16
        self.resize = -1
        self.device = None
        self.connect("motion-notify-event", self.motion_notify_event)

        self.part_size = 0

    def set_device(self, device):
        self.device = device

    def add_segment_rgb(self, title, percent, rgb_color):
        SegmentedBar.add_segment_rgb(self, title, percent, rgb_color)
        i = 0
        for s in self.segments:
            if self.device == s:
                self.resize = i
                break
            i = i + 1

        # FIXME: Should be done in some sort of expose event, so it doesn't
        # matter if the min_size is set after the segments are added.
        if self.resize != -1 and len(self.segments) > self.resize + 1:
            sum = self.segments[self.resize].size + self.segments[self.resize + 1].size
            self.segments[self.resize].set_size(self.max_size)
            self.segments[self.resize + 1].set_size(sum - self.max_size)
            self.queue_draw()

    def motion_notify_event(self, widget, event):
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state

        if not (state & gtk.gdk.BUTTON1_MASK) or self.resize == -1:
            return

        i = 0
        resize_part_start = 0
        while i < self.resize:
            resize_part_start += self.segments[i].size
            i += 1
        sum = self.segments[self.resize].size + self.segments[self.resize + 1].size
        b = x / float(self.allocation.width - self.h_padding)

        # The minimum size the old partition can be.
        if self.min_size != -1:
            a = (self.min_size + resize_part_start) / float(self.disk_size)
            if b < a:
                self.segments[self.resize].set_size(self.min_size)
                self.segments[self.resize + 1].set_size(sum - self.min_size)
                self.queue_draw()
                return
        else:
            # FIXME
            return

        # The maximum size the old partition can be.
        if self.max_size != -1:
            a = (self.max_size + resize_part_start) / float(self.disk_size)
            if b > a:
                self.segments[self.resize].set_size(self.max_size)
                self.segments[self.resize + 1].set_size(sum - self.max_size)
                self.queue_draw()
                return
        else:
            # FIXME
            return

        s = (b - (resize_part_start / float(self.disk_size))) * self.disk_size
        self.segments[self.resize].set_size(s)
        self.segments[self.resize + 1].set_size(sum - s)

        self.queue_draw()

    def set_min(self, m):
        self.min_size = m

    def set_max(self, m):
        self.max_size = m

    def set_part_size(self, size):
        self.part_size = size

    def get_size(self):
        return int(self.segments[self.resize].size)

    def do_realize(self):
        self.set_flags(self.flags() | gtk.REALIZED)
        self.window = gdk.Window(
            self.get_parent_window(),
            width=self.allocation.width,
            height=self.allocation.height,
            window_type=gdk.WINDOW_CHILD,
            wclass=gdk.INPUT_OUTPUT,
            event_mask=self.get_events()
            | gdk.EXPOSURE_MASK
            | gdk.BUTTON1_MOTION_MASK
            | gdk.BUTTON_PRESS_MASK
            | gdk.POINTER_MOTION_MASK
            | gdk.POINTER_MOTION_HINT_MASK,
        )
        self.window.set_user_data(self)
        self.style.attach(self.window)
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)

    def render_slider(self, cr, w, h, r):
        i = 0
        size = 0.0
        while i <= self.resize:
            size += self.segments[i].size
            i += 1
        t = size / float(self.disk_size)
        p = (t * w) - ((self.slider_size / w) / 2)

        grad = cairo.LinearGradient(0, 0, 0, h)
        c = CairoExtensions.rgb_to_color("f4f1ef")
        grad.add_color_stop_rgb(0, c.r, c.g, c.b)
        c = CairoExtensions.rgb_to_color("f2efec")
        grad.add_color_stop_rgb(0.5, c.r, c.g, c.b)
        c = CairoExtensions.rgb_to_color("ece7e2")
        grad.add_color_stop_rgb(0.5, c.r, c.g, c.b)
        c = CairoExtensions.rgb_to_color("e8e2dc")
        grad.add_color_stop_rgb(1, c.r, c.g, c.b)
        CairoExtensions.rounded_rectangle(
            cr,
            p - (self.slider_size / 2),
            0,
            self.slider_size,
            h,
            r / 2,
            corners=CairoCorners.all,
        )
        cr.set_source(grad)
        cr.fill_preserve()
        c = CairoExtensions.rgb_to_color("9f9890")
        cr.set_source_rgb(c.r, c.g, c.b)
        cr.set_line_width(1)

        # Handle
        cr.move_to(p - 2, (h / 4))
        cr.line_to(p - 2, h - (h / 4))
        cr.move_to(p + 2, (h / 4))
        cr.line_to(p + 2, h - (h / 4))
        cr.stroke()

    def render_bar(self, w, h):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(s)
        self.render_bar_segments(cr, w, h, h / 2)
        self.render_bar_strokes(cr, w, h, h / 2)
        if self.resize != -1:
            self.render_slider(cr, w, h, h / 2)
        pattern = cairo.SurfacePattern(s)
        return pattern


gobject.type_register(SegmentedBarSlider)
