'''
Created on 26 mars 2014

@author: gtheurillat
'''

import os, shutil
from PIL import Image

class Cut_Images(object):
    
    ""
    
    def __init__(self):
        ""
        self.isEuropeenLectureWay = True
        
    def start(self, input, output, isEuropeenLectureWay):
        ""
        self.isEuropeenLectureWay = isEuropeenLectureWay
        
        if not os.path.exists(output):
            print "[INFO] Creation du repertoire de sortir '{0}'".format(output)
            os.makedirs(output)
        self._parcours_folder(input, output, "")
        
        return True, ""
    
    def _parcours_folder(self, folder_path, output, current_folder):
        print "[info]: recherche d'images dans le repertoire: '{0}'".format(folder_path)
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            if os.path.isfile(item_path):
                item_extension = item.split(".")[-1]
                item_name = item.split(".")[:-1]
                if item_extension.lower() in ["jpg", "png"]:
                    self._try_to_cut(item_path, output, current_folder)
            elif os.path.isdir(item_path):
                self._parcours_folder(item_path, output, os.path.join(current_folder, item))
        
    
    def _try_to_cut(self,image_file, output, current_folder):
        ""
        try:
            if not os.path.exists(os.path.join(output, current_folder)):
                os.makedirs(os.path.join(output, current_folder))
            
            img = Image.open(image_file)
            width = img.size[0]
            height = img.size[1]
            #print "height: {0} | width: {1}".format(height, width)
            item_extension = image_file.split(".")[-1]
            item_name = ".".join(os.path.basename(image_file).split(".")[:-1])
            #print "name {0} | ext: {1}".format(item_name, item_extension)
            #coupe seulement les page en paysage
            if width > height:
                print "[INFO] Decoupage de l'image '{0}'".format(image_file)
                
                #dans le sens de lecture "europpeen" la page de gauche est le premiere et la page de droite la dexieme
                right_number = 1
                left_number = 0
                if self.isEuropeenLectureWay == False:
                    #dans le sens de lecture "asiatique" la page de gauche est la deuxiement et la page de droite al premiere
                    right_number = 0
                    left_number = 1
                
                #image de gauche
                coord_gauche = (0, 0, width/2, height)
                region_gauche = img.crop(coord_gauche)
                region_gauche.save(os.path.join(output, current_folder, "{0}_{2}.{1}".format(item_name, item_extension, left_number)))
                print "\t [INFO] Decoupage de l'image de gauche"
                 
                #image de droite
                coord_droite = (width/2, 0, width, height)
                region_droite = img.crop(coord_droite)
                region_droite.save(os.path.join(output, current_folder, "{0}_{2}.{1}".format(item_name, item_extension, right_number)))
                print "\t [INFO] Decoupage de l'image de droite"
            else:
                print "[INFO] Image '{0}' deja en portrait. Pas de decoupage".format(image_file)
                print "\t [INFO] copy '{0}' -> '{1}'".format(image_file, os.path.join(output, current_folder, os.path.basename(image_file)))
                shutil.copyfile(image_file, os.path.join(output, current_folder, os.path.basename(image_file)))
            #img.close()
        except Exception, e:
            print "[ERREUR] {0}".format(e)
                

            