import sys
import cv2
import numpy as np
import multiprocess as mp
import time

process_count = 4
single_process = False

if len(sys.argv) >= 2 and int(sys.argv[1]) <= mp.cpu_count():  #checking, if the right value was entered
    process_count = int(sys.argv[1])
    if len(sys.argv) >= 3 and sys.argv[2] == 's':
        single_process = True
elif len(sys.argv) < 2:
    pass
    #print(f'Aviable are {mp.cpu_count()}. Running on default {process_count} cores.')
else:
    print(f'Error occured. Aviable are {mp.cpu_count()}, but entered {sys.argv[1]}. Running on default {process_count} cores.')
    sys.argv[1] = process_count  #if the false value entered, sets the default value
    
def sort_filter(e):  #filter, that filters array from dictionary by first value, which is the key
    return e[0]


def brightness(particle, beta):   #brightness. beta is the value of brightness. returns editted value
  particle = np.array(particle)
  bright = cv2.convertScaleAbs(particle, beta=beta)
  
  return bright
""" 
def sharpness(particle):    #sharpness. takes only fne argument
    #specified values for sharpness
    kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
    particle = np.array(particle)
    img_sharpen = cv2.filter2D(src=particle, ddepth=-1, kernel=kernel)
    
    return img_sharpen
"""
def contrast(particle, alpha):   #gets specifid contrast value. 1.0 is default
    new_particle = np.zeros(particle.shape, particle.dtype) 
    for y in range(particle.shape[0]):  
        for x in range(particle.shape[1]):
            for z in range(particle.shape[2]):
                new_particle[y, x, z] = np.clip(alpha*particle[y, x, z], 0, 255)    
                
    return new_particle

def hdr(particle):  #hdr. takes only one argument
    particle = np.array(particle)
    #specific values
    hdr = cv2.detailEnhance(particle, sigma_s=12, sigma_r=0.15)
    
    return hdr

def process_img(id, img_particle, tasks_done=None, return_list=None):
    if img_particle is not None:
        start_count = time.time()
        if id == 0 or id == 4:
            #contrast(img_particle, 1.0)
            part = hdr(img_particle)  #1.0
        elif id == 1 or id == 5:
            part = hdr(img_particle)
        elif id == 2 or id == 6:
            part = brightness(img_particle, -60)
        elif id == 3 or id == 7:
            part = brightness(img_particle, -60)
        #specified dictionary, given in init function
        if single_process is False:
            return_list[f'{id}'] = np.vstack([part])    
            stop_count = time.time() - start_count
            #returns array of tasks completed
            tasks_done.put(f'Particle {id+1} was processed in {stop_count}s.')
        else:
            return np.vstack([part])

if __name__ == '__main__':
    
    print(f'Process count is {process_count}. Aviable cores are {mp.cpu_count()}')
    image_path = "dog.jpg"

    #specified array, to register and to return task values
    tasks_done = mp.Queue()
    #manager, which provides special dict, which can be returned from multiprocess function
    manager = mp.Manager()
    return_list = manager.dict()
    
    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]
    
    particle_arr = []
    
    
    if process_count >= 1 and single_process is False:
        one_el_width = w//process_count     #single elemen width, to calculate other elements
        for a in range(process_count):
            particle = image[0:h, one_el_width*a:(one_el_width*a)+one_el_width]
            particle_arr.append(particle)
        
        procs = []

        start_time = time.time()
        
        for i in range(len(particle_arr)):
            print(f'{i} process started')
            proc = mp.Process(target=process_img, args=(i, particle_arr[i], tasks_done, return_list))
            #process_img(i+1, particle_arr[i])
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()
        
        while not tasks_done.empty():   #prints completed task log
            print(tasks_done.get())
        
        return_list = list(return_list.items())     #parsing returned dict and making it a list, to sort it 
        return_list.sort(key=sort_filter)   #sorting the list using sort function

        stop_time = time.time() - start_time
        print((f'Image was processed in {stop_time}s.'))

        parsed_return_list = []
        for x in return_list:
            parsed_return_list.append(x[1]) #parsing list and returning it without keys
            
        processed_img = np.hstack(parsed_return_list)   #constructing image from particles
        cv2.namedWindow("Processed image", cv2.WINDOW_NORMAL)
        processed_img = cv2.resize(processed_img, (1000, 1000))
        cv2.imshow('Processed image', processed_img)
        cv2.waitKey(0)
    
    else:
        processed_parts = []
        one_el_width = w//4     #single elemen width, to calculate other elements
        for a in range(4):
            particle = image[0:h, one_el_width*a:(one_el_width*a)+one_el_width]
            particle_arr.append(particle)
            
        start_time = time.time() 
        
        for i in range(len(particle_arr)):
            print(f'{i} particle being processed')
            part = process_img(i, particle_arr[i])
            processed_parts.append(part)
        
        stop_time = time.time() - start_time
        
        print((f'Image was processed in {stop_time}s.'))
        
        processed_img = np.hstack(processed_parts) 
        cv2.namedWindow("Multiprocessed image", cv2.WINDOW_NORMAL)
        processed_img = cv2.resize(processed_img, (1000, 1000))
        cv2.imshow('Processed image', processed_img)
        cv2.waitKey(0)

