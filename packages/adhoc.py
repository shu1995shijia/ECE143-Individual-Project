"""
Ad-Hoc Communications Network Installation
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

def generate_region(length, width):
    """
    Generate the rectangle region or region for communication tower installation.

    Args:
        length: The length of the region.
        width: The width of the region.
        
    Returns:
        The matrix initialized with all zeros as type <numpy.ndarray>.
    """
    assert isinstance(length, int) and isinstance(width, int), "Input should be integer type."
    assert length > 0 and width > 0, "Input should all be greater than zero."
    
    return np.zeros((length, width), dtype=int)

def generate_rand_num(lower, upper):
    """
    Randomly select one number from the supplied range/bounds(inclusive). Sampled from a uniform distribution.

    Args:
        lower (int): The lower limit of the range to draw random sample.
        upper (int): The upper limit of the range to draw random sample.
        
    Returns:
        sample (int): A sample(number) selected uniformly from the given bounds.
    """
    assert isinstance(upper, int) and isinstance(lower, int), "Input should be integer type."
    assert upper >= lower

    sample_list = np.array(range(lower, upper + 1))
    return np.random.choice(sample_list)

def generate_tower(region_size):
    """
    To create a new tower location with randomly chosen width and length.

    Args:
        region_size (tuple): The size tuple with length and width information (length, width).
        
    Returns:
        tower (dict): A dictionary object contains the location, length and width information.
    """
    tower = dict()
    tower['loc'] = (generate_rand_num(0, region_size[0] - 1), generate_rand_num(0, region_size[1] - 1))
    tower['length'] = generate_rand_num(1, region_size[0] - tower['loc'][0])
    tower['width'] = generate_rand_num(1, region_size[1] - tower['loc'][1])
    return tower

def place_tower(region, tower):
    # Update the canvas by placing the tower
    """
    To place the tower onto the overall region.

    Args:
        region (<numpy.ndarray>): The overall rectangle region.
        tower (dict):  A dictionary contains the location(key = 'loc'), length(key = 'length') and width(key = 'width').
        
    Returns:
        region_update (<numpy.ndarray>): A numpy.ndarray contains the updated overall region. Need to be trim latter.
    """
    loc, l, w = tower['loc'], tower['length'], tower['width']
    region_update = region.copy()
    region_update[loc[0] : loc[0] + l, loc[1] : loc[1] + w] +=  1
    return region_update

def update_tower_coverage(region, new_coverage):
    # Update the overall tower coverage on the given region
    """
    To update the tower coverage after the communication tower coverage has been trimmed.

    Args:
        region (<numpy.ndarray>): The region to install the communication tower.
        new_coverage (<numpy.ndarray>): The generated communication tower coverage.
        
    Returns:
        new_region (<numpy.ndarray>): The updated region with the provided new coverage added. 
                                      (The new region can only contains 0s and 1s in the matrix)
    """
    assert isinstance(region, np.ndarray)
    assert isinstance(new_coverage, np.ndarray)

    new_region = region + new_coverage
    return new_region


def max_histogram_area(histogram, row):
    # Cut the extra tower coverage
    """
    To find the maximum rect in a given histogram

    Args:
        histogram (list): A list contains the histogram.
        row (int): The current row index when scanning through the rows in the overall region.
        
    Returns:
        max_rect (int): A numpy.ndarray contains the updated overall region with the newly installed communication tower
        max_loc (dict): A dictionary contains the location(key = 'loc'), length(key = 'length') and width(key = 'width').
    """
    assert isinstance(histogram, np.ndarray)
    assert isinstance(row, int)

    i = 0 
    max_rect = -1
    max_loc = dict()
    stack = []
    for i in xrange(len(histogram) + 1):
        if i == 0: stack.append(i)
        elif i == len(histogram):
            while len(stack) != 0:           
                top = stack.pop()   
                if len(stack) == 0:
                    l, w = histogram[top], i
                else:
                    l, w = histogram[top], (i - stack[-1] - 1)
                rect_area = l * w 
                if rect_area > max_rect:
                    max_rect = rect_area
                    max_loc['loc'] = (row - histogram[top] + 1, i - w) # Not Sure !!!!
                    max_loc['length'] = l
                    max_loc['width'] = w
        elif histogram[i] < histogram[i - 1]:
            while len(stack) != 0 and histogram[stack[-1]] >= histogram[i]:           
                top = stack.pop()   
                if len(stack) == 0:
                    l, w = histogram[top], i
                else:
                    l, w = histogram[top], (i - stack[-1] - 1)
                rect_area = l * w 
                if rect_area > max_rect:
                    max_rect = rect_area
                    max_loc['loc'] = (row - histogram[top] + 1, i - w) # Not Sure !!!!
                    max_loc['length'] = l
                    max_loc['width'] = w
                if len(stack) == 0: break
            stack.append(i)
        else: 
            stack.append(i)
            # print stack

    return max_rect, max_loc


def find_max_rect(region):
    # Find the maximum non-overlappying rectangle on the canvas.
    """
    To find the maximum rectangle appeared in given area of interest.

    Args:
        region (<numpy.ndarray>): The rectangle area that contains 0s (represents blank space) and 1s (represents the area to combine as rectangle).
        
    Returns:
        max_rect (int): The maximum possible rectangle area consists 1s.
        max_loc (dict): A dictionary contains the location(key = 'loc'), length(key = 'length') and width(key = 'width') of the maximum rectangle
                        (representation of the maximum rectangle which could be used for trimming the coverage).
    """
    l, w = region.shape
    hist_region = np.zeros((l, w), dtype=int)
    hist_region[:] = region[:]
    #print hist_region
    max_rect, max_loc = max_histogram_area(hist_region[0, :], 0)
    #print "histogram", hist_region[0,:]
    for i in range(1, l):
        for j in range(w):
            if hist_region[i][j] != 0:
                hist_region[i][j] += hist_region[i - 1][j]
            else:
                hist_region[i][j] = 0
        
        tmp_max_rect, tmp_max_loc = max_histogram_area(hist_region[i,:], i)
        #print "histogram", hist_region[i,:]
        if tmp_max_rect > max_rect:
            max_rect, max_loc = tmp_max_rect, tmp_max_loc
            #print max_rect, i, j

    return max_rect, max_loc

def trim_tower(region, tower, show_coverage_update=False):
    # Cut the extra tower coverage
    """
    To trim the newly added tower and find a rectangle of the maximum size to monitor 
    the uncovered space left in the overall region.

    Args:
        region (<numpy.ndarray>): The overall rectangle region.
        tower (dict):  A dictionary contains the location(key = 'loc'), length(key = 'length') and width(key = 'width').
        
    Returns:
        trimmed_coverage (<numpy.ndarray>): A numpy.ndarray contains the whole region (marked as 0) and the maximum possible 
                                            trimmed coverage of the communication tower installed (marked as 1).
        tower_area (int): The area of the maximal area of the trimed tower coverage.
    """
    loc, l, w = tower['loc'], tower['length'], tower['width']
     # To prepare for finding the largest area of rectangle
    patch = np.zeros((l, w), dtype=int)
    patch[:] = region[loc[0] : loc[0] + l, loc[1] : loc[1] + w]
    #patch[patch == 1] = 1 # 1 represents open space
    patch[patch != 1] = 0 # 0 represents used space
    # Find the largest area of rectangle
    tower_area, tmp_tower_loc = find_max_rect(patch)
    # To calculate the new tower coverage
    tower_new = dict()
    tower_new['loc'] = (tmp_tower_loc['loc'][0] + loc[0], tmp_tower_loc['loc'][1] + loc[1])
    tower_new['length'] = tmp_tower_loc['length']
    tower_new['width'] = tmp_tower_loc['width']
    #print "Tower Area after trimming: ", tower_area
    
    if show_coverage_update == True:
        new_patch = np.zeros((l, w), dtype=int)
        new_patch = place_tower(new_patch, tmp_tower_loc)
        # Add the new coverage on a plane region map
        coverage_update_display = np.zeros(region.shape, dtype=int)
        coverage_update_display[loc[0] : loc[0] + l, loc[1] : loc[1] + w] = new_patch
        #print "The new tower coverage location info: ", tower_new
        #print "The trimmed tower coverage: \n", coverage_update_display

    return tower_area, tower_new

def full_coverage_generation(region, display=False, debug=False):
    target_area = region.shape[0] * region.shape[1]

    tower_num_need = 0
    coverage_area = 0

    while coverage_area != target_area:
            # Generate the new tower to be installed into the region
            tower = generate_tower(region.shape)
            # 
            region_update = place_tower(region, tower)
            # To keep the maximum possible coverage
            tower_area, tower_loc_new = trim_tower(region_update, tower)
            if tower_area != 0:
                tower_num_need += 1
                coverage_area  += tower_area
            # To update the region
            region = place_tower(region, tower_loc_new)

    return tower_num_need, coverage_area

   
def coverage_generation(region, tower_num, display=False, debug=False):
    # Generate the coverage map by inputing the desired coverage and a sequence of n  communication towers. 
    """
    Need to be added

    Args:
        region (<numpy.ndarray>): The overall rectangle region.
        target_area (int):  
        display (boolen): True for show the visualization. (Default=False)
    Returns:
        coverage_area (int): The total area of the coverage after execution
        coverage_map (<numpy.ndarray>): The updated region map with the new towers added.
    """
    target_area = region.shape[0] * region.shape[1]
    print target_area
    coverage_area = 0
    tower_cnt = 0
    if display == True: fig, ax = draw_region(region.shape)
    tower_loc_list = []
    while tower_num != tower_cnt:
            # Generate the new tower to be installed into the region
            tower = generate_tower(region.shape)

            if debug: print "The tower generated initially: \n", tower
            # 
            region_update = place_tower(region, tower)
            if debug: print "The region after inital tower placement: \n", region_update
            # To keep the maximum possible coverage
            tower_area, tower_loc_new = trim_tower(region_update, tower, show_coverage_update=debug)

            # To update the region
            if tower_area > 0: 
                tower_cnt += 1   
                tower_loc_list.append(tower_loc_new)
                if display == True: ax = draw_tower(ax, tower_loc_new)     
                region = place_tower(region, tower_loc_new)
                if np.sum(region[region > 1]) != 0:
                    print "Original_tower: ", tower
                    print tower_loc_new
                    print tower_loc_list
                    raise STOP
            coverage_area  += tower_area

            if coverage_area >= target_area:
                print "Coverage requirement met, ", coverage_area
                break
    print "Total tower used: ", tower_cnt
    percent_coverage = (coverage_area * 1.0 / target_area) * 100
    print "The overall percentage of coverage area: ", percent_coverage, "%"
    return coverage_area, region, percent_coverage, tower_loc_list


def draw_region(region_size):
    fig, ax = plt.subplots(1)
    print region_size[0]
    plt.ylim(region_size[0],0)
    plt.xlim(0,region_size[1])
    #ax.grid(color='r', linestyle='-', linewidth=1)
    return fig, ax

def draw_tower(ax, tower, color_selection=None):
    l, w = tower['length'], tower['width']
    loc_xy = (tower['loc'][1], tower['loc'][0])
    if color_selection == None:
        color_selection = (np.random.uniform(0,1), np.random.uniform(0,1), np.random.uniform(0,1))
        #color_selection = 'b'

    ax.add_patch(Rectangle(xy=loc_xy, height=l, width=w, color=color_selection, hatch='\\', ec=(0,0,0,1)))
    return ax














