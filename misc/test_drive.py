#! /usr/bin/python
#
# detect sharp corners in a path.
# (c) 2013 jnweiger@gmail.com, distribute under GPL-2.0
# 
# Usage: 
#  '-'           zoom out
#  '+'           zoom in
#  'f' ('F')     cursor forward (20 points)
#  'b' ('B')     cursor backwards (20 points)
#  '0'           cursor to first node
#  LMB           drag the graphics around
#  'p'           save 'output.pdf'
#
# Reference Manual:
# http://people.gnome.org/~gianmt/pygoocanvas/
# https://developer.gnome.org/goocanvas/unstable/
#
# Examples:
# http://nullege.com/codes/search/goocanvas.Ellipse

import sys
import gtk
from goocanvas import *
import cairo
import random

sys.path.append('.')
sys.path.append('..')
from silhouette.Strategy import MatFree

cut_vertical_zigzag = [[(5.0, 5.5), (4.9, 5.8), (4.6, 6.1), (4.2, 6.3), (3.7, 6.4), (3.2, 6.3), (2.8, 6.1), (2.5, 5.8), (2.4, 5.5), (2.5, 5.2), (2.8, 4.9), (3.2, 4.7), (3.7, 4.6), (4.2, 4.7), (4.6, 4.9), (4.9, 5.2), (5.0, 5.5), (5.0, 5.5)], [(2.4, 1.2), (0.7, 2.1), (5.9, 3.0), (5.3, 10.4), (6.6, 9.5), (6.7, 10.6), (8.2, 4.6), (8.5, 6.0), (9.1, 4.3), (10.6, 5.6), (10.3, 11.0), (11.3, 9.4), (11.9, 11.0), (12.0, 4.5), (17.6, 1.9), (16.9, 1.1), (2.4, 1.2)]]

cut_vertical_zigzag_big = [[(17.6, 26.8), (17.5, 27.9), (17.2, 28.9), (16.7, 29.8), (16.1, 30.6), (15.3, 31.2), (14.4, 31.7), (13.5, 32.0), (12.4, 32.1), (11.4, 32.0), (10.4, 31.7), (9.5, 31.2), (8.8, 30.6), (8.1, 29.8), (7.6, 28.9), (7.3, 27.9), (7.2, 26.8), (7.3, 25.8), (7.6, 24.8), (8.1, 23.9), (8.8, 23.1), (9.5, 22.5), (10.4, 22.0), (11.4, 21.7), (12.4, 21.5), (13.5, 21.7), (14.4, 22.0), (15.3, 22.5), (16.1, 23.1), (16.7, 23.9), (17.2, 24.8), (17.5, 25.8), (17.6, 26.8), (17.6, 26.8)], [(7.2, 1.1), (0.7, 6.3), (20.9, 11.9), (18.5, 56.1), (23.7, 50.7), (24.2, 57.3), (29.8, 21.5), (30.8, 30.0), (33.1, 19.7), (39.0, 27.2), (38.1, 59.6), (41.6, 50.5), (44.2, 59.6), (44.6, 20.6), (66.0, 5.3), (63.5, 0.4), (7.2, 1.1)]]

cut_stars = [[(.1,.1), (50,1), (55,55), (3,30), (.1,.9)], [(1,31),(3,30),(44,44),(55,55)], [(1.115547484444443, .9047956222222213), (10.226748977499998,
7.4399208438888875), (10.565074486006942, 8.35713915909722),
(10.744325588888888, 8.654524502222221), (10.74829029517361,
8.308048945104165), (10.576251919166666, 7.3462779936111104),
(9.75446755111111, 3.733597646666666)], [(5.447516268888889,
8.040548646666666), (9.064625246944445, 8.845782692222222),
(10.028122384201389, 9.011393399791666), (10.375291246666666,
9.00485005111111), (10.077216924131944, 8.828178662187499), (9.158279633055555,
8.496282819722222), (5.618714244444446, 7.401628579999999)],
[(7.195168066666667, 13.285033402222222), (9.701075516388888,
10.555142226111109), (10.326247061354167, 9.803534618472222),
(10.494164657777777, 9.499605926666666), (10.192125792118052,
9.669410178645835), (9.445226960833331, 10.299285239166666),
(6.727445975555555, 12.817311593333335)], [(12.610850797777776,
14.393765133333334), (11.49964934, 10.858639911666666), (11.161323994652777,
9.941421596458332), (10.982072975555555, 9.644036253333333),
(10.978108022326388, 9.990511814861112), (11.150146363055555,
10.952282797222221), (11.97193044888889, 14.56496339111111)],
[(16.278882013333334, 10.258012108888888), (12.66177296472222,
9.452778169166665), (11.698275977395832, 9.287167395451387),
(11.351107317777776, 9.293710704444443), (11.649181516840278,
9.470382137465279), (12.568118790277776, 9.802278076944441),
(16.107684037777776, 10.896932457777776)], [(14.531229933333334,
5.013527353333333), (12.02532283638889, 7.743418635277778),
(11.400151256145831, 8.495026176770834), (11.232233624444444,
8.798954828888888), (11.534272653263889, 8.629150660694442),
(12.281171568333333, 7.999275551666666), (14.998952588888889,
5.481249444444444)],
[(26.50000062222222, 9.499994698802027), (26.38212318656249,
10.083862443871473), (26.060660808611107, 10.560654954357585),
(25.583868381909713, 10.882117363177029), (25.0000008, 10.999994803246473),
(24.416133054930555, 10.882117363177029), (23.93934054444444,
10.560654954357585), (23.617878135625002, 10.083862443871473),
(23.500000695555556, 9.499994698802029), (23.617878135625002,
8.916126997829808), (23.93934054444444, 8.439334584357585),
(24.416133054930555, 8.117872272552031), (25.0000008, 7.999994876579808),
(25.583868381909713, 8.117872272552031), (26.060660808611107,
8.439334584357585), (26.38212318656249, 8.916126997829808), (26.50000062222222,
9.499994698802029), (26.50000062222222, 9.499994698802027)],
[(19.650427213333334, 4.178705705468693), (19.78811015347222,
4.516244550399249), (20.393146426111112, 5.2977940749131385),
(22.880160262222226, 8.08356398102425), (19.34480054916667, 6.875860938246471),
(18.387352025034723, 6.625260446024249), (18.021270931111115,
6.63095717213536), (18.277643930520835, 6.8901134779686934),
(19.13571057138889, 7.38063372713536), (22.499479173333334, 9.002610205468693),
(18.771063691111113, 9.23976210324647), (17.790595160208333,
9.374637576093694), (17.45455939555556, 9.51999494102425), (17.790591989618058,
9.66131326057286), (18.771056741388893, 9.786127004079805),
(22.499476915555558, 9.99737919213536), (19.145622956666674,
11.643282435190917), (18.29140263868056, 12.143100191197862),
(18.036571891111116, 12.405988096579806), (18.401105706111114,
12.407955225156192), (19.354701292777783, 12.148060445190916),
(22.880156311111115, 10.916426545468694), (20.411460390555554,
13.720506535468694), (19.813535888611117, 14.509173757343692),
(19.678705880000003, 14.849569978802027), (20.01624401055556,
14.711886368385361), (20.797794037777784, 14.10684963713536),
(23.58356415555556, 11.61983467213536), (22.375861818333338,
15.155195372968693), (22.125261493680554, 16.11264457619786),
(22.130958757777783, 16.478726825468694), (22.390114150798613,
16.22235356147564), (22.880634783611114, 15.364286126857582),
(24.502611791111118, 12.000514349913136), (24.739764500277786,
15.72892806824647), (24.874639915798618, 16.709396219913135),
(25.019997091111115, 17.045431869913138), (25.161315736979173,
16.709399434600638), (25.28612964805556, 15.72893473574647),
(25.497381906666668, 12.000514349913136), (27.14328525555556,
15.35436841463536), (27.64310294541667, 16.208588666475638),
(27.905990811111117, 16.46341937435758), (27.90795810284723,
16.09888555494786), (27.648063406666672, 15.145289937413137),
(26.416429542222225, 11.61983467213536), (29.220510378888893,
14.088530627968696), (30.009177627222222, 14.68645521369786),
(30.349573822222226, 14.821285385468693), (30.21189035291667,
14.483747087343694), (29.606853551111115, 13.702196945468692),
(27.11983738666667, 10.916426545468692), (30.65519692333334,
12.124128741579804), (31.612645584166675, 12.374729286718694), (31.978727,
12.369032507690912), (31.722353890347225, 12.109876986788136),
(30.864286689444448, 11.61935630546869), (27.500516782222228,
9.997378909913134), (31.228929795000003, 9.760226271302024),
(32.20939730284722, 9.625351340850635), (32.545432044444446,
9.479995021024246), (32.209400473437505, 9.33867595623258), (31.22893610972222,
9.21386186435758), (27.500516500000003, 9.002608794357581), (30.8543690125,
7.35670593935758), (31.708589070312502, 6.85688886685758), (31.96341926666667,
6.594002147690913), (31.5988859146875, 6.592034229774248), (30.6452908175,
6.85192856435758), (27.11983654, 8.083561441024246), (29.588531578611114,
5.279482191857582), (30.186456208437498, 4.490815618211749),
(30.32128668888889, 4.150420547690916), (29.98374783954861, 4.288103611302027),
(29.20219786083333, 4.893139901579805), (26.41642813111111, 7.380153878802027),
(27.62413325527778, 3.8447950300520266), (27.87473400767361,
2.8873466774582766), (27.86903719777778, 2.5212656201353605),
(27.609881002187496, 2.777638643357583), (27.119360678055557,
3.6357054509131386), (25.497383600000003, 6.999475894357583),
(25.260232160833333, 3.2710593855520265), (25.125357142187504,
2.290591424826332), (24.98000084, 1.9545566245798047), (24.83868141802083,
2.2905891251561936), (24.7138675775, 3.271053053190916), (24.502614613333336,
6.999472225468693), (22.856712746111114, 3.64562182963536),
(22.356895717708333, 2.791402425343694), (22.094009095555556,
2.5365722528020274), (22.09204101888889, 2.9011064395416106),
(22.35193551222222, 3.854701305218693), (23.58356838888889, 7.380155572135361),
(20.779488681111108, 4.91146003963536), (19.99082212951389, 4.313535744947861),
(19.650427213333334, 4.178705705468693), (19.650427213333334,
4.178705705468693)]]
cut_1_sharp_turn = [[(6.447013888888888, 1.7197916666666666), (2.7447450608333335, 1.8781719273333333), (1.7712151617013887, 1.9675756834166662), (1.4375694444444445, 2.0637499999999998), (1.7712129392013884, 2.15725412703125), (2.7447391341666667, 2.240002452083333), (6.447013888888888, 2.38125)]]
cut_2_sharp_turn = [[(1,2.1), (2,2), (2.5,1)], [(1,3.1), (2,3), (3,2.5)],
                    [(1,4.1), (2,4), (3,4.5)], [(1,5.1), (2,5), (2.5,6)]]

cut = cut_vertical_zigzag
#cut = cut_stars
#cut = cut_2_sharp_turn

if len(sys.argv) > 1:
  str=open(sys.argv[1]).readlines()
  cut=eval("".join(str), {}, {})
  print "loading from", sys.argv[1]


def print_pdf(c):
  # (x1,y1,x2,y2) = c.get_bounds()
  scale= 72/25.4 # PDF is at 72DPI, so this is 12 inch wide.
  width=300     # mm
  height=400    # mm
  width *= scale
  height *= scale
  surface = cairo.PDFSurface("output.pdf", width, height)
  ctx = cairo.Context(surface)
  ctx.scale(scale,scale)
  # ctx.set_source_rgb(1,1,1)
  # ctx.rectangle(0,0,width,height)
  # ctx.fill()
  # ctx.set_source_rgb(1,0,0)
  # ctx.move_to(width/2,height/2)
  # ctx.arc(width/2,height/2,512*0.25,0, 6)     # math.pi*2)
  # ctx.fill()
  c.render(ctx)
  ctx.show_page()
  print "output.pdf written"

def key_press(win, ev, c):
  new_idx = None
  s = c.get_scale()  
  key = chr(ev.keyval & 0xff)
  if   key == '+':  c.set_scale(s*1.2)
  elif key == '-':  c.set_scale(s*.8)
  elif key == 'p':  print_pdf(c)
  elif key == 'f':  new_idx = c.cursor_idx + 1
  elif key == 'F':  new_idx = c.cursor_idx + 20
  elif key == 'a':  new_idx = c.cursor_idx + 1
  elif key == 'b':  new_idx = c.cursor_idx - 1
  elif key == 'B':  new_idx = c.cursor_idx - 20
  elif key == 'r':  new_idx = 0
  elif key == '0':  new_idx = 0
  elif ev.keyval <= 255: gtk.main_quit()

  if new_idx is not None and (new_idx < 1 or  new_idx >= len(c.points)):
    new_idx = 1
    for a in c.arrows:
      a.remove()
    c.arrow = []
  else:
    print c.get_scale()

  if new_idx is not None:
    jumpto = True
    if key == 'f':
      jumpto = c.points[new_idx][1]
    elif key == 'b':
      jumpto = c.points[c.cursor_idx][1]
    ox = c.points[c.cursor_idx][0].x
    oy = c.points[c.cursor_idx][0].y
    c.cursor_idx = new_idx
    cx = c.points[c.cursor_idx][0].x
    cy = c.points[c.cursor_idx][0].y
    # GooCanvas.CanvasAnimateType.FREEZE = 0 
    if jumpto:
      c.cursor.set_simple_transform(cx,cy, 1, 0.)
    else:
      if key == 'f':
        ## place forward pointing arrows
        p = Points([(ox,oy),(cx,cy)])
        c.arrows.append(Polyline(parent=c.get_root_item(), points=p, line_width=0.3, end_arrow="True", stroke_color_rgba=0x00000033))
      c.cursor.animate(cx,cy, 1, -360., absolute=True, duration=150, step_time=30, type=0)
    print new_idx, c.points[c.cursor_idx][0].attr
  else:
    c.cursor.stop_animation()

def button_press(win, ev):
  win.click_x = ev.x
  win.click_y = ev.y

def button_release(win, ev):
  win.click_x = None
  win.click_y = None

def motion_notify(win, ev, c):
  try:
    # 3.79 is the right factor for units='mm'
    dx = (ev.x-win.click_x) / c.get_scale() / 3.79
    dy = (ev.y-win.click_y) / c.get_scale() / 3.79
    win.click_x = ev.x
    win.click_y = ev.y
    (x1,y1,x2,y2) = c.get_bounds()
    c.set_bounds(x1-dx,y1-dy,x2-dx,y2-dy)
  except:
    pass


def main ():
    win = gtk.Window()

    canvas = Canvas(units='mm', scale=10)
    canvas.set_size_request(800, 600)
    # canvas.set_bounds(0, 0, 120., 90.)
    root = canvas.get_root_item()

    win.connect("destroy", gtk.main_quit)
    win.connect("key-press-event", key_press, canvas)
    win.connect("motion-notify-event", motion_notify, canvas)
    win.connect("button-press-event", button_press)
    win.connect("button-release-event", button_release)

    mf = MatFree(preset='pyramids')
    new_cut = mf.apply(cut)

    canvas.points = [ None ]
    canvas.arrows = [ ]

    idx = 1
    for path in new_cut:
      for C in path:
        if 'attr' in C.__dict__ and 'sharp' in C.attr:
          Ellipse(parent=root, center_x=C.x, center_y=C.y, radius_x=.25, radius_y=.25, fill_color_rgba = 0xFF666644, line_width = 0.01)
          

        Ellipse(parent=root, center_x=C.x, center_y=C.y, radius_x=.2, radius_y=.2, line_width = 0.01)

      p = Points(path)
      poly = Polyline(parent=root, points=p, line_width=0.05, stroke_color="black")

      jumpto = True
      for C in path:
        text = Text(parent=root, text=idx, font="4", fill_color="blue")
        idx += 1
        canvas.points.append((C,jumpto))         # store to allow cursor movement.
        jumpto = False
        text.translate(C.x+random.uniform(-.1,0), C.y+random.uniform(-.1,0))
        text.scale(.05,.05)
      
    
    if len(canvas.points) <= 1:
      rect = Rect(parent=root, x=1, y=1, width=3,  height=2,
                  fill_color = '#77ff77', stroke_color = 'black', line_width = .01)
      print "Dummy rectangle drawn. No points in canvas."
    else:
      cursor_p = Points([(-0.5,0),(0,0.5),(0.5,0),(0,-0.5),(-0.5,0)])
      canvas.cursor = Polyline(parent=root, points=cursor_p, line_width=0.05, stroke_color="green", fill_color_rgba=0x77ff7777)
      canvas.cursor.translate(canvas.points[1][0].x,canvas.points[1][0].y)
      canvas.cursor_idx = 1
    
    # text = Text(parent=root, text="Hello World", font="12")
    # text.rotate(30,0,10)
    # text.scale(.05,.05)
                    
    win.add(canvas)
    win.show_all()
                                
    gtk.main()

if __name__ == "__main__":
    main ()
