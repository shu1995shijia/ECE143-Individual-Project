"""
Ad-Hoc Communications Network Installation
"""
import numpy as np

def generate_region(length, width):
    """
    Generate the rectangle region or region for communication tower installation.

    Args:
        length: The length of the region.
        width: The width of the region.
        
    Returns:
        The matrix initialized with all zeros as type <numpy.ndarray>.
    
    Raises:
        KeyError: Raises an exception.
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
    
    Raises:
        KeyError: Raises an exception.
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
    
    Raises:
        KeyError: Raises an exception.
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
    
    Raises:
        KeyError: Raises an exception.
    """
    loc, l, w = tower['loc'], tower['length'], tower['width']
    region_update = region.copy()
    region_update[loc[0] : loc[0] + l, loc[1] : loc[1] + w] +=  1
    return region_update

def update_tower_coverage(region, new_coverage):
    # Update the overall tower coverage on the given region
    region = region + new_coverage
    return region


def max_histogram_area(histogram, row):
    # Cut the extra tower coverage
    """
    To find the maximum rect in a given histogram

    Args:
        histogram (list): A list contains the histogram.
        
    Returns:
        max_rect (int): A numpy.ndarray contains the updated overall region with the newly installed communication tower
        max_loc (dict): A dictionary contains the location(key = 'loc'), length(key = 'length') and width(key = 'width').
    
    Raises:
        KeyError: Raises an exception.
    """
    assert isinstance(histogram, np.ndarray)
    assert isinstance(row, int)

    i = 0 
    max_rect = -1
    max_loc = dict()
    stack = []
    for i in xrange(len(histogram) + 1):
        if i == 0:
            stack.append(i)

        elif i == len(histogram) or histogram[i] < histogram[i - 1]:
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
            stack.append(i)
        else: 
            stack.append(i)
            # print stack
    return max_rect, max_loc


def find_max_rect(region):
    # Find the maximum non-overlappying rectangle on the canvas.
    l, w = region.shape
    hist_region = np.zeros((l, w), dtype=int)
    hist_region[:] = region[:]
    #print hist_region
    max_rect, max_loc = max_histogram_area(hist_region[0, :], 0)

    for i in range(1, l):
        for j in range(w):
            if hist_region[i][j] != 0:
                hist_region[i][j] = hist_region[i - 1][j] + 1
            else:
                hist_region[i][j] = 0
        
        tmp_max_rect, tmp_max_loc = max_histogram_area(hist_region[i,:], i)
        if tmp_max_rect > max_rect:
            max_rect, max_loc = tmp_max_rect, tmp_max_loc

    return max_rect, max_loc

    

def trim_tower(region, tower):
    # Cut the extra tower coverage
    """
    To trim the newly added tower and find a rectangle of the maximum size to monitor 
    the uncovered space left in the overall region.

    Args:
        region (<numpy.ndarray>): The overall rectangle region.
        tower (dict):  A dictionary contains the location(key = 'loc'), length(key = 'length') and width(key = 'width').
        
    Returns:
        region_update (<numpy.ndarray>): A numpy.ndarray contains the updated overall region with the newly installed communication tower
        tower_install (dict): A dictionary contains the location(key = 'loc'), length(key = 'length') and width(key = 'width').
    
    Raises:
        KeyError: Raises an exception.
    """
    print region
    print "Original Tower Location: ", tower
    loc, l, w = tower['loc'], tower['length'], tower['width']
     # To prepare for finding the largest area of rectangle
    patch = np.zeros((l, w), dtype=int)
    patch[:] = region[loc[0] : loc[0] + l, loc[1] : loc[1] + w]
    patch[patch == 1] = 1 # 1 represents open space
    patch[patch > 1] = 0 # 0 represents used space
    # Find the largest area of rectangle
    tower_area, tmp_tower_loc = find_max_rect(patch)
    new_patch = np.zeros((l, w), dtype=int)
    
    new_patch = place_tower(new_patch, tmp_tower_loc)
    # Add the new coverage on a plane region map
    trimmed_coverage = np.zeros(region.shape, dtype=int)
    trimmed_coverage[loc[0] : loc[0] + l, loc[1] : loc[1] + w] = new_patch
    print "Most recent added tower loaciton: ", tower
    print "Trimed Tower Area: ", tower_area
    print "Trimmed Coverage Map: "
    print trimmed_coverage
    #print new_patch

    return trimmed_coverage

    





   
def coverage_generation():
    # Generate the coverage map by inputing the desired coverage and a sequence of n  communication towers. 
    pass
def coverage_generation_random():
    # Generate a list of towers by inputting the desired coverage. 
    pass
