import os 
import sys
import vss_cls
import serch_cls
import argparse
import json
import time
import hashlib

def searc_by_file_name(filename,path):
    sech = serch_cls.search()
    find_file = sech.find_files(filename,path)
    return  find_file

def searc_by_hash(hash,path):
    sech = serch_cls.search()
    find_file = sech.find_hash(hash,path)
    return  find_file

def searc_by_folder(path,root_dir):
    path = path[3:]
    path  = os.path.join(root_dir, path)
    if os.path.exists(path):
        print("Exsiting Path: "+path)
        sech = serch_cls.search()
        find_file = sech.find_folders_files(path)
        return  find_file
    else:
         print("Path Doesn't exists in " + root_dir)
################################################################
def copy_file_filename(filename,path,dest_path):
    if os.path.exists(dest_path) == True:
       if os.path.isdir(dest_path) == True:
           copy_file = searc_by_file_name(filename,path)
           for cf in copy_file:
             fname = os.path.basename(cf)
             with open(cf, 'rb') as cp:
              cpy = cp.read()
             with open(os.path.join(dest_path,fname) , 'wb+') as df:
              df.write(cpy)
       else: 
          print('The path you have entered is not a directory')
    else:
       print('The path you have entered does not exist')
#################################################################
def hash_files(filename):
    sech = serch_cls.search()
    find_file = sech.hash_file(filename,hashlib.md5())
    return find_file

def main(argv=[]):
    parser = argparse.ArgumentParser(description="Explore Volume Shadow Copies")
    parser.add_argument("-p", "--Path", type=str, help="")
    parser.add_argument("-v", "--Vss", type=str, help="Check vss")
    parser.add_argument("-s", "--Hash",type=str, help="")
    parser.add_argument("-f", "--FileName",type=str, help="")
    parser.add_argument("-k", "--Keywords",type=str, help="Type the File Name or Hash or Path")
    parser.add_argument("-c", "--CopyFile", nargs= 2 ,type=str, help="Type the File Name")
    parser.add_argument("-j", "--JsonOutput", help="Print the output in json format")

    args = parser.parse_args()
    cs_vss = vss_cls.vss()
    IDs = cs_vss.get_devicesIDs()
#################################################################
    if args.Vss == "true":
        for id in IDs:
            print(id['ID'])


    if args.Hash == "true":
        try:
            for id in IDs:
                hashes = args.Keywords
                if "," in hashes:
                        hashex = hashes.split(',')
                        for hash in hashex:
                            files = searc_by_hash(hash, id['ID'])
                            for f in files:
                                file_meta = os.stat(f)
                                access= time.strftime("%b %d %Y %H:%M:%S", time.localtime(file_meta.st_atime))
                                modify= time.strftime("%b %d %Y %H:%M:%S", time.localtime(file_meta.st_mtime))
                                print(" File Name: "+os.path.basename(f)+'\n'+" File Owner: "+str(file_meta.st_uid)+'\n'+" File Size: "+str(file_meta.st_size)+' Bytes \n'+" File Last Accessed: "+access+'\n'+" File Last Modified: "+modify)    
                else:
                    files = searc_by_hash(hashes, id['ID'])
                    for f in files:
                        file_meta = os.stat(f)
                        access= time.strftime("%b %d %Y %H:%M:%S", time.localtime(file_meta.st_atime))
                        modify= time.strftime("%b %d %Y %H:%M:%S", time.localtime(file_meta.st_mtime))
                        
                        print(" File Name: "+os.path.basename(f)+'\n'+" Path: "+f+'\n'+" File Owner: "+str(file_meta.st_uid)+'\n'+" File Size: "+str(file_meta.st_size)+' Bytes \n'+" File Last Accessed: "+access+'\n'+" File Last Modified: "+modify)        
        except:
            print("No such Hash exists")
################################################################
    if args.FileName == "true": 
        for id in IDs:
            files = searc_by_file_name(args.Keywords, id['ID'])
            for f in files:
               file_meta = os.stat(f)     
               access= time.strftime("%b %d %Y %H:%M:%S", time.localtime(file_meta.st_atime))
               modify= time.strftime("%b %d %Y %H:%M:%S", time.localtime(file_meta.st_mtime))
               print(" File Name: "+os.path.basename(f)+'\n'+" Path: "+f+'\n'+" Hash: "+str(hash_files(f))+'\n'+" File Owner: "+str(file_meta.st_uid)+'\n'+" File Size: "+str(file_meta.st_size)+' Bytes \n'+" File Last Accessed: "+access+'\n'+" File Last Modified: "+modify)
################################################################
    if args.Path == "true":
        for id in IDs:
            files = searc_by_folder(args.Keywords, id['ID'])
            for f in files:
               file_meta = os.stat(f)
               access= time.strftime("%b %d %Y %H:%M:%S", time.localtime(file_meta.st_atime))
               modify= time.strftime("%b %d %Y %H:%M:%S", time.localtime(file_meta.st_mtime))
               print(" File Name: "+os.path.basename(f)+'\n'+" Path: "+f+'\n'+" File Owner: "+str(file_meta.st_uid)+'\n'+" File Size: "+str(file_meta.st_size)+' Bytes \n'+" File Last Accessed: "+access+'\n'+" File Last Modified: "+modify) 
################################################################
    if args.CopyFile:
       args = args.CopyFile
       fn,dst = tuple(args)
       for id in IDs:
         copy_file_filename (fn,id['ID'],dst)



if __name__ == '__main__':
      main(sys.argv)








