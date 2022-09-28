#@title <font size=3><img src="https://exoplanets.nasa.gov/system/exotic/leftdownarrow_tall.png" height=18 hspace=8>2b. <b>Identify the target and comparison stars in a telescope image</b></font>

setupDisplay()

#########################################################

# Show the first telescope image in an interactive interface
def display_image(filename):
    #print(f"{filename}")
    hdu = fits.open(filename)

    dheader = dict(hdu[0].header)
  
    data = hdu[0].data
    megapixel_factor = (data.shape[0])*(data.shape[1])/1000000.0
    if megapixel_factor > 5:
      print(f"Downsampling image because it has {megapixel_factor} megapixels.")
      image_downscaled = downscale_local_mean(data, (2, 2)).astype(int)
      data = image_downscaled
    
    max_y = len(data)
    max_x = len(data[0])
    p_height = 500
    p_width = int((p_height/max_y) * max_x)

    # create a figure with text on mouse hover
    fig = figure(tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")], plot_width=p_width, plot_height=p_height,
        tools=[PanTool(),BoxZoomTool(),WheelZoomTool(),ResetTool(),HoverTool()])
    fig.x_range.range_padding = fig.y_range.range_padding = 0

    r = fig.multi_line('x', 'y', source={'x':[],'y':[]},color='white',line_width=3)
    fig.add_tools(FreehandDrawTool(renderers=[r]))

    # set up a colobar + data range
    color_mapper = LogColorMapper(palette="Cividis256", low=np.percentile(data, 55), high=np.percentile(data, 99))

    # must give a vector of image data for image parameter
    fig.image(
        image=[data],
          x=0, y=0, dw=hdu[0].data.shape[1], dh=hdu[0].data.shape[0],
          level="image", color_mapper=color_mapper
    )
    fig.grid.grid_line_width = 0.5

    color_bar = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),
                         label_standoff=12, border_line_color=None, location=(0,0))

    fig.add_layout(color_bar, 'right')

    show(fig)

#########################################################

display(HTML('<p class="bookend">START: Compare telescope image and star chart</p>'))
display(HTML('<ul class="step4">'))

# set up bokeh
bokeh.io.output_notebook()
sample_data = False

# set up image path
p = "sample-data/HatP32Dec202017"
#p = check_dir(os.path.join("/content/EXOTIC/exotic-in-action/", p))
p = os.path.join("/content/EXOTIC/exotic-in-action/", p)
output_dir = os.path.join(p, "EXOTIC_output/")      
         
#########################################################

# Find and show the images
inits = []    # array of paths to any inits files found in the directory

all_files_print = [f for f in sorted(os.listdir(p))]
all_files = [f for f in sorted(os.listdir(p)) if os.path.isfile(os.path.join(p, f))]
fits_count, first_image = 0, ""
for f in all_files:
  if re.search(r"\.f[itz]+s?\.?g?z?$", f, re.IGNORECASE):
    if first_image == "":
      first_image = os.path.join(p, f)
    fits_count += 1
  if re.search(r"\.json$", f, re.IGNORECASE):
    inits.append(os.path.join(p, f))

# show images
if fits_count >= 2:
  obs = ""
  # instructions for finding the target star
  display(HTML('''
  <h3>Data Entry 1 of 2: Enter coordinates for the target star</h3>
  <ol class="step">
  <li class="step4">In the right image, find the <i>crosshairs</i> in the center - that represents your target star.</li>
  <li class="step4">On the left image, <i>find this target star and roll over it with your mouse</i>, note the X and Y coordinates.</li>
  <li class="step4">Put the X and Y coordinates in the box below in the format <code>[x,y]</code> and press return.</li></ol>
  <p>Tip: Use the zoom feature. Click the magnifying glass and click-and-drag to draw a rectangle that matches the starchart.</p>

  <br />
  <div class="plots">
  <img align=right src="https://app.aavso.org/vsp/chart/X28194FDL.png" width=380>
  '''))
  display_image(first_image)
  display(HTML('</div><br clear="all"/>'))

  # request coordinates and verify the entries are valid
  success = False
  while not success:
    targ_coords = input("Enter coordinates for target star - [424,286] - and press return:  ")  

    # check syntax and coords
    tc_syntax = re.search(r"\[\d+,\d+\]$", targ_coords)
    if tc_syntax:
      tc_coords = re.findall("\d+", targ_coords)
      if 422 <= int(tc_coords[0]) <= 426 and 284 <= int(tc_coords[1]) <= 288:
        success = True
      else:
        display(HTML('<p class="output error">Try again, your coordinates are a bit off: ' + targ_coords + ' should be closer to [424,286]</p>'))
    else:
      display(HTML('<p class="output error">Try again, your syntax is not quite right: ' + targ_coords + ' needs to look like [424,286]</p>'))


  showProgress(2)

  # instructions for finding the comparison stars
  display(HTML('<p class="output">Target star coordinates saved to inits.json</p>'))
  display(HTML('<h3>Data Entry 2 of 2: Enter coordinates for at least two comparison stars.</h3>'))
  display(HTML('<ol class="step"><li class="step4">In the right image, find the stars <i>with numbers</i> that represent suggested comparison stars.</li><li class="step4">On the left image, <i>find and roll over each comparison star with your mouse</i> and note the coordinates.</li><li class="step4">Put the X and Y coordinates in the box below in the format <code>[[x1,y1][x2,y2]]</code> and press return.</li></ol>'))
  
  # request coordinates and verify the entries are valid
  success = False
  while not success:
    comp_coords = input("Enter coordinates for the comparison stars - [[326,365],[416,343]] - and press return:  ")  

    # check syntax
    cc_syntax = re.search(r"\[(\[\d+,\d+\],?)+\]$", comp_coords)
    if cc_syntax:
      #display(HTML('<p class="output">Syntax OK:  [[x1,y1],[x2,y2]] e.g. ' + comp_coords + '</p>'))
      success = True
    else:
      display(HTML('<p class="output error">Try again, your syntax is not quite right: ' + comp_coords + ' needs to look more like [[326,365],[416,343]]</p>'))

  showProgress(1)
  display(HTML('<p class="output">Comparison star coordinates saved to inits.json</p>'))
  display(HTML('<p class="output">Images and inits.json set up. Ready for EXOTIC data reduction/analysis</p>'))
  aavso_obs_code = ""

  if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

  #inits = [make_inits_file(planetary_params, p, output_dir, first_image, targ_coords, comp_coords, obs, aavso_obs_code, sample_data)]
  inits = [output_dir+"inits.json"]

  if not os.path.isdir(output_dir):    # Make the output directory if it does not exist already.
    os.mkdir(output_dir)
  output_dir_for_shell = output_dir.replace(" ", "\ ")

#print("Path to the inits file(s) that will be used:")

#for inits_file in inits:
#  print(inits_file)

num_inits = len(inits)


display(HTML('<p class="bookend">DONE: Compare telescope image and star chart. <b>You may move on to the next step.</b></p>'))


