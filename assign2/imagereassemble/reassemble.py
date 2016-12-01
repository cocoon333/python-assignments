#!/usr/bin/env python3 -tt
"""
File: reassemble.py
-------------------
Assignment 2: Quest for the Holy Grail
Course: CS 41
Name: <YOUR NAME>
SUNet: <SUNet ID>

Replace this with a description of the program.

The choice of how you implement this module is entirely up to you!
You have a hand not only in the program implementation, but also
in the program design. As such, take a moment to plan out your approach
to this problem. How will you merge the image slices? You can import any
builtin libraries you need (i.e. itertools, operator, etc), but do not
use any 3rd party libraries (outside of Pillow, which we've provided
through the imageutils module)

Best of luck! Now go find that Holy Grail.
"""
import imageutils

def pixel_diff(p1, p2):
    assert (type(p1) is imageutils.Pixel)
    assert (type(p2) is imageutils.Pixel)
    #return imageutils.Pixel(abs(p1.red-p2.red), abs(p1.green-p2.green), abs(p1.blue-p2.blue), 255)
    return (abs(p1.red-p2.red) +  abs(p1.green-p2.green) + abs(p1.blue-p2.blue))

def edge_diff(e1, e2):
    return sum([pixel_diff(p1, p2) for (p1, p2) in zip(e1, e2)])

def reduce_image_column(x, y):
    assert(type(x) is list)
    assert(type(y) is list)
    assert(type(x[0]) is list)
    assert(type(y[0]) is list)
    assert(type(x[0][0]) is imageutils.Pixel)
    assert(type(y[0][0]) is imageutils.Pixel)
    #assert (len(x) == len(y))
    assert (len(x[0]) == len(y[0]))
    #res = []
    #for i in xrange(len(x)):
    #    res.append(x[i]+y[i])
    return x + y


def combine_images(dir):
    l = imageutils.files_in_directory(dir)
    data = map(imageutils.load_image, l)
    res = []
    edges = [x[0] for x in data]
    edges += [x[-1] for x in data]

    num_image = len(data)
    for i in xrange(num_image):
        for j in xrange(num_image, 2*num_image):
            if i + num_image ==  j:
                continue
            ledge = edges[i]
            redge = edges[j]
            assert(type(ledge) is list)
            assert(type(redge) is list)
            assert(type(ledge[0]) is imageutils.Pixel)
            assert(type(redge[0]) is imageutils.Pixel)
            res.append(edge_diff(ledge, redge))
    start = 0
    right_neighbor_dict = {}
    for i in range(0, (num_image)*(num_image-1), num_image-1):
        m = min(res[i:i+num_image-1])
        left = i / (num_image-1)
        right = res[i:i+num_image-1].index(m)
        if right >= left:
            right += 1
        if m >= 100000:
            right_neighbor_dict[left] = ()
            continue
        right_neighbor_dict[left] = right
    print right_neighbor_dict
    print len(right_neighbor_dict.keys())

    values_set = set()
    for value in right_neighbor_dict.values():
        if type(value) == tuple:
            continue
        values_set.add(value)
    for key in right_neighbor_dict.keys():
        if key not in values_set:
            start = key
    print values_set
    print start

    ordered_image = []
    for i in xrange(num_image):
        ordered_image.insert(0, data[start])
        start = right_neighbor_dict[start]
    print len(ordered_image)

    '''
    counter = 0
    reset_counter_times = 0
    min = res[0]
    directions_for_unshredding = {}
    for i in res:
        if counter == reset_counter_times:
            counter += 1
        if i < min:
            directions_for_unshredding[reset_counter_times] = [counter, min]
            min = i
        if counter == 19:
            counter = 0
            reset_counter_times += 1
            min = res[reset_counter_times*18+1]
            continue
        counter += 1
    return directions_for_unshredding
    '''
    res = reduce(reduce_image_column, ordered_image)
    
    imageutils.save_image(res, 'hi.png')

if __name__ == '__main__':
    combine_images('shredded/destination/')
    #combine_images('shredded/grail4/')
    #combine_images('shredded/grail20/')
