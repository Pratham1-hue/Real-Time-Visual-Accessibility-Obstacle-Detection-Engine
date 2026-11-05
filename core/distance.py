def estimate_distance(box):
    x1, y1, x2, y2 = box
    pixel_width = x2 - x1
    
    if pixel_width == 0:
        return 99.9

    # These are approximations. For production, you'd map 'known_width' dynamically 
    # based on the class (e.g., a car is wider than a person) and calibrate focal_length.
    known_width = 0.5  # average obstacle width in meters
    focal_length = 600 # rough camera focal length

    distance = (known_width * focal_length) / pixel_width
    return distance