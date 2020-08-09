import os
import hashlib

class search:
    #def __init__(self):
        
    def find_files(self,filename, search_path):
        result = []
        # itrate through all dirctires and file and if match append it to an array
        for root, dir, files in os.walk(search_path):
            if filename in files:
                result.append(os.path.join(root, filename))
        return result
    
    def find_folders_files(self,search_path):
        result=[]
        for root, dir, files in os.walk(search_path):
            for filename in files:
                result.append(os.path.join(root, filename))
        return result
    
    def hash_file(self, file_name,method):
        try:
        
            # Create the hash object, can use something other than `.sha256()` if you wish
            file_hash = method
            # Open the file to read it's bytes
            with open(file_name, 'rb') as f: 
                # Read from the file. Take in the amount declared above
                fb = f.read()
                # While there is still data being read from the file
                file_hash.update(fb)
            return file_hash.hexdigest()
        except:
            pass

    def find_hash(self,hash,search_path):
        # list all hashes method and their sizes
        length_hashes = [{'size':32,'method':hashlib.md5()},{'size':40,'method':hashlib.sha1()},{'size':64,'method':hashlib.sha256()}]
        #itrate through the the size and update the method
        for arr in length_hashes:
            if arr['size'] == len(hash):
                print(str(arr['size']) +" for hash:" + hash)
                file_hash = arr['method']
        #itrate through all files and call hash_file function to return the hash. if match occur then break and print file name
        for root, dir, files in os.walk(search_path):
            for filename in files:
                file_with_path = os.path.join(root, filename)
                rtn_hash = self.hash_file(file_with_path,file_hash)
                if hash == rtn_hash:
                    return file_with_path
                    break

        