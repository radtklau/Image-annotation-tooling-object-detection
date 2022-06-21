# import the necessary packages
from scipy.spatial import distance as dist
from scipy.optimize import linear_sum_assignment
from collections import OrderedDict
import numpy as np
from operator import itemgetter



class centroidtracker():
    def __init__(self, maxDisappearedNeighbor=4, DISTANCE_TOLERANCE = 520, NEIGHBOR_TOLERANCE = (80, 40)):
        # initialize the next unique object ID along with two ordered
        # dictionaries used to keep track of mapping a given object
        # ID to its centroid and number of consecutive frames it has
        # been marked as "disappeared", respectively
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.class_id = OrderedDict()

        # store the number of maximum consecutive frames a given
        # object is allowed to be marked as "disappeared" until we
        # need to deregister the object from tracking
        self.maxDisappearedNeighbor = maxDisappearedNeighbor
        self.DISTANCE_TOLERANCE = DISTANCE_TOLERANCE
        self.NEIGHBOR_TOLERANCE = NEIGHBOR_TOLERANCE

    def register(self, centroid, class_id):
        # when registering an object we use the next available object
        # ID to store the centroid
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.class_id[self.nextObjectID] = class_id
        self.nextObjectID += 1
        

    def deregister(self, objectID):
        # to deregister an object ID we delete the object ID from
        # both of our respective dictionaries
        del self.objects[objectID]
        del self.disappeared[objectID]
        del self.class_id[objectID]

    def update(self, rects, input_class_ids):
        # check to see if the list of input bounding box rectangles
        # is empty
        if len(rects) == 0:
            # loop over any existing tracked objects and mark them
            # as disappeared
            objectsToDeregister = list()
            for objectID in self.disappeared.keys():
                objectsToDeregister.append(objectID)
            for objectID in objectsToDeregister:
                self.deregister(objectID)

            # return early as there are no centroids or tracking info
            # to update
            return self.objects

        # initialize an array of input centroids for the current frame
        inputCentroids = np.zeros((len(rects), 2), dtype="int")

        # loop over the bounding box rectangles
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            # use the bounding box coordinates to derive the centroid
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)

        # if we are currently not tracking any objects take the input
        # centroids and register each of them
        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(inputCentroids[i], input_class_ids[i])

        # otherwise, are are currently tracking objects so we need to
        # try to match the input centroids to existing object
        # centroids
        else:
            #create a copy of objects dictionary for motion estimation by neighbors and 
            #an empty list for objects which have to be checked for motion estimation
            copy_objects = self.objects.copy()
            objects_to_estimate_motion = list()


            #create list of all classes (cats) which exist in current objects
            cat_list = list(set(self.class_id.values()))

            for cat in cat_list:
                #create emtpy lists of IDs and centroids for existing objects for cat
                cat_objectIDs = list()
                cat_objectCentroids = list()

                # create empty list of inputCentroids for cat
                cat_inputCentroids_index = list()

                #only use the object IDs and centroids for objects of respective class:
                for key in self.objects.keys():
                    if self.class_id[key] == cat:
                        cat_objectIDs.append(key)
                        cat_objectCentroids.append(self.objects[key])
            
                # only use the inputCentroids with respective class
                for i in range(0, len(inputCentroids)):
                    if input_class_ids[i] != cat:
                        cat_inputCentroids_index.append(i)
                cat_inputCentroids = np.delete(inputCentroids, (cat_inputCentroids_index),0)

                # if there are no inputCentroids of this class, mark existing objects of the class as diappered
                if cat_inputCentroids.size == 0:
                    for objectID in cat_objectIDs:
                        self.disappeared[objectID] += 1
                        # add to list for neighbor_motion
                        objects_to_estimate_motion.append(objectID)
                    continue

                # compute the distance between each pair of object
                # centroids and input centroids, respectively -- our
                # goal will be to match an input centroid to an existing
                # object centroid
                D = dist.cdist(np.array(cat_objectCentroids), cat_inputCentroids)


                # use hunagrian method to minimize total matching cost
                row_ind, col_ind = linear_sum_assignment(D)

                # check if distance between pairs is below the tolerated distance:
                for i, j in zip(row_ind, col_ind):
                    # If yes, allocate:
                    if D[i,j] <= self.DISTANCE_TOLERANCE:
                        objectID = cat_objectIDs[i]
                        self.objects[objectID] = cat_inputCentroids[j]
                        self.disappeared[objectID] = 0
                    # if not, register input and mark object as disappeared
                    else:
                        self.register(cat_inputCentroids[j], cat)
                        objectID = cat_objectIDs[i]
                        self.disappeared[objectID] += 1
                        # add to list for neighbor_motion
                        objects_to_estimate_motion.append(objectID)
                    
                # check if objects are not in row_ind because there are more inputs than objects. If so, mark as disappeared and add to list:
                for i, objectID in enumerate(cat_objectIDs):
                    if i not in row_ind:
                        self.disappeared[objectID] += 1
                        # add to list for neighbor_motion
                        objects_to_estimate_motion.append(objectID)
                        
                    
                # check if inputs are not in col_ind because there are more objects than inputs. If so, register them:
                for j, _ in enumerate(cat_inputCentroids):
                    if j not in col_ind:
                        self.register(cat_inputCentroids[j], cat)


            # register inputCentroids whose class is not in the objects yet
            for i in range(0, len(inputCentroids)):
                if input_class_ids[i] not in cat_list:
                    self.register(inputCentroids[i], input_class_ids[i])

            # go thorugh list of disappeared objects to check if motion can be estimated by neighbors:
            for objectID in objects_to_estimate_motion:
                self.neighbor_motion(objectID, copy_objects, objects_to_estimate_motion)

        # return the set of trackable objects
        return self.objects



    def neighbor_motion(self, objectID, copy_objects, objects_to_estimate_motion):
        neighbor_motions = list()
        for neighborID, neighborCentroid in zip(copy_objects.keys(), copy_objects.values()):
            # check if NEIGHBOR_TOLERANCE is not exceeded and if neighbor is not object itself 
            # and if neighbor has not been deregistered, and if neighbour is not in objects_to_estimate_motion itself
            if dist.euclidean(neighborCentroid[0], self.objects[objectID][0]) <= self.NEIGHBOR_TOLERANCE[0] and dist.euclidean(neighborCentroid[1], self.objects[objectID][1]) <= self.NEIGHBOR_TOLERANCE[1]\
                and neighborID != objectID and neighborID in self.objects.keys() and neighborID not in objects_to_estimate_motion:
                neighbor_motions.append((neighborCentroid[0] - self.objects[neighborID][0], neighborCentroid[1] - self.objects[neighborID][1]))
        if len(neighbor_motions) != 0:
            neighbor_average = (sum(i for i, j in neighbor_motions) /len(neighbor_motions), sum(j for i, j in neighbor_motions) /len(neighbor_motions))
            self.objects[objectID][0] -= neighbor_average[0]
            self.objects[objectID][1] -= neighbor_average[1]
            # check to see if the number of consecutive
            # frames the object has been marked "disappeared"
            # for warrants deregistering the object
            # check if vehicle was on edges of the lanes or has exceeded maxDisappearedNeighbor
            if (self.disappeared[objectID] > self.maxDisappearedNeighbor):
                self.deregister(objectID)
        #if there is no neighbor inside neighbor_TOLERANCE, object will be deregistered
        else:
            self.deregister(objectID)
