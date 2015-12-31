#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import gtk


BACK = [1,1,1,1]
FRONT = [0,0,0,0.8]
LIGHT = [0,0,0,0.2]
CYAN = [0,0.5,0.5,0.2]
BLUE = [0,0,1,0.3]


NMAX = 10**6
SIZE = 800
ONE = 1./SIZE
LINEWIDTH = ONE*1.1

INIT_NUM = 900
INIT_RAD = 0.45

SOURCE_DST = 3.0*ONE

FRAC_DOT = 0.90
FRAC_DST = 50.*ONE
FRAC_STP = ONE*4


SPAWN_ANGLE = 0.5
SPAWN_FACTOR = 0.7




def show(render,fractures):

  sources = fractures.sources
  alive_fractures = fractures.alive_fractures
  dead_fractures = fractures.dead_fractures

  def draw_sources():
    for s in sources:
      render.circle(*s, r=3*ONE, fill=True)

  def draw_lines(fracs):
    for frac in fracs:
      start = frac.inds[0]
      render.ctx.move_to(*sources[start,:])
      for c in frac.inds[1:]:
        render.ctx.line_to(*sources[c,:])
      render.ctx.stroke()

  render.clear_canvas()

  # render.ctx.set_source_rgba(*CYAN)
  # draw_sources()

  render.ctx.set_source_rgba(*LIGHT)
  render.set_line_width(3*LINEWIDTH)
  draw_lines(alive_fractures+dead_fractures)

  render.ctx.set_source_rgba(*FRONT)
  render.set_line_width(LINEWIDTH)
  draw_lines(alive_fractures+dead_fractures)


  # for f in alive_fractures:
    # for s in sources[f.inds,:]:
      # render.circle(*s, r=2*ONE, fill=False)



def main():

  from render.render import Animate
  from numpy.random import random
  from modules.fracture import Fractures

  F = Fractures(
    INIT_NUM,
    INIT_RAD,
    SOURCE_DST,
    FRAC_DOT,
    FRAC_DST,
    FRAC_STP
  )

  for _ in xrange(3):
    F.blow(2, random(size=2))

  def wrap(render):

    if F.i % 5 == 0:
      show(render,F)

    F.print_stats()
    res = F.step(dbg=True)
    n = F.spawn(factor=SPAWN_FACTOR, angle=SPAWN_ANGLE)
    print('spawned: {:d}'.format(n))

    # fn = './asdf_{:04d}.png'.format(F.i)
    # render.write_to_png(fn)

    # from dddUtils.ioOBJ import export_2d as export
    # vertices, paths = F.get_vertices_and_paths()
    # fn = './res/export.2obj'.format(F.i)
    # export('fractures', fn, vertices, lines=paths)

    return res

  render = Animate(SIZE, BACK, FRONT, wrap)

  def __write_svg_and_exit(*args):
    gtk.main_quit(*args)
    show(render,F)
    render.write_to_png('./res/on_exit.png')

    from dddUtils.ioOBJ import export_2d as export
    vertices, paths = F.get_vertices_and_paths()
    fn = './res/on_exit.2obj'.format(F.i)
    export('fractures', fn, vertices, lines=paths)

  render.window.connect("destroy", __write_svg_and_exit)

  gtk.main()


if __name__ == '__main__':

  main()

