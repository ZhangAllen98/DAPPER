
from common import *
from mods.QG.core import *

#########################
# Plotting
#########################

# Colormap -- darkened jet
cm_ = plt.cm.jet
cm  = mpl.colors.ListedColormap(0.85*cm_(arange(cm_.N)))

def liveplotter(stats,obs_inds=None):

  fig, axs = plt.subplots(2,2,sharex=True,sharey=True, num=plt.gcf().number,
      gridspec_kw={'left':0.125-0.04,'right':0.9-0.04})

  for ax in axs.flatten():ax.set_aspect('equal',adjustable_box_or_forced())

  ((ax_11, ax_12), (ax_21, ax_22)) = axs

  ax_11.grid(color='w',linewidth=0.2)
  ax_12.grid(color='w',linewidth=0.2)
  ax_21.grid(color='k',linewidth=0.1)
  ax_22.grid(color='k',linewidth=0.1)


  # Upper colorbar -- position relative to ax_12
  bb    = ax_12.get_position()
  dy    = 0.1*bb.height
  ax_13 = fig.add_axes([bb.x1+0.03, bb.y0 + dy, 0.04, bb.height - 2*dy])
  # Lower colorbar -- position relative to ax_22
  bb    = ax_22.get_position()
  dy    = 0.1*bb.height
  ax_23 = fig.add_axes([bb.x1+0.03, bb.y0 + dy, 0.04, bb.height - 2*dy])

  # Extract data arrays
  xx, yy, mu, var, err = stats.xx, stats.yy, stats.mu, stats.var, stats.err

  #square(xx[0])[3,3] = 99 # Debug

  # Plot
  # - origin='lower' might get overturned by set_ylim() below.
  im_11 = ax_11.imshow(square(mu[0])       , cmap=cm) 
  im_12 = ax_12.imshow(square(xx[0])       , cmap=cm)
  im_21 = ax_21.imshow(square(sqrt(var[0])), cmap=plt.cm.bwr) # hot is better, but needs +1 colorbar
  im_22 = ax_22.imshow(square(err[0])      , cmap=plt.cm.bwr)
  # Obs init -- a list where item 0 is the handle of something invisible.
  lh = list(ax_12.plot(nx/2,ny/2)[0:1])
  
  sx = '$\\psi$'
  ax_11.set_title('mean '+sx)
  ax_12.set_title('true '+sx)
  ax_21.set_title('std. '+sx)
  ax_22.set_title('err. '+sx)

  for ax in axs.flatten():
    lims = (1, nx-2) # crop boundries (which should be 0, i.e. yield harsh q gradients).
    step = (nx - 1)/8
    ticks = arange(step,nx-1,step)
    ax.set_xlim  (lims)
    ax.set_ylim  (lims[::-1])
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

  im_11.set_clim(-40,40)
  im_12.set_clim(-40,40)
  im_21.set_clim(-10,10)
  im_22.set_clim(-10,10)

  fig.colorbar(im_12,cax=ax_13)
  fig.colorbar(im_22,cax=ax_23)
  for ax in [ax_13, ax_23]:
    ax.yaxis.set_tick_params('major',length=2,width=0.5,direction='in',left=True,right=True)

  # Title
  title = "Streamfunction ("+sx+")"
  fig.suptitle(title)
  # Time info
  tt = stats.setup.t.tt
  time_info = ["   t=%g"%tt[0], "   k=%d"%0, "kObs=N/A"] 
  txt = ax_12.text(1, 1.1, "\n".join(time_info),
      transform=ax_12.transAxes,family='monospace',ha='left')

  def update(k,kObs):
    t = tt[k]

    im_11.set_data(square(mu[k])        )
    im_12.set_data(square(xx[k])        )
    im_21.set_data(square(sqrt(var[k])) )
    im_22.set_data(square(err[k])       )

    # Remove previous obs
    try:
      lh[0].remove()
    except ValueError:
      pass
    # Plot current obs. 
    #  - plot() automatically adjusts to direction of y-axis in use.
    #  - ind2sub returns (iy,ix), while plot takes (ix,iy) => reverse.
    if kObs is not None and obs_inds is not None:
      lh[0] = ax_12.plot(*ind2sub(obs_inds(t))[::-1],'k.',ms=1,zorder=5)[0]

    # Time info
    time_info = ["   t=%g"%t, "   k=%d"%k, "kObs="+ ("-" if kObs is None else str(kObs))] 
    txt.set_text("\n".join(time_info))

    plt.pause(0.01)

  return update


