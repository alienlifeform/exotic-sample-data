#@title <font face="Helvetica" class="button" color='#702020'>&lt;- Click to run the data reduction for HAT-P-32 b</font> { vertical-output: true }

importCustomStyles()

# If the user presses enter to run the sample data, download sample data if needed and
# put it into a sample-data directory at the top level of the user's Gdrive.  Count
# the .fits files (images) and .json files (inits files) in the directory entered 
# by the user (or in the sample-data directory if the user pressed enter).  If 
# there are at least 20 .fits files, assume this is a directory of images and display
# the first one in the series.  If there is exactly one inits file in the directory, 
# show the specified target and comp coords so that the user can check these against
# the displayed image.  Otherwise, prompt for target / comp coords and make an inits 
# file based  on those (save this new inits file in the folder with the output files 
# so that the student can consult it later).  Finally, run EXOTIC with the newly-made 
# or pre-existing inits file, plus any other inits files in the directory.

#########################################################

def display_image(filename):
    #print(f"{filename}")
    hdu = fits.open(filename)

# replace 0's with extension      # Stuff to put in if the hdul ever becomes a problem.    
#    extension = 0
#    image_header = hdul[extension].header
#    while image_header["NAXIS"] == 0:
#      extension += 1
#      image_header = hdul[extension].header

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

    # quick hot pixel/ cosmic ray mask
    # mask, cdata = detect_cosmics(
    #     data, psfmodel='gauss',
    #     psffwhm=4, psfsize=2*round(4)+1, # just a guess
    #     sepmed=False, sigclip = 4.25,
    #     niter=3, objlim=10, cleantype='idw', verbose=False
    # )

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

def floats_to_ints(l):
  while (True):
#    print (l)
    m = re.search(r"^(.*?)(\d+\.\d+)(.*?)$", l)
    if m:
      start, fl, end = m.group(1), float(m.group(2)), m.group(3)
      l = start+str("%.0f" % fl)+end
    else:
      return(l)
  
#########################################################

# Find a field in the image fits header or prompt the user to enter the corresponding
# value.

def check_dir(p):
  p = p.replace("\\", "/")

  if not(os.path.isdir(p)):
    print(f"Problem: the directory {p} doesn't seem to exist")
    print("on your Gdrive filesystem.")
    return("")
  return(p)

#########################################################

def add_sign(var):
  str_var = str(var)
  m=re.search(r"^[\+\-]", str_var)
  if m:
    return(str_var)
  if float(var) >= 0:
    return(str("+%.6f" % float(var)))
  else:
    return(str("-%.6f" % float(var)))

#########################################################

def get_val(hdr, ks):
  for key in ks:
    if key in hdr.keys():
      return hdr[key]
    if key.lower() in hdr.keys():
      return hdr[key.lower()]
    new_key = key[0]+key[1:len(key)].lower()  # first letter capitalized
    if new_key in hdr.keys():
      return hdr[new_key]
  return("")

#########################################################

def process_lat_long(val, key):
  m = re.search(r"\'?([+-]?\d+)[\s\:](\d+)[\s\:](\d+\.?\d*)", val)
  if m:
    deg, min, sec = float(m.group(1)), float(m.group(2)), float(m.group(3))
    if deg < 0:
      v = deg - (((60*min) + sec)/3600)
    else:
      v = deg + (((60*min) + sec)/3600)
    return(add_sign(v))
  m = re.search("^\'?([+-]?\d+\.\d+)", val)
  if m:
    v = float(m.group(1))
    return(add_sign(v))
  else:
    print(f"Cannot match value {val}, which is meant to be {key}.")

#########################################################

# Convert a MicroObservatory timestamp (which is in local time) to UTC.

def convert_Mobs_to_utc(datestamp, latitude, longitude, height):

#  print(datestamp)
  t = Time(datestamp[0:21], format='isot', scale='utc')
  t -= 0.33

  return(str(t)[0:10])

#########################################################

def find (hdr, ks, obs):
  # Special stuff for MObs and Boyce-Astro Observatories
  boyce = {"FILTER": "ip", "LATITUDE": "+32.6135", "LONGITUD": "-116.3334", "HEIGHT": 1405 }
  mobs = {"FILTER": "V", "LATITUDE": "+37.04", "LONGITUD": "-110.73", "HEIGHT": 2606 }

  if "OBSERVAT" in hdr.keys() and hdr["OBSERVAT"] == 'Whipple Observatory':
    obs = "MObs"

#  if "USERID" in hdr.keys() and hdr["USERID"] == 'PatBoyce':
#    obs = "Boyce"

  if obs == "Boyce":
    boyce_val = get_val(boyce, ks)
    if (boyce_val != ""):
      return(boyce_val)
  if obs == "MObs":
    mobs_val = get_val(mobs, ks)
    if (mobs_val != ""):
      return(mobs_val)

  val = get_val(hdr, ks)

  if ks[0] == "LATITUDE" and val != "":         # Because EXOTIC needs these with signs shown.
    return(process_lat_long(str(val), "latitude"))
  if ks[0] == "LONGITUD" and val != "":
    return(process_lat_long(str(val), "longitude"))

  if (val != ""):
    return(val)

  print(f"\nI cannot find a field with any of these names in your image header: \n{ks}.")
  print("Please enter the value (not the name of the header field, the actual value) that should")
  print("be used for the value associated with this field.\n")
  if ks[0] == "HEIGHT":
    print("The units of elevation are meters.")
  
  value = input("")

  return(value)

###############################################

def look_for_calibration(image_dir):
  darks_dir, flats_dir, biases_dir = "null", "null", "null"

  m = re.search(r"(.*?)(\d\d\d\d\-\d\d\-\d\d)\/images", image_dir)  # This handles the way I set up the MObs image paths for my seminar teams.
  if m:
    prefix, date = m.group(1), m.group(2)
    darks = prefix+date+"/darks"
    if os.path.isdir(darks):
      darks_dir = str("\""+darks+"\"")
      
  d_names = ["dark", "darks", "DARK", "DARKS", "Dark", "Darks"]  # Possible names for calibration image directories.
  f_names = ["flat", "flats", "FLAT", "FLATS", "Flat", "Flats"]
  b_names = ["bias", "biases", "BIAS", "BIASES", "Bias", "Biases"]

  for d in d_names:
    if os.path.isdir(os.path.join(image_dir, d)):
      darks_dir = str("\""+os.path.join(image_dir, d)+"\"")
      break

  for f in f_names:
    if os.path.isdir(os.path.join(image_dir, f)):
      flats_dir = str("\""+os.path.join(image_dir, f)+"\"")
      break

  for b in b_names:
    if os.path.isdir(os.path.join(image_dir, b)):
      biases_dir = str("\""+os.path.join(image_dir, b)+"\"")
      break

  return(darks_dir, flats_dir, biases_dir)

###############################################

# Writes a new inits file into the directory with the output plots.  This prompts
# for needed information that it cannot find in the fits header of the first image.

def make_inits_file(planetary_params, image_dir, output_dir, first_image, targ_coords, comp_coords, obs, aavso_obs_code, sample_data):
  inits_file_path = output_dir+"inits.json"
  hdul = fits.open(first_image)
  hdr = dict(hdul[0].header)

  min, max = "null", "null"
  filter = find(hdr, ['FILTER', 'FILT'], obs)
  if filter == "w":
    filter = "PanSTARRS-w"
    min = "404"
    max = "846"
  if filter == "Clear":
    filter = "V"
  if filter == "ip":
    min = "690"
    max = "819"
  if filter == "EXO":
    filter = "CBB"
  if re.search(r"Green", filter, re.IGNORECASE):
    filter = "SG"
    
  date_obs = find(hdr,["DATE", "DATE_OBS", "DATE-OBS"], obs)
  date_obs = date_obs.replace("/", "_")
  longitude = find(hdr,['LONGITUD', 'LONG', 'LONGITUDE', 'SITELONG'],obs)
  latitude = find(hdr,['LATITUDE', 'LAT', 'SITELAT'],obs)
  height = int(find(hdr, ['HEIGHT', 'ELEVATION', 'ELE', 'EL', 'OBSGEO-H', 'ALT-OBS', 'SITEELEV'], obs))
  obs_notes = "N/A"
  sec_obs_code = "N/A"

  mobs_data = False
  # For MObs, the date is local rather than UTC, so convert.
  if "OBSERVAT" in hdr.keys() and hdr["OBSERVAT"] == 'Whipple Observatory':
    date_obs = convert_Mobs_to_utc(date_obs, latitude, longitude, height)
    weather = hdr["WEATHER"] 
    temps = float(hdr["TELTEMP"]) - float(hdr["CAMTEMP"])
    obs_notes = str("First image seeing %s (0: poor, 100: excellent), Teltemp - Camtemp %.1f.  These observations were conducted with MicroObservatory, a robotic telescope network managed by the Harvard-Smithsonian Center for Astrophysics on behalf of NASA's Universe of Learning. This work is supported by NASA under award number NNX16AC65A to the Space Telescope Science Institute." % (weather, temps))
    sec_obs_code = "MOBS"  
    mobs_data = True
  
  if aavso_obs_code == "":
      aavso_obs_code = "N/A"

  obs_date = date_obs[0:10]
  (darks_dir, flats_dir, biases_dir) = look_for_calibration(image_dir)

  with open(inits_file_path, 'w') as inits_file:
    inits_file.write("""
{
  %s,
    "user_info": {
            "Directory with FITS files": "%s",
            "Directory to Save Plots": "%s",
            "Directory of Flats": %s,
            "Directory of Darks": %s,
            "Directory of Biases": %s,

            "AAVSO Observer Code (N/A if none)": "%s",
            "Secondary Observer Codes (N/A if none)": "%s",

            "Observation date": "%s",
            "Obs. Latitude": "%s",
            "Obs. Longitude": "%s",
            "Obs. Elevation (meters)": %d,
            "Camera Type (CCD or DSLR)": "CCD",
            "Pixel Binning": "1x1",
            "Filter Name (aavso.org/filters)": "%s",
            "Observing Notes": "%s",

            "Plate Solution? (y/n)": "y",
            "Align Images? (y/n)": "y",

            "Target Star X & Y Pixel": %s,
            "Comparison Star(s) X & Y Pixel": %s
    },    
    "optional_info": {
            "Pixel Scale (Ex: 5.21 arcsecs/pixel)": null,
            "Filter Minimum Wavelength (nm)": %s,
            "Filter Maximum Wavelength (nm)": %s
    }
}
""" % (planetary_params, image_dir, output_dir, flats_dir, darks_dir, biases_dir, 
       aavso_obs_code, sec_obs_code, obs_date, latitude, longitude, height, filter, 
       obs_notes, targ_coords, comp_coords, min, max))

  print("\nWithin your folder of images, there is now a new folder called EXOTIC_output.")
  print("This folder contains an initialization file for EXOTIC called inits.json.")
  print("The same folder will contain the output files and images when EXOTIC finishes running.")

  if not mobs_data:  
    print(f"\nThe inits.json file currently says that your observatory latitude was {latitude} deg,")
    print(f"longitude was {longitude} deg, and elevation was {height}m.  \n")
    print("*** If any of these are incorrect, please change them in the inits.json file. ***")
    print("*** (Please make sure that Western longitudes have a negative sign! ***")
    print("*** TheSkyX sometimes stamps Western longitudes as positive; this needs to be switched! ***\n")

  #print("\nNOTE: At this point in EXOTIC, you would have the opportunity change parameters in the inits file.")

  #print("\nIf you want to change anything in the inits file, please do that now.")
  #print("When you are done, press enter to continue.")
  #okay = input()

  return(inits_file_path)

#########################################################

# p is the name of the folder entered by the user.  Decide what to do based on what
# is found in the folder.
display(HTML('<p class="bookend">START: Analyzing sample data</p>'))
#display(HTML("<p class='warning'>NOTE: At this point in EXOTIC, you would have the opportunity choose where to temporarily save the sample data. For this exercise, we're downloading to /content/EXOTIC/exotic-quick-start/sample-data/HatP32Dec202017"))
display(HTML('<ul class="step5">'))


bokeh.io.output_notebook()
sample_data = False

#p = input("Press enter to run the HAT-P-32 b sample data, or enter a path as described above.")

# Is there a way to download this without a google drive? like a public but self-deleting google drive?
p = ""

display(HTML('<li class="step5">Ensuring we have sample data</li>'))

if p == "":
  sample_data = True
  if os.path.isdir("/content/EXOTIC/exotic-quick-start/sample-data/HatP32Dec202017"):
    print("It looks like you already have sample data, no need to download it again.")
  else:
    !git clone https://github.com/rzellem/EXOTIC_sampledata.git /content/EXOTIC/exotic-quick-start/sample-data

  p = "sample-data/HatP32Dec202017"

p = check_dir(os.path.join("/content/EXOTIC/exotic-quick-start/", p))
output_dir = os.path.join(p, "EXOTIC_output/")      
                                         
inits = []    # array of paths to any inits files found in the directory
files = [f for f in sorted(os.listdir(p)) if os.path.isfile(os.path.join(p, f))]
fits_count, first_image = 0, ""
for f in files:
  if re.search(r"\.f[itz]+s?\.?g?z?$", f, re.IGNORECASE):
    if first_image == "":
      first_image = os.path.join(p, f)
    fits_count += 1
  if re.search(r"\.json$", f, re.IGNORECASE):
    inits.append(os.path.join(p, f))

display(HTML('<li class="step5">Found ' + str(fits_count) + ' image files and ' + str(len(inits)) + ' initialization files in the directory</li>'))

if fits_count >= 19:                  # more than 20 images in the folder --> run EXOTIC on these images
  if len(inits) == 1:                 # one inits file exists
    inits_path = os.path.join(p, inits[0])
    with open(inits_path) as i_file:
      inits_data = i_file.read()
      d = json.loads(inits_data)
      targ_coords = d["user_info"]["Target Star X & Y Pixel"]
      comp_coords = d["user_info"]["Comparison Star(s) X & Y Pixel"]
      input_dir = d["user_info"]["Directory with FITS files"]
      if input_dir != p:
        print(f"The directory with fits files should be {p} but your inits file says {input_dir}.")
        print("This may or may not cause problems.  Just letting you know.")
      print(f"Coordinates from your inits file:\ntarget: {targ_coords}\ncomps: {comp_coords}")
      output_dir = d["user_info"]["Directory to Save Plots"]
      
  else:                               # no inits file: display image and prompt for target, comp coords;
                                      # then make an inits file and put it into the output directory (with the plots)
    #print("There are either 0 or > 1 inits files in your image directory, so we'll make a new one.")
    print("Displaying first image:")

    display(HTML('<hr />'))
    display(HTML('<div class="plots">'))
    display(HTML('<img align=right src="https://app.aavso.org/vsp/chart/X28194FDL.png" width=380>'))
    display_image(first_image)
    display(HTML('</div>'))

    obs = ""
    display(HTML('<hr /><br /><li class="step5"><b>STEP 1: Identify the target star</b></li>'))
    display(HTML('<p class="step">In the right image, find the <i>crosshairs</i> in the center that represent the target star. On the left image, roll over the target star with your mouse and note the coordinates. Put them in the box below as follows <code>[425,286]</code>.</p>'))
    targ_coords = input("")  
    if targ_coords != "[425,286]":
      display(HTML('<p class="step">You entered ' + targ_coords))
      targ_coords = "[425,286]"

    display(HTML('<hr /><br /><li class="step5"><b>STEP 2: Identify the comparison star(s).</b></li>'))
    display(HTML('<p>In the right image, find the stars <i>with numbers</i> that represent suggested comparison stars. On the left image, roll over each comparison star with your mouse and note the coordinates. Put them in the box below as follows <code>[[493,304],[415,343]]</code>.</p>'))
    comp_coords = input("")
    if comp_coords != "[[493,304],[415,343]]":
      display(HTML('<p class="step">You entered ' + comp_coords))
      comp_coords = "[[493,304],[415,343]]"

    aavso_obs_code = ""
    if not sample_data:
      print("If you have an AAVSO Observer code, enter it here.")
      print("If not (or if you are not sure), just press enter.")
      aavso_obs_code = input()
#    print("If you want an alternate output directory, type it here.")
#    alt_out = input()
#    if (re.search(r"\w", alt_out)):
#      output_dir = alt_out
    if not os.path.isdir(output_dir):
      os.mkdir(output_dir)
    inits = [make_inits_file(planetary_params, p, output_dir, first_image, targ_coords, comp_coords, obs, aavso_obs_code, sample_data)]

  if not os.path.isdir(output_dir):    # Make the output directory if it does not exist already.
    os.mkdir(output_dir)
  output_dir_for_shell = output_dir.replace(" ", "\ ")

# At this point, we have made an inits file if needed and are ready to run it.
# Or, if there were < 20 images in the directory (meaning that the directory was 
# only contained inits files, we'll run those one-by-one.

print("Path to the inits file(s) that will be used:")

for inits_file in inits:
  print(inits_file)

num_inits = len(inits)

commands = []
for inits_file in inits:
  with open(inits_file) as i_file:
    inits_data = i_file.read()
    d = json.loads(inits_data)
    date_obs = d["user_info"]["Observation date"]
    planet = d["planetary_parameters"]["Planet Name"]
    output_dir = d["user_info"]["Directory to Save Plots"]
    if not os.path.isdir(output_dir):
      os.mkdir(output_dir)
    inits_file_for_shell = inits_file.replace(" ", "\\ ")
    run_exotic = str(f"exotic -red {inits_file_for_shell} -ov")
    debug_exotic_run = str(f"!exotic -red \"{inits_file}\" -ov")

    commands.append({"inits_file_for_shell": inits_file_for_shell, "output_dir": output_dir, 
                      "planet": planet, "date_obs": date_obs, 
                      "run_exotic": run_exotic, "debug_exotic_run": debug_exotic_run
                      })
    print(f"{debug_exotic_run}")
    !eval "$run_exotic"

    # Only show lightcurve for beginner - bm
    lightcurve = os.path.join(output_dir,"FinalLightCurve_"+planet+"_"+date_obs+".png")
    fov = os.path.join(output_dir,"temp/FOV_"+planet+"_"+date_obs+"_LinearStretch.png")
    triangle = os.path.join(output_dir,"temp/Triangle_"+planet+"_"+date_obs+".png")
    print(f"lightcurve: {lightcurve}\nfov: {fov}\ntriangle: {triangle}\n")

    if not (os.path.isfile(lightcurve) and os.path.isfile(fov) and os.path.isfile(triangle)):
      print(f"Something went wrong with {planet} {date_obs}.\nCopy the command below into a new cell and run to find the error:\n{debug_exotic_run}\n")
      continue

    imageA = widgets.Image(value=open(lightcurve, 'rb').read())
    imageB = widgets.Image(value=open(fov, 'rb').read())
    hbox = HBox([imageB, imageA])
    # removing for "see it in action" - bm
    #display(hbox)
    #display(Image(filename=triangle))

display(HTML('</ul>'))

display(HTML('<p class="bookend">DONE: Analyzing sample data. <b>You may move on to the next step.</b></p>'))

    