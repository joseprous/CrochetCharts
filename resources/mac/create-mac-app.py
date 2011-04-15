#!/usr/bin/python2.7
#
# Script by Brian C. Milco <bcmilco@gmail.com>
#
# This script generates a Mac App Bundle for a qt application
#
#
#TODO: check that the files actually exist, if they don't let the user know.

import argparse
import os
import shutil

def main():
    parser = argparse.ArgumentParser(description='Create a Mac application bundle for a Qt application.')
    parser.add_argument('-n', help='Name of the package being creating (excluding the .app extension)')
    parser.add_argument('b', help='Binary Mach-O file')
    parser.add_argument('--plist', help='Info.plist file')
    parser.add_argument('-i', '--icns', help='Binary icns file')
    parser.add_argument('-f', '--frameworks', nargs='*', help='Qt or third party framework files')
    parser.add_argument('-p', '--plugins', nargs='*', help='Qt or third party plugin files (dylib)')
    parser.add_argument('-q', '--qtconf', help='The qt.conf file')
    
    args = parser.parse_args()
    print args

    appName = args.b
    if(args.n != None):
        appName = os.path.basename(args.n)

    try:
        os.makedirs(appName + '.app/Contents/Doc/')
        os.makedirs(appName + '.app/Contents/Frameworks/')
        os.makedirs(appName + '.app/Contents/Locales/')
        os.makedirs(appName + '.app/Contents/MacOS/')
        os.makedirs(appName + '.app/Contents/Plugins/')
        os.makedirs(appName + '.app/Contents/Resources/')
    except:
        print "Folders exist."
    
    shutil.copy(args.b, appName + '.app/Contents/MacOS/')

#replace the values of the info.plist value.
    plist = 'Info.plist'
    if(args.plist != None):
        plist = args.plist
    shutil.copy(plist, appName + '.app/Contents/Info.plist')

    if(args.icns != None):
        shutil.copy(args.icns, appName + '.app/Contents/Resources/' + appName + '.icns')

    if(args.qtconf != None):
        shutil.copy(args.qtconf, appName + '.app/Contents/Resources/')

    if args.frameworks != None:
        for f in args.frameworks:
            shutil.copy(f, appName + '.app/Contents/Frameworks/')

    if args.plugins != None:
        for p in args.plugins:
            shutil.copytree(p, appName + '.app/Contents/Plugins/')
            
    
if __name__ == "__main__":
    main()