import os 
import sys
import vss_cls
import serch_cls
import argparse


def searc_by_file_name(filename,path):
    sech = serch_cls.search()
    find_file = sech.find_files(filename,path)
    return find_file

def searc_by_hash(hash,path):
    sech = serch_cls.search()
    find_file = sech.find_hash(hash,path)
    return find_file

def searc_by_folder(path,root_dir):
    path = path[3:]
    path  = os.path.join(root_dir, path)
    if os.path.exists(path):
        print("Exsiting Path: "+path)
        sech = serch_cls.search()
        find_file = sech.find_folders_files(path)
        return find_file
    else:
         print("Path Doesn't exists in " + root_dir)



def main(argv=[]):
    parser = argparse.ArgumentParser(description="Explore Volume Shadow Copies")
    parser.add_argument("-p", "--Path", type=str, help="Type path")
    parser.add_argument("-s", "--Hash", type=str, help="Type Hash")
    parser.add_argument("-f", "--FileName", type=str, help="Type File Name")
    parser.add_argument("-c", "--CopyFile", type=str, help="Type File Name")

    args = parser.parse_args()
    cs_vss = vss_cls.vss()
    IDs = cs_vss.get_devicesIDs()
    
    if args.Hash:
        for id in IDs:
            hashes = args.Hash
            if "," in hashes:
                hashex = hashes.split(',')
                for hash in hashex:
                    files = searc_by_hash(hash, id['ID'])
                    print(files)
            else:
                files = searc_by_hash(hashes, id['ID'])
                print(files)
    
    if args.FileName:
        for id in IDs:
            files = searc_by_file_name(args.FileName, id['ID'])
            print(files)
    
    if args.Path:
        for id in IDs:
            files = searc_by_folder(args.Path, id['ID'])
            print(files)
    

if __name__ == '__main__':
    main(sys.argv)